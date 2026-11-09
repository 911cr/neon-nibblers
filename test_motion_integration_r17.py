"""Independent rendered integration checks; temporary cabinet stores only."""
import os
os.environ.setdefault('SDL_VIDEODRIVER','dummy')
os.environ.setdefault('SDL_AUDIODRIVER','dummy')
import copy
import tempfile
import unittest
from pathlib import Path
import pygame as pg
from cabinet import CabinetStore
from game import App, center, OX, TOP, TILE, COLS


class MotionIntegration(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(dir=Path.cwd())
        self.app=App(simulate_controllers=True,cabinet=CabinetStore(Path(self.tmp.name)))
        self.app.count=1
        self.app.start()
        self.p=self.app.match.players[0]
        self.p.entry=0

    def tearDown(self):
        pg.quit()
        self.tmp.cleanup()

    def seed(self,cell):
        self.p.pos=cell
        self.app.reset_visuals()
        self.app.draw(0)

    def test_rendered_turn_stays_on_segments_and_does_not_change_match(self):
        a=self.app
        self.seed((10,13))
        self.p.pos=(11,13)
        a.draw(.1)
        self.p.pos=(11,14)
        before=copy.deepcopy(a.match.__dict__)
        a.draw(.1)
        x,y=a.visual_positions[0]
        self.assertEqual(y,center((10,13))[1])
        self.assertLess(x,center((11,13))[0])
        a.draw(.1)
        self.assertEqual(a.visual_positions[0][0],center((11,13))[0])
        self.assertGreater(a.visual_positions[0][1],y)
        # Objects with identity equality (arena, RNG, ledger) are checked by
        # their state rather than comparing the copied enclosing dictionary.
        self.assertEqual(a.match.players,before['players'])
        self.assertEqual(a.match.dots,before['dots'])
        self.assertEqual(a.match.elapsed,before['elapsed'])
        self.assertEqual(a.match.ledger.events,before['ledger'].events)

    def test_pause_freezes_midsegment_and_resume_continues(self):
        a=self.app;self.seed((10,13));self.p.pos=(11,13);a.draw(.1)
        old=dict(a.visual_positions);t=a.animation_time
        self.p.locate_remaining=1
        self.app.match.paused=True
        a.advance(.5);a.draw(.5)
        self.assertEqual(a.visual_positions,old)
        self.assertEqual(a.animation_time,t)
        self.assertEqual(self.p.locate_remaining,1)
        self.app.match.paused=False;a.draw(.1)
        self.assertGreater(a.visual_positions[0][0],old[0][0])

    def test_tunnel_wrap_is_short_and_keeps_row(self):
        a=self.app;y=next(iter(a.match.arena.portals))
        self.seed((COLS-1,y));self.p.pos=(0,y)
        a.draw(.125)
        x,py=a.visual_positions[0]
        self.assertTrue(x>=OX+COLS*TILE-1 or x<=OX+1)
        self.assertEqual(py,center((0,y))[1])
        a.draw(.125)
        self.assertEqual(a.visual_positions[0],center((0,y)))

    def test_death_relocation_and_restart_clear_tracks(self):
        a=self.app;self.seed((29,13));self.p.safe=0
        self.assertTrue(a.match.hurt(self.p));a.draw(.01)
        self.assertEqual(a.visual_positions[0],center(self.p.pos))
        self.assertTrue(a.motion_tracks['players'])
        a.start()
        self.assertTrue(all(not tracks for tracks in a.motion_tracks.values()))
        self.assertFalse(a.visual_positions)

    def test_external_visual_override_is_authoritative(self):
        a=self.app;self.seed((10,13));self.p.pos=(11,13);a.draw(.1)
        a.visual_positions[0]=center((11,13));a.draw(.01)
        self.assertEqual(a.visual_positions[0],center((11,13)))

    def test_actual_app_adapter_rate_independence_no_backlog(self):
        a=self.app
        for hz in (30,60,144):
            a.reset_visuals();old=(OX+100,TOP+100)
            for frame in range(hz*5):
                target=(OX+100+20*(int((frame+1)*4/hz)+1),TOP+100)
                new=a.corridor_position('players',0,old,target,1/hz,.25,False)
                self.assertAlmostEqual(new[0]-old[0],80/hz,places=6)
                self.assertEqual(new[1],TOP+100)
                old=new
            self.assertAlmostEqual(old[0],OX+500,places=6)
            self.assertLessEqual(len(a.motion_tracks['players'][0]._waypoints),2)

    def test_gate_entry_fifty_pixels_finishes_one_interval(self):
        a=self.app;spawn=a.match.arena.spawns[0];entry=a.match.arena.entries[0]
        self.seed(spawn);self.p.pos=entry
        interval=a.match.player_interval(self.p)
        a.draw(interval/2)
        self.assertAlmostEqual(a.visual_positions[0][1],(center(spawn)[1]+center(entry)[1])/2)
        a.draw(interval/2)
        self.assertEqual(a.visual_positions[0],center(entry))

    def test_ghost_item_pause_and_removed_item_track_cleanup(self):
        a=self.app;g=a.match
        g.items={(10,13):'Crown'};g.foes[0]=(10,13)
        a.reset_visuals();a.draw(0)
        g.items={(11,13):'Crown'};g.foes[0]=(11,13)
        a.draw(.05)
        old_items=dict(a.visual_items);old_foes=dict(a.visual_foes)
        self.assertGreater(old_foes[0][0],center((10,13))[0])
        self.assertLess(old_foes[0][0],center((11,13))[0])
        self.assertGreater(next(iter(old_items.values()))[0],center((10,13))[0])
        g.paused=True;a.draw(.5)
        self.assertEqual(old_items,a.visual_items)
        self.assertEqual(old_foes,a.visual_foes)
        g.paused=False;g.items={};a.draw(.01)
        self.assertFalse(a.motion_tracks['items'])
        self.assertFalse(a.visual_items)

    def test_all_player_counts_render_reversal_without_forward_drift(self):
        a=self.app
        for count in (1,2,8):
            a.count=count;a.start()
            for p in a.match.players[:count]:p.pos=(10,13);p.entry=0
            a.draw(0)
            for p in a.match.players[:count]:p.pos=(11,13)
            a.draw(.1)
            for p in a.match.players[:count]:p.pos=(10,13)
            a.draw(.1)
            for p in a.match.players[:count]:
                self.assertEqual(a.visual_positions[p.idx],center((10,13)))


if __name__=='__main__':unittest.main()
