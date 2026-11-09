"""Cabinet QA uses temporary stores only, never the real user profile."""
import os
os.environ.setdefault('SDL_VIDEODRIVER','dummy');os.environ.setdefault('SDL_AUDIODRIVER','dummy')
import json, tempfile, unittest
from pathlib import Path
from unittest.mock import patch
import pygame as pg
from cabinet import CabinetStore,DEFAULTS,atomic_json,spectator_view
from spectator import read_feed,draw_scoreboard
from game import App,Match

class CabinetQA(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory(dir=Path.cwd());self.root=Path(self.tmp.name);self.store=CabinetStore(self.root)
 def tearDown(self):pg.quit();self.tmp.cleanup()
 def app(self):return App(simulate_controllers=True,cabinet=self.store)
 def key(self,app,key):
  pg.event.post(pg.event.Event(pg.KEYDOWN,key=key,mod=0));app.events()
 def paid(self,credits):
  self.store.configure(dict(DEFAULTS,free_play=False));self.store.credits=credits;self.store.save()
 def test_operator_events_save_cancel_and_new_match_rules(self):
  a=self.app();self.key(a,pg.K_F11);self.assertTrue(a.operator_open)
  self.key(a,pg.K_RIGHT);a.draw();self.key(a,pg.K_RETURN)
  self.assertEqual(CabinetStore(self.root).settings['starting_lives'],4)
  self.key(a,pg.K_F11);self.key(a,pg.K_RIGHT);self.key(a,pg.K_ESCAPE)
  self.assertEqual(self.store.settings['starting_lives'],4)
  a.count=8;a.start();self.assertTrue(all(p.lives==4 for p in a.match.players))
  self.key(a,pg.K_F11);self.assertFalse(a.operator_open)
 def test_credits_atomic_preset_and_station_find_eliminated(self):
  self.paid(1);a=self.app();a.count=2
  self.assertFalse(a.start());self.assertEqual(self.store.credits,1);self.assertIsNone(a.match)
  self.key(a,pg.K_c);self.assertEqual(self.store.credits,2)
  self.assertTrue(a.start());self.assertEqual(self.store.credits,0)
  a.station_action(0);self.assertEqual(self.store.credits,0)
  a.match.players[0].lives=0;a.station_action(0)
  self.assertEqual(a.match.players[0].lives,0);self.assertEqual(self.store.credits,0)
  a.station_action(7);self.assertFalse(any(p.idx==7 and p.joined for p in a.match.players))
 def test_freeplay_sparse_join_and_scores_overlay(self):
  a=self.app();self.key(a,pg.K_h);self.assertTrue(a.scores_open);a.draw()
  self.key(a,pg.K_h);self.key(a,pg.K_F10)
  self.assertEqual(a.match.count,1);self.assertEqual(self.store.credits,0);a.draw()
 def test_store_roundtrip_rules_credit_and_ties_once(self):
  self.store.configure(dict(DEFAULTS,starting_lives=2,bonus_threshold=0,match_seconds=90))
  self.store.add_credit();m=Match(8,rules=self.store.settings);m.over=True
  for p in m.players:p.score=123
  self.assertTrue(self.store.record(m,'a'));self.assertFalse(self.store.record(m,'a'))
  loaded=CabinetStore(self.root);self.assertEqual(loaded.credits,1)
  self.assertEqual(len(loaded.high_scores),8);self.assertFalse(loaded.record(m,'a'))
  self.assertEqual(m.time,90);self.assertTrue(all(p.lives==2 for p in m.players))
 def test_failed_writes_rollback(self):
  self.paid(3);m=Match(1);m.over=True
  with patch('cabinet.atomic_json',side_effect=OSError('denied')):
   self.assertFalse(self.store.add_credit());self.assertEqual(self.store.credits,3)
   self.assertFalse(self.store.pay(1));self.assertEqual(self.store.credits,3)
   self.assertFalse(self.store.configure(dict(DEFAULTS,starting_lives=5)))
   self.assertFalse(self.store.record(m,'fail'));self.assertEqual(self.store.high_scores,[])
   self.assertNotIn('fail',self.store.recorded)
  self.assertFalse(self.store.settings['free_play'])
 def test_corrupt_file_fully_resets_not_partial_settings(self):
  atomic_json(self.store.path,{'settings':dict(DEFAULTS,starting_lives=5),'credits':12,'high_scores':[{'score':1,'player_id':None}]})
  loaded=CabinetStore(self.root)
  self.assertEqual(loaded.settings,DEFAULTS);self.assertEqual(loaded.credits,0);self.assertEqual(loaded.high_scores,[])
  self.assertTrue(loaded.error)
  self.store.path.write_text('{broken');self.assertTrue(CabinetStore(self.root).error)
 def test_results_record_before_immediate_restart_or_escape(self):
  for key in (pg.K_RETURN,pg.K_F3,pg.K_ESCAPE):
   with self.subTest(key=key):
    a=self.app();a.count=2;a.start();a.match.over=True
    a.match.players[0].score=9876;token=a.session_id
    self.key(a,key)
    self.assertIn(token,self.store.recorded)
    self.assertTrue(any(r['score']==9876 for r in self.store.high_scores))
    pg.quit()
 def test_real_run_records_once_and_publishes_feed(self):
  a=self.app();a.count=8;a.start();a.match.over=True
  a.spectator_path=self.root/'feed.json';a.publish_clock=1
  a.run(frames=3)
  self.assertEqual(len(self.store.high_scores),8)
  feed=read_feed(self.root/'feed.json');self.assertEqual(len(feed['ranking']),8)
  self.assertEqual(feed['phase'],'results')
 def test_spectator_validation_and_stale_actual_render(self):
  pg.init();canvas=pg.Surface((960,720));m=Match(8)
  value=spectator_view(m,'playing','Test');atomic_json(self.root/'feed.json',value)
  feed=read_feed(self.root/'feed.json');draw_scoreboard(canvas,feed,now=value['updated'])
  fresh=pg.image.tobytes(canvas,'RGB')
  draw_scoreboard(canvas,feed,now=value['updated']+4)
  self.assertNotEqual(fresh,pg.image.tobytes(canvas,'RGB'));draw_scoreboard(canvas,None)
  for bad in ('bad',None,{},float('nan'),float('inf')):
   value['remaining']=bad;atomic_json(self.root/'feed.json',value)
   self.assertIsNone(read_feed(self.root/'feed.json'))
 def test_all_counts_paid_start_and_rule_threshold(self):
  self.paid(50)
  for count in range(1,9):
   with self.subTest(count=count):
    a=self.app();a.count=count;before=self.store.credits
    self.assertTrue(a.start());self.assertEqual(self.store.credits,before-count)
    self.assertEqual(a.match.count,count);a.draw();pg.quit()
  rules=dict(DEFAULTS,starting_lives=1,bonus_threshold=0)
  m=Match(1,rules=rules);m.players[0].score=99999;m.award(m.players[0],'dot')
  self.assertEqual(m.players[0].lives,1)
 def test_operator_failed_save_stays_open_and_no_rule_mutation(self):
  a=self.app();self.key(a,pg.K_F11);self.key(a,pg.K_RIGHT)
  with patch('cabinet.atomic_json',side_effect=OSError('denied')):self.key(a,pg.K_RETURN)
  self.assertTrue(a.operator_open);self.assertEqual(self.store.settings,DEFAULTS)
  a.draw()
 def test_invalid_spectator_timestamp_and_rows_rejected(self):
  base=spectator_view(Match(2),'playing','Test')
  for bad in (float('nan'),float('inf'),None,'oops'):
   value=dict(base,updated=bad);atomic_json(self.root/'bad.json',value)
   self.assertIsNone(read_feed(self.root/'bad.json'))
  value=dict(base,ranking=[{'rank':1,'player_id':9,'score':0,'lives':3}])
  atomic_json(self.root/'bad.json',value);self.assertIsNone(read_feed(self.root/'bad.json'))

 def test_failed_result_save_survives_leaving_results_and_retries(self):
  a=self.app();a.start();a.match.players[0].score=12345;a.match.over=True
  token=a.session_id
  with patch('cabinet.atomic_json',side_effect=OSError('denied')):
   self.key(a,pg.K_ESCAPE)
  with patch('game.time.monotonic',return_value=a.next_save_retry+1):a.events()
  self.assertIn(token,self.store.recorded)
  self.assertTrue(any(row['score']==12345 for row in self.store.high_scores))

 def test_failed_result_retry_is_throttled_and_snapshot_is_immutable(self):
  a=self.app();a.start();a.match.players[0].score=12345;a.match.over=True
  with patch('cabinet.atomic_json',side_effect=OSError('denied')) as write:
   a.save_result();self.assertEqual(write.call_count,1)
   a.match.players[0].score=0
   for unused in range(10):a.events()
   self.assertEqual(write.call_count,1)
   self.assertEqual(len(a.pending_results),1)
  a.save_result();a.save_result()
  self.assertEqual(len(a.pending_results),0)
  self.assertTrue(any(row['score']==12345 for row in self.store.high_scores))
  self.assertEqual(len(self.store.high_scores),a.match.count)

 def test_invalid_payment_count_rejected(self):
  self.paid(3)
  for count in (-1,0,9,True,'1'):
   with self.assertRaises(ValueError):self.store.pay(count)
  self.assertEqual(self.store.credits,3)

 def test_idle_attract_survives_lost_audio(self):
  a=self.app();a.idle_time=20;pg.mixer.quit();a.run(frames=1)

 def test_idle_attract_actual_draw_and_input_reset(self):
  a=self.app();a.idle_time=20;a.draw();self.assertIsNone(a.match)
  self.key(a,pg.K_h);self.assertEqual(a.idle_time,0);self.assertTrue(a.scores_open);a.draw()

if __name__=='__main__':unittest.main(verbosity=2)

