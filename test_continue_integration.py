"""Continuation integration: estimated timing and original restore policy."""
import os
os.environ['SDL_VIDEODRIVER']='dummy'
os.environ['SDL_AUDIODRIVER']='dummy'
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import game
from cabinet import CabinetStore
from replay import digest
from stations import Phase

class ContinueIntegration(unittest.TestCase):
    def final_death(self,g,idx=0):
        p=g.players[idx];p.lives=1;p.safe=0;p.effects={};p.entry=0
        p.pos=g.arena.entries[idx]
        self.assertTrue(g.hurt(p));self.assertEqual(p.lives,0)
        return p

    def test_final_death_delay_accept_preserves_score_and_bonus(self):
        g=game.Match(2,seed=31,continue_seconds=10,continue_delay=1)
        p=g.players[0];p.score=12345;p.bonus_life=True
        self.final_death(g)
        self.assertTrue(g.continues.active)
        self.assertFalse(g.can_continue_station(0));self.assertFalse(g.continue_station(0))
        g.foes=[];g.items={}
        for _ in range(60):g.update(1/60)
        self.assertTrue(g.can_continue_station(0))
        self.assertTrue(g.continue_station(0));self.assertFalse(g.continue_station(0))
        p=g.players[0]
        self.assertEqual((p.score,p.bonus_life,p.lives),(12345,True,g.rules['starting_lives']))
        self.assertEqual(p.pos,g.arena.spawns[0]);self.assertEqual(p.effects,{})
        self.assertGreater(p.entry,0);self.assertGreater(p.safe,0)
        self.assertFalse(g.continues.can_accept(0))

    def test_last_human_window_defers_settlement_and_dead_score(self):
        g=game.Match(1,seed=31,continue_seconds=.5,continue_delay=0)
        g.fill_vacancies();p=self.final_death(g);p.score=777
        g.foes=[];g.items={}
        for _ in range(29):g.update(1/60)
        self.assertFalse(g.over);self.assertEqual(p.score,777)
        self.assertFalse(any(e['event']=='match_end' for e in g.ledger.events))
        g.update(1/60);self.assertTrue(g.over)
        self.assertEqual(sum(e['event']=='match_end' for e in g.ledger.events),1)
        before=digest(g);g.update(1);self.assertEqual(digest(g),before)

    def test_one_human_expiry_does_not_end_other_human_and_timer_overrides(self):
        g=game.Match(2,seed=31,continue_seconds=.1,continue_delay=0)
        self.final_death(g);g.foes=[];g.items={}
        for _ in range(6):g.update(1/60)
        self.assertFalse(g.over);self.assertFalse(g.can_continue_station(0))
        self.final_death(g,1);g.time=1/60;g.update(1/60)
        self.assertTrue(g.over);self.assertFalse(g.can_continue_station(1))
        self.assertEqual(g.ledger.events[-1]['context']['reason'],'time')

    def test_raw_match_default_has_no_continue(self):
        g=game.Match(1,seed=31);self.final_death(g);g.update(1/60)
        self.assertTrue(g.over);self.assertFalse(g.continues.active)

class AppContinueIntegration(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(dir=Path.cwd())
        self.store=CabinetStore(self.tmp.name)
        self.app=game.App(cabinet=self.store,simulate_controllers=True)
        self.app.count=1;self.app.start();game.pg.event.clear()
    def tearDown(self):game.pg.quit();self.tmp.cleanup()
    def kill(self):
        p=self.app.match.players[0];p.lives=1;p.safe=0;p.effects={}
        p.pos=self.app.match.arena.entries[0];p.entry=0
        self.assertTrue(self.app.match.hurt(p));return p
    def test_background_moves_and_pause_guide_freeze_without_autosave(self):
        g=self.app.match;p=self.kill();p.score=900
        self.assertEqual(self.app.phase,Phase.CONTINUE)
        g.paused=True;paused=digest(g)
        self.app.advance(5);self.assertEqual(digest(g),paused)
        g.paused=False;self.app.help=True;paused=digest(g)
        self.app.advance(5);self.assertEqual(digest(g),paused)
        self.app.help=False
        for _ in range(90):self.app.advance(1/60)
        self.assertTrue(any(b.bot and b.pos!=g.arena.spawns[b.idx] for b in g.players))
        self.assertEqual(p.score,900);self.app.save_result()
        self.assertNotIn(self.app.session_id,self.store.recorded)
        self.assertFalse(self.app.pending_results)
    def test_payment_failure_retry_and_no_double_debit(self):
        self.store.settings['free_play']=False;self.store.credits=1;self.store.save()
        self.kill();g=self.app.match
        self.app.station_action(0);self.assertEqual(self.store.credits,1)
        for _ in range(60):self.app.advance(1/60)
        self.assertTrue(g.can_continue_station(0))
        with patch('cabinet.atomic_json',side_effect=OSError('disk')):self.app.station_action(0)
        self.assertEqual(self.store.credits,1);self.assertEqual(g.players[0].lives,0)
        self.assertTrue(g.can_continue_station(0))
        self.app.station_action(0)
        self.assertEqual(self.store.credits,0);self.assertGreater(g.players[0].lives,0)
        self.app.station_action(0);self.assertEqual(self.store.credits,0)
    def test_failed_debit_message_is_visible_in_continuation_render(self):
        self.store.settings['free_play']=False;self.store.credits=1;self.store.save()
        self.kill()
        for _ in range(60):self.app.advance(1/60)
        with patch('cabinet.atomic_json',side_effect=OSError('disk')):self.app.station_action(0)
        labels=[];original=self.app.text
        def capture(text,*args,**kwargs):
            labels.append(str(text));return original(text,*args,**kwargs)
        with patch.object(self.app,'text',capture):self.app.draw(0)
        self.assertTrue(any('could not be saved' in label for label in labels),labels)

    def test_no_credit_offer_remains_and_new_station_does_not_redeem_it(self):
        self.kill();g=self.app.match
        for _ in range(60):self.app.advance(1/60)
        self.store.settings['free_play']=False;self.store.credits=0
        self.app.station_action(0);self.assertEqual(g.players[0].lives,0)
        self.assertTrue(g.can_continue_station(0))
        self.store.settings['free_play']=True;self.app.station_action(7)
        self.assertTrue(g.players[7].joined);self.assertEqual(g.players[0].lives,0)
        self.assertTrue(g.can_continue_station(0))
    def test_p6_down_key_does_not_insert_credit_during_other_station_offer(self):
        self.app.count=6;self.app.start();self.kill()
        before=self.store.credits
        game.pg.event.post(game.pg.event.Event(game.pg.KEYDOWN,key=game.pg.K_c,unicode='c'))
        self.app.events()
        self.assertEqual(self.store.credits,before)
        self.assertEqual(self.app.match.players[5].wanted,(0,1))

    def test_bot_death_does_not_offer_continue_and_pause_rejects_accept(self):
        g=self.app.match;bot=g.players[7];bot.lives=1;bot.safe=0;bot.effects={}
        self.assertTrue(g.hurt(bot));self.assertFalse(g.continues.active)
        self.kill()
        for _ in range(60):self.app.advance(1/60)
        g.paused=True
        before=digest(g);self.app.station_action(0)
        self.assertEqual(digest(g),before)
        g.paused=False;self.app.help=True
        before=digest(g);self.app.station_action(0)
        self.assertEqual(digest(g),before)

    def test_continue_prompt_bounds_all_stations_all_maps(self):
        self.app.count=8;self.app.continue_delay=0
        for theme in range(4):
            self.app.theme=theme;self.app.start();g=self.app.match
            for p in g.players:
                p.lives=1;p.safe=0;p.effects={};g.hurt(p)
            for clock in (0,.6):
                self.app.animation_time=clock;labels=[];original=self.app.text
                def capture(text,x,y,color=(224,234,247),font=None):
                    if str(text).startswith('CONTINUE ') or str(text).endswith(' START') or text=='INSERT COIN':
                        if y<game.H-12:
                            labels.append((str(text),(font or self.app.font).render(str(text),True,color).get_rect(topleft=(x,y))))
                    return original(text,x,y,color,font)
                with patch.object(self.app,'text',capture):self.app.draw(0)
                self.assertEqual(len(labels),8)
                for label,rect in labels:
                    self.assertLessEqual(rect.width,108,(label,rect))
                    self.assertTrue(game.pg.Rect(0,0,game.W,game.H-12).contains(rect),(label,rect))

    def test_continue_timeout_automatically_opens_saved_qualifying_initials(self):
        self.app.continue_seconds=.1;self.app.continue_delay=0;self.app.start()
        p=self.kill();p.score=333;token=self.app.session_id
        for _ in range(6):self.app.advance(1/60)
        self.assertTrue(self.app.match.over)
        self.assertIn(token,self.store.recorded)
        self.assertIsNotNone(self.app.name_entry)
        self.assertEqual(self.app.name_entry['rows'][0]['score'],333)
        before=digest(self.app.match);self.app.advance(2)
        self.assertEqual(digest(self.app.match),before)

    def test_timed_end_does_not_force_continue_timeout_name_entry(self):
        self.kill();self.app.match.time=1/60
        self.app.advance(1/60)
        self.assertTrue(self.app.match.over)
        self.assertIsNone(self.app.name_entry)
        self.assertEqual(self.app.match.ledger.events[-1]['context']['reason'],'time')

    def test_auto_name_write_failure_retains_result_for_explicit_retry(self):
        self.app.continue_seconds=.1;self.app.continue_delay=0;self.app.start()
        self.kill();token=self.app.session_id
        with patch('cabinet.atomic_json',side_effect=OSError('disk')):
            for _ in range(6):self.app.advance(1/60)
        self.assertIsNone(self.app.name_entry)
        self.assertNotIn(token,self.store.recorded)
        self.assertTrue(self.app.pending_results)
        self.app.begin_name_entry()
        self.assertIn(token,self.store.recorded)
        self.assertIsNotNone(self.app.name_entry)

    def test_expiry_pending_save_survives_immediate_restart(self):
        self.app.continue_seconds=.1;self.app.continue_delay=0;self.app.start()
        p=self.kill();p.score=222;token=self.app.session_id
        with patch('cabinet.atomic_json',side_effect=OSError('disk')):
            for _ in range(6):self.app.advance(1/60)
            self.assertTrue(self.app.match.over)
            self.app.start()
        self.assertFalse(self.app.match.over);self.assertTrue(self.app.pending_results)
        self.app.save_result();self.assertFalse(self.app.pending_results)
        rows=[row for row in self.store.high_scores if row.get('session')==token]
        self.assertEqual(len(rows),1);self.assertEqual(rows[0]['score'],222)

if __name__=='__main__':unittest.main(verbosity=2)
