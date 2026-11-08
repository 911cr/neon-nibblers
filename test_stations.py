"""Adversarial station/lifecycle checks. Synthetic devices are not hardware proof."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
import unittest
from collections import defaultdict
from unittest.mock import patch
import pygame as pg
from game import App, Match
from stations import Phase, StationBindings


class Pad:
    def __init__(self, iid, guid='model', axis=(0,0)):
        self.iid, self.guid, self.axis = iid, guid, axis
    def get_instance_id(self): return self.iid
    def get_guid(self): return self.guid
    def get_numaxes(self): return 2
    def get_numhats(self): return 0
    def get_axis(self, n): return self.axis[n]
    def get_init(self): return True
    def get_attached(self): return True


class Stations(unittest.TestCase):
    def setUp(self):
        self.app=App(simulate_controllers=True)
        pg.event.clear()
    def tearDown(self): pg.quit()
    def key(self, key, mod=0):
        pg.event.post(pg.event.Event(pg.KEYDOWN,key=key,mod=mod))
        self.app.events()

    def test_sparse_p8_joins_first_and_has_only_own_score(self):
        self.key(pg.K_F10)
        g=self.app.match
        self.assertEqual(g.count,1)
        self.assertEqual([p.idx for p in g.players if p.joined],[7])
        self.assertEqual(g.players[7].pos,g.arena.spawns[7])
        self.assertEqual([r['player_id'] for r in g.rankings()],[8])
        self.app.advance(1)
        self.assertFalse(g.over)
        self.assertTrue(all(p.lives==0 for p in g.players[:7]))
        self.app.draw()

    def test_simultaneous_start_buttons_join_every_station_once(self):
        self.app.pads={100+i:Pad(100+i,str(i)) for i in range(8)}
        self.app.bindings.sync(self.app.pads)
        for iid in self.app.pads:
            pg.event.post(pg.event.Event(pg.JOYBUTTONDOWN,instance_id=iid,button=0))
        self.app.events()
        g=self.app.match
        self.assertEqual(g.count,8)
        self.assertEqual(sum(e['event']=='station_join' for e in g.ledger.events),8)
        before=[(p.score,p.lives,p.pos) for p in g.players]
        for i in range(8): self.app.station_action(i)
        self.assertEqual(before,[(p.score,p.lives,p.pos) for p in g.players])
        self.app.draw()

    def test_find_retrigger_expiry_pause_and_guide(self):
        self.key(pg.K_F3)
        p=self.app.match.players[0]
        self.app.advance(.5)
        self.assertAlmostEqual(p.locate_remaining,1.5)
        self.key(pg.K_F3)
        self.assertEqual(p.locate_remaining,self.app.locator_seconds)
        self.key(pg.K_p)
        self.assertEqual(self.app.phase,Phase.PAUSED)
        before=self.app.match.snapshot()
        self.app.advance(2)
        self.key(pg.K_F10)
        self.assertEqual(before,self.app.match.snapshot())
        self.app.draw()
        self.key(pg.K_p)
        self.key(pg.K_F1)
        self.assertEqual(self.app.phase,Phase.GUIDE)
        before=self.app.match.snapshot()
        self.app.advance(2)
        self.key(pg.K_F10)
        self.assertEqual(before,self.app.match.snapshot())
        self.app.draw()
        self.key(pg.K_ESCAPE)
        self.app.advance(2.01)
        self.assertAlmostEqual(p.locate_remaining,0)
        self.assertEqual(self.app.phase,Phase.PLAYING)

    def test_eliminated_station_cannot_reset_score_or_lives(self):
        self.app.count=2; self.app.start()
        g=self.app.match; p=g.players[0]
        p.score=123; p.lives=0
        for _ in range(4): self.app.station_action(0)
        self.assertEqual((p.score,p.lives),(123,0))
        self.assertIs(self.app.match,g)
        self.app.draw()

    def test_results_ties_sparse_restart_and_lobby(self):
        self.app.station_action(7)
        self.app.station_action(2)
        g=self.app.match; g.over=True
        self.assertEqual(self.app.phase,Phase.RESULTS)
        self.assertEqual([r['rank'] for r in g.rankings()],[1,1])
        self.app.draw()
        self.app.station_action(5)
        self.assertIsNot(self.app.match,g)
        self.assertEqual([p.idx for p in self.app.match.players if p.joined],[5])
        self.key(pg.K_ESCAPE)
        self.assertEqual(self.app.phase,Phase.ATTRACT)
        self.app.draw()
        self.key(pg.K_RETURN)
        self.assertEqual(self.app.match.count,self.app.count)

    def test_survivor_assignment_and_unique_reconnection(self):
        b=StationBindings(); devices={10:Pad(10,'A'),20:Pad(20,'B')}
        b.sync(devices)
        self.assertEqual(b.by_instance,{10:0,20:1})
        b.sync({20:devices[20]})
        self.assertEqual(b.by_instance,{20:1})
        b.sync({20:devices[20],30:Pad(30,'A')})
        self.assertEqual(b.by_instance,{20:1,30:0})
        self.app.pads={20:Pad(20,'B',(-1,0)),30:Pad(30,'A',(1,0))}
        self.app.bindings=b; self.app.count=2; self.app.start()
        with patch.object(pg.key,'get_pressed',return_value=defaultdict(bool)):
            self.app.inputs()
        self.assertEqual([p.wanted for p in self.app.match.players],[(1,0),(-1,0)])

    def test_identical_guid_reconnect_requires_explicit_pair(self):
        b=self.app.bindings
        b.sync({10:Pad(10),20:Pad(20)})
        b.sync({20:Pad(20)})
        self.app.pads={20:Pad(20),30:Pad(30)}
        b.sync(self.app.pads)
        self.assertNotIn(30,b.by_instance)
        self.assertEqual(b.by_instance[20],1)
        self.key(pg.K_F3,pg.KMOD_SHIFT)
        pg.event.post(pg.event.Event(pg.JOYBUTTONDOWN,instance_id=30,button=0))
        self.app.events()
        self.assertEqual(b.by_instance,{20:1,30:0})
        self.assertIsNone(self.app.pair_station)
        self.assertIsNone(self.app.match)

    def test_assignment_conflict_does_not_steal_live_station(self):
        b=self.app.bindings; b.sync({10:Pad(10,'A'),20:Pad(20,'B')})
        self.assertFalse(b.bind(20,0,'B'))
        self.assertEqual(b.by_instance,{10:0,20:1})
        self.assertTrue(b.bind(20,7,'B'))
        self.assertEqual(b.by_instance,{10:0,20:7})

    def test_missing_sparse_station_is_not_masked_by_unrelated_device(self):
        self.app.simulate_controllers=False
        self.app.pads={10:Pad(10,'A')}; self.app.bindings.sync(self.app.pads)
        self.app.station_action(7)
        self.assertEqual(self.app.controller_status()['actual'],1)
        self.assertEqual(self.app.controller_status()['missing'],1)
        self.app.bindings.bind(10,7,'A')
        self.assertEqual(self.app.controller_status()['missing'],0)

    def test_render_rates_produce_same_fixed_logic(self):
        states=[]
        for fps in (30,60,144):
            self.app.match=Match(8,seed=300)
            self.app.reset_visuals(); self.app.demo=True
            for _ in range(fps*3): self.app.advance(1/fps)
            states.append(self.app.match.snapshot())
        self.assertEqual(states[0],states[1]); self.assertEqual(states[1],states[2])

    def test_every_player_count_and_map_with_independent_joins(self):
        for theme in range(4):
            for count in range(1,9):
                self.app.match=None; self.app.theme=theme
                order=[7,2,5,0,6,3,1,4][:count]
                for idx in order: self.app.station_action(idx)
                self.app.demo=True; self.app.advance(.5)
                self.assertEqual(self.app.match.count,count)
                self.assertEqual(len(self.app.match.rankings()),count)
                self.assertFalse(self.app.match.over)
                self.app.draw()



    def test_late_join_preserves_existing_clock_scores_and_station(self):
        self.app.station_action(7)
        g=self.app.match; g.time=.04; g.players[7].score=900
        self.app.station_action(0)
        self.assertEqual(g.time,.04)
        self.assertEqual(g.players[7].score,900)
        self.assertEqual(g.players[0].score,0)
        self.assertEqual(g.players[0].pos,g.arena.spawns[0])
        self.app.advance(.05)
        self.assertTrue(g.over)
        self.app.draw()

    def test_two_identical_disconnected_units_do_not_claim_each_other(self):
        b=StationBindings(); b.sync({10:Pad(10),20:Pad(20)})
        b.sync({})
        b.sync({30:Pad(30),40:Pad(40)})
        self.assertEqual(b.by_instance,{})
        self.assertEqual(set(b.reserved),{0,1})
        self.assertTrue(b.bind(40,1,'model'))
        self.assertTrue(b.bind(30,0,'model'))
        self.assertEqual(b.by_instance,{40:1,30:0})

    def test_locator_is_rendered_and_refresh_does_not_create_score(self):
        self.app.station_action(7)
        p=self.app.match.players[7]; p.pos=(17,9); p.entry=0
        seen=[]; original=self.app.text
        def capture(s,*args,**kwargs):
            seen.append(str(s)); return original(s,*args,**kwargs)
        with patch.object(self.app,'text',capture): self.app.draw()
        self.assertIn('P8',seen)
        self.assertEqual(p.score,0)
        self.assertEqual(self.app.match.ledger.totals().get(8),0)
        p.locate_remaining=0; seen.clear()
        with patch.object(self.app,'text',capture): self.app.draw()
        self.assertNotIn('P8',seen)


    def test_double_house_contours_leave_inner_doorway_open(self):
        from game import OX, TOP, TILE, THEMES, center
        for theme in range(4):
            self.app.theme=theme; self.app.count=8; self.app.start(); self.app.draw()
            g=self.app.match; dx,dy,dw,dh=g.arena.den
            left,top=OX+dx*TILE+5,TOP+dy*TILE+5
            accent=THEMES[theme][1]
            self.assertEqual(tuple(self.app.canvas.get_at((left+20,top)))[:3],accent)
            self.assertEqual(tuple(self.app.canvas.get_at((left+20,top+4)))[:3],accent)
            self.assertEqual(tuple(self.app.canvas.get_at((left+20,top-3)))[:3],(0,0,4))
            marks=[tuple(self.app.canvas.get_at((left+20,y)))[:3]==accent for y in range(top-10,top+10)]
            runs=sum(mark and (i==0 or not marks[i-1]) for i,mark in enumerate(marks))
            self.assertEqual(runs,2)
            door_x=center((27,15))[0]
            self.assertEqual(tuple(self.app.canvas.get_at((door_x,top+4)))[:3],(0,0,4))

if __name__=='__main__': unittest.main(verbosity=2)




