"""Bot roster policy tests; AI difficulty is original and not cabinet measured."""
import os
os.environ['SDL_VIDEODRIVER']='dummy'
os.environ['SDL_AUDIODRIVER']='dummy'
import unittest
from game import Match

class Bots(unittest.TestCase):
    def test_explicit_fill_all_maps_and_human_counts(self):
        for theme in range(4):
            for count in (1,2,8):
                g=Match(count,theme,seed=17)
                self.assertEqual(len(g.players),count)
                self.assertEqual(g.fill_vacancies(),8-count)
                self.assertEqual(len(g.players),8)
                self.assertEqual(g.count,count)
                self.assertEqual(len(g.rankings()),count)
                for idx,p in enumerate(g.players):
                    self.assertEqual(p.idx,idx)
                    self.assertEqual(p.joined,idx<count)
                    self.assertEqual(p.bot,idx>=count)
                    self.assertEqual(p.pos,g.arena.spawns[idx])
                    self.assertEqual(p.lives,3)
                    self.assertEqual(p.entry,.8)
                    self.assertEqual(p.direction,(0,1) if p.pos[1]==0 else (0,-1))

    def test_replacing_bot_starts_fresh_human(self):
        g=Match(1,seed=1);g.fill_vacancies();bot=g.players[7]
        bot.score=9876;bot.lives=1;bot.effects={'Titan':7};bot.stun=2
        self.assertTrue(g.join_station(7))
        p=g.players[7]
        self.assertIsNot(p,bot)
        self.assertEqual((p.score,p.lives,p.bot,p.joined),(0,3,False,True))
        self.assertEqual((p.stun,p.effects,p.safe,p.entry),(0,{},2.5,.8))
        self.assertEqual(g.count,2)
        self.assertTrue(g.ledger.events[-1]['context']['replaced_bot'])
        self.assertEqual({r['player_id'] for r in g.rankings()},{1,8})

    def test_bot_replacement_clears_owned_weapons_and_contact_cooldown(self):
        g=Match(1,seed=1);g.fill_vacancies()
        g.traps={(1,1):(7,3),(2,1):(0,3)}
        g.bump_cooldowns={(0,7):.2,(0,1):.2}
        g.foe_carriers={0:7};g.foe_modes[0]='carried'
        ghost_position=g.foes[0]
        self.assertTrue(g.join_station(7))
        self.assertEqual(g.traps,{(2,1):(0,3)})
        self.assertEqual(g.bump_cooldowns,{(0,1):.2})
        self.assertEqual(g.foe_carriers,{})
        self.assertEqual(g.foe_modes[0],'eyes')
        self.assertEqual(g.foes[0],ghost_position)

    def test_fill_does_not_revive_or_reset_actors(self):
        g=Match(2,seed=1);g.fill_vacancies()
        human=g.players[0];bot=g.players[7]
        human.lives=0;bot.lives=0;bot.score=999
        before=g.snapshot();events=len(g.ledger.events)
        self.assertEqual(g.fill_vacancies(),0)
        self.assertEqual(g.snapshot(),before)
        self.assertEqual(len(g.ledger.events),events)
        self.assertFalse(g.join_station(0))
        self.assertTrue(g.join_station(7))

    def test_bots_do_not_prolong_eliminated_human_match(self):
        g=Match(2,seed=1);g.fill_vacancies()
        g.players[0].lives=0;g.update(1/60)
        self.assertFalse(g.over)
        g.players[1].lives=0;g.update(1/60)
        self.assertTrue(g.over)
        self.assertTrue(any(p.bot and p.lives>0 for p in g.players))
        self.assertEqual(g.ledger.events[-1]['event'],'match_end')
        self.assertEqual(g.ledger.events[-1]['context']['reason'],'elimination')

    def test_sparse_join_fill_and_operator_lives(self):
        g=Match(0,seed=1,rules={'starting_lives':5})
        self.assertTrue(g.join_station(6));self.assertEqual(g.fill_vacancies(),7)
        self.assertEqual([p.idx for p in g.players if p.joined],[6])
        self.assertEqual(g.count,1)
        self.assertTrue(all(p.lives==5 for p in g.players))
        for _ in range(48):g.update(1/60)
        self.assertTrue(all(p.pos==g.arena.entries[p.idx] for p in g.players))
        g.new_arena(1)
        self.assertEqual(sum(p.bot for p in g.players),7)
        self.assertTrue(all(p.pos==g.arena.spawns[p.idx] for p in g.players))

    def test_fill_paused_and_finished_is_noop(self):
        for state in ('paused','over'):
            g=Match(1,seed=1);setattr(g,state,True)
            before=g.snapshot()
            self.assertEqual(g.fill_vacancies(),0)
            self.assertEqual(g.snapshot(),before)

class AppBots(unittest.TestCase):
    def test_input_autoplay_and_station_takeover(self):
        from collections import defaultdict
        from unittest.mock import patch
        import game
        app=game.App(simulate_controllers=True)
        try:
            app.cabinet.settings.update(fill_bots=True,free_play=True)
            app.count=1;app.start();g=app.match
            self.assertEqual(sum(p.bot for p in g.players),7)
            self.assertFalse(app.demo)
            keys=defaultdict(bool)
            for station_keys in game.KEYS:keys[station_keys[0]]=True
            with patch.object(game.pg.key,'get_pressed',return_value=keys):app.inputs()
            self.assertEqual(g.players[0].wanted,game.DIRS[0])
            self.assertTrue(all(p.wanted==(0,0) for p in g.players if p.bot))
            human_wanted=g.players[0].wanted
            for _ in range(90):app.advance(1/60)
            self.assertEqual(g.players[0].wanted,human_wanted)
            self.assertTrue(any(p.pos!=g.arena.spawns[p.idx] for p in g.players if p.bot))
            bot=g.players[7];bot.score=1111;bot.effects={'Titan':4}
            app.draw(.25)
            self.assertEqual(app.presentation.radius(7),36)
            app.station_action(7)
            self.assertFalse(g.players[7].bot)
            self.assertTrue(g.players[7].joined)
            self.assertEqual(g.players[7].score,0)
            self.assertEqual(g.count,2)
            app.draw(0)
            self.assertEqual(app.presentation.radius(7),17)
        finally:game.pg.quit()

    def test_filled_replay_roundtrip(self):
        from replay import record,replay,digest
        import json
        for count in (1,2,8):
            document=record(count,3,42,180,fill_bots=True)
            restored=replay(json.loads(json.dumps(document)))
            self.assertEqual(digest(restored),document['final_digest'])
            self.assertEqual(restored.count,count)
            self.assertEqual(sum(p.bot for p in restored.players),8-count)

if __name__=='__main__':unittest.main(verbosity=2)
