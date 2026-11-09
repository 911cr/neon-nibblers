"""Source-supported global ghost tint, separate from protected contact rules."""
import os
os.environ.setdefault('SDL_VIDEODRIVER','dummy');os.environ.setdefault('SDL_AUDIODRIVER','dummy')
import unittest
from unittest.mock import patch
import game

class GhostTintR18(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.app=game.App(simulate_controllers=True)
    @classmethod
    def tearDownClass(cls):game.pg.quit()
    def test_actual_renderer_body_modes_receive_global_tint_all_maps(self):
        for theme in range(4):
            for mode in ('house','leaving','roaming','carried','eyes','entering'):
                g=game.Match(1,theme,seed=18);self.app.match=g;self.app.reset_visuals()
                g.players[0].effects={'Crown':3}
                g.foes=[g.arena.homes[0]];g.foe_modes=[mode];g.foe_zapped=[0]
                with patch.object(game,'foe',wraps=game.foe)as draw:self.app.draw(0)
                self.assertEqual(len(draw.call_args_list),1)
                call=draw.call_args.args
                self.assertEqual(call[6],mode in ('house','leaving','roaming'))
                self.assertEqual(call[7],mode in ('eyes','entering'))
                if mode=='house':
                    x,y=game.center(g.foes[0]);rgb=self.app.canvas.get_at((x,y-10))
                    self.assertGreater(rgb.b,rgb.r*2)
    def test_tunnel_duplicate_uses_same_tint(self):
        g=game.Match(1,0,seed=18);self.app.match=g;self.app.reset_visuals()
        g.players[0].effects={'Titan':3};g.foes=[(0,g.arena.portals[0])];g.foe_modes=['roaming'];g.foe_zapped=[0]
        with patch.object(game,'foe',wraps=game.foe)as draw:self.app.draw(0)
        self.assertEqual(len(draw.call_args_list),2)
        self.assertTrue(all(c.args[6]for c in draw.call_args_list))
    def test_housed_blue_bodies_remain_harmless_and_cannot_be_farmed(self):
        for mode in ('house','leaving'):
            g=game.Match(1,0,seed=18);p=g.players[0];p.effects={'Crown':3};p.safe=0;p.pos=g.arena.exit
            g.foes[0]=p.pos;g.foe_modes[0]=mode;before=(p.lives,p.score)
            g.combat();self.assertEqual((p.lives,p.score),before);self.assertEqual(g.foe_modes[0],mode)
    def test_no_living_hunter_keeps_normal_house_colors(self):
        for dead in (False,True):
            g=game.Match(1,0,seed=18);self.app.match=g;self.app.reset_visuals()
            g.players[0].effects={'Crown':3}if dead else {};g.players[0].lives=0 if dead else 3
            with patch.object(game,'foe')as draw:self.app.draw(0)
            self.assertTrue(all(not c.args[6]for c in draw.call_args_list))

if __name__=='__main__':unittest.main()
