"""Ghost faces follow actual rendered travel, including tunnels and corners."""
import os
os.environ.setdefault('SDL_VIDEODRIVER','dummy')
os.environ.setdefault('SDL_AUDIODRIVER','dummy')
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path
import game
from cabinet import CabinetStore
from corridor_motion import CorridorTrack


class GhostFacing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp=tempfile.TemporaryDirectory(dir=Path.cwd())
        cls.app=game.App(simulate_controllers=True,cabinet=CabinetStore(cls.temp.name))
        cls.app.cabinet.settings['fill_bots']=False
        cls.app.start()

    @classmethod
    def tearDownClass(cls):
        game.pg.quit();cls.temp.cleanup()

    def seed(self,cell,theme=0):
        a=self.app
        a.match=game.Match(1,theme,seed=18)
        a.match.foes=[cell];a.match.foe_modes=['roaming']
        a.match.foe_zapped=[0];a.reset_visuals()
        a.draw(0)

    def draw_looks(self,dt):
        with patch.object(game,'foe') as draw:
            self.app.draw(dt)
        return [call.args[5] for call in draw.call_args_list]

    def test_both_tunnel_directions_and_twins_all_maps(self):
        for theme in range(4):
            for row in game.Arena(theme).portals:
                for start,end,expected in ((0,game.COLS-1,(-1,0)),
                                            (game.COLS-1,0,(1,0))):
                    with self.subTest(theme=theme,row=row,start=start):
                        self.seed((start,row),theme)
                        self.app.match.foes[0]=(end,row)
                        looks=self.draw_looks(.1)
                        self.assertGreaterEqual(len(looks),2)
                        self.assertTrue(all(look==expected for look in looks),looks)

    def test_queued_corner_faces_current_segment_not_future_target(self):
        self.seed((10,13),3)
        self.app.match.foes[0]=(11,13)
        self.assertEqual(self.draw_looks(.1),[(1,0)])
        self.app.match.foes[0]=(11,14)
        self.assertEqual(self.draw_looks(.1),[(1,0)])
        self.assertEqual(self.app.visual_foes[0][1],game.center((10,13))[1])
        self.assertEqual(self.draw_looks(.25),[(0,1)])

    def test_stopped_and_paused_faces_retain_last_travel(self):
        self.seed((10,1))
        self.app.match.foes[0]=(11,1)
        self.assertEqual(self.draw_looks(.4),[(1,0)])
        self.assertEqual(self.draw_looks(.1),[(1,0)])
        self.app.match.paused=True
        self.assertEqual(self.draw_looks(.2),[(1,0)])
        self.app.reset_visuals()
        self.assertEqual(self.draw_looks(0),[(0,0)])

    def test_motion_facing_uses_last_segment_and_resets_on_relocation(self):
        track=CorridorTrack((0,0))
        track.sample((20,0),.1,50)
        track.sample((20,20),.4,50)
        self.assertEqual(track.position,(20,5))
        self.assertEqual(track.direction,(0,1))
        track.sample((200,200),.1,50)
        self.assertEqual(track.direction,(0,0))


if __name__=='__main__':unittest.main()
