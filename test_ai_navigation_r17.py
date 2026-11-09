"""Original bot policy regressions; these do not assert commercial difficulty."""
import unittest
from types import SimpleNamespace
from arcade_ai import choose_direction,DIRECTIONS
from game import Match,Arena

class BotNavigationTests(unittest.TestCase):
    def quiet_match(self,count=1,theme=0):
        g=Match(count,theme,seed=12)
        g.items={};g.dots=set();g.foe_modes=['house']*len(g.foes)
        for p in g.players:p.safe=0;p.entry=0;p.effects={}
        return g
    def test_one_step_tunnel_power_is_local(self):
        g=self.quiet_match();p=g.players[0];p.pos=(0,17)
        g.items={(58,17):'Titan'};g.dots={(1,17)}
        self.assertEqual(choose_direction(g,p,DIRECTIONS),(-1,0))
    def test_titan_hunts_rival_even_with_no_roaming_ghost(self):
        g=self.quiet_match(2);p,q=g.players;p.pos=(10,1);q.pos=(20,1)
        p.effects={'Titan':5};g.dots={(9,1)}
        direction=choose_direction(g,p,DIRECTIONS)
        self.assertEqual(direction,(1,0))
        q.safe=2
        self.assertEqual(choose_direction(g,p,DIRECTIONS),(-1,0))
    def test_empty_refill_fallback_leaves_blocked_direction_and_escapes_giant(self):
        g=self.quiet_match(2);p,q=g.players;p.pos=(10,1);q.pos=(11,1)
        p.wanted=(0,-1);p.direction=(1,0);q.effects={'Titan':5}
        self.assertEqual(choose_direction(g,p,DIRECTIONS),(-1,0))
    def test_unreachable_item_does_not_prevent_dot_collection(self):
        g=self.quiet_match();p=g.players[0];p.pos=(10,1)
        g.items={(10,3):'Heart'};g.dots={(9,1)}
        self.assertNotIn((10,3),g.arena.lanes)
        self.assertEqual(choose_direction(g,p,DIRECTIONS),(-1,0))
    def test_all_counts_all_maps_sustain_legal_navigation(self):
        from game import steer_demo
        for theme in range(4):
            for count in range(1,9):
                g=Match(count,theme,seed=143)
                for tick in range(150):
                    steer_demo(g);g.update(1/30)
                    for p in g.players:
                        self.assertIn(p.pos,g.arena.floor)
                self.assertFalse(g.over)

    def test_all_maps_counts_choose_legal_steps(self):
        for theme in range(4):
            for count in range(1,9):
                g=self.quiet_match(count,theme)
                lanes=sorted(g.arena.lanes)
                for i,p in enumerate(g.players):
                    p.pos=lanes[i*11];p.wanted=(0,0)
                    direction=choose_direction(g,p,DIRECTIONS)
                    self.assertTrue(g.arena.can_enter(g.arena.step(p.pos,direction),p))

if __name__=='__main__':unittest.main()
