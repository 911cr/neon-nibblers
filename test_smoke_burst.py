import os
os.environ.setdefault('SDL_VIDEODRIVER','dummy')
os.environ.setdefault('SDL_AUDIODRIVER','dummy')
import unittest
from game import Match


class SmokeBurstTests(unittest.TestCase):
    def test_stationary_pickup_emits_smoke_and_slows_local_ghost(self):
        g=Match(1,seed=15);p=g.players[0]
        p.pos=(10,1);p.entry=0;p.direction=p.wanted=(0,0)
        g.items.clear();g.foes=[(11,1),(30,1)]
        g.foe_previous=list(g.foes);g.foe_modes=['roaming']*2
        g.foe_release=[0.]*2;g.foe_ticks=[0.]*2;g.foe_zapped=[0.]*2
        g.collect(p,'Mist')
        self.assertEqual(g.smoke[p.pos],g.tuning['smoke_seconds'])
        g.update_foes(.16)
        self.assertEqual(g.foes[0],(11,1))
        self.assertNotEqual(g.foes[1],(30,1))

    def test_burst_refresh_and_expiry_follow_tuning(self):
        g=Match(1,seed=15,tuning={'smoke_seconds':.1});p=g.players[0]
        p.pos=(10,1);p.entry=0;p.direction=p.wanted=(0,0)
        g.foes=[];g.foe_modes=[];g.items.clear()
        g.collect(p,'Mist');g.update(.05)
        self.assertAlmostEqual(g.smoke[p.pos],.05)
        g.collect(p,'Mist');self.assertEqual(g.smoke[p.pos],.1)
        p.effects.clear();g.update(.1);self.assertNotIn(p.pos,g.smoke)


if __name__=='__main__':unittest.main()
