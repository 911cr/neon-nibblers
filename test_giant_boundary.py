import math
import os
import unittest
from unittest.mock import patch

os.environ.setdefault('SDL_VIDEODRIVER','dummy')
os.environ.setdefault('SDL_AUDIODRIVER','dummy')
import game
from player_contacts import giant_contact


class GiantBoundary(unittest.TestCase):
    def prepare(self,theme=0):
        g=game.Match(2,theme,seed=42)
        g.items.clear();g.foes.clear()
        for p,pos in zip(g.players,[(14,1),(16,2)]):
            p.pos=pos;p.stun=2;p.entry=p.safe=0
        g.players[0].effects['Titan']=6
        return g

    def test_euclidean_miss_at_open_corner_and_single_award(self):
        g=self.prepare();p,q=g.players
        self.assertAlmostEqual(math.dist(*[g.body_circle(a)[0] for a in (p,q)]),math.sqrt(2000))
        self.assertTrue(giant_contact(g,p,q))
        g.combat();g.combat()
        self.assertEqual(q.lives,2)
        self.assertEqual([e['event'] for e in g.ledger.events].count('rival_eaten'),1)
        self.assertEqual(p.score,g.score_values['rival_eaten'])

    def test_subpixel_before_at_after_and_tunnel_seam(self):
        for theme in range(4):
            g=self.prepare(theme);p,q=g.players
            p.pos=(10,1);q.pos=(13,1)
            for dx,expected in [(53.01,False),(53,True),(52.99,True)]:
                g.body_circle=lambda a: ((210,30),36) if a is p else ((210+dx,30),17)
                self.assertEqual(giant_contact(g,p,q),expected)
            del g.body_circle
            row=g.arena.portals[0]
            p.pos=(0,row);q.pos=(game.COLS-2,row)
            self.assertTrue(giant_contact(g,p,q))
            q.pos=(game.COLS-3,row)
            self.assertFalse(giant_contact(g,p,q))

    def test_exact_rendered_growth_boundary_at_30_60_144_hz(self):
        app=game.App()
        self.addCleanup(game.pg.quit)
        ticks=[]
        for hz in (30,60,144):
            g=self.prepare();app.match=g;app.reset_visuals()
            p,q=g.players
            visible=[]
            while q.lives==3 and g.elapsed<.4:
                app.advance(1/hz)
                with patch.object(game,'muncher',wraps=game.muncher) as sprite:
                    app.draw(1/hz)
                if q.lives==3 and g.tick:
                    circles=[]
                    for a in (p,q):
                        call=next(c.args for c in sprite.call_args_list if c.args[2]==game.COLORS[a.idx])
                        point,r=g.body_circle(a)
                        self.assertEqual(call[1],(round(game.OX+point[0]),round(game.TOP+point[1])))
                        self.assertEqual(call[5],r)
                        circles.append((point,r))
                    gap=math.dist(circles[0][0],circles[1][0])-sum(r for _,r in circles)
                    self.assertGreater(gap,0)
                    visible.append(gap)
            self.assertTrue(visible)
            self.assertEqual(q.lives,2)
            ticks.append(next(e['tick'] for e in g.ledger.events if e['event']=='rival_eaten'))
        self.assertEqual(len(set(ticks)),1)

    def test_protection_then_expiry_and_giant_vs_giant(self):
        g=self.prepare();p,q=g.players
        q.safe=.5
        for _ in range(24):g.update(1/60)
        self.assertEqual(q.lives,3)
        self.assertTrue(giant_contact(g,p,q))
        for _ in range(7):g.update(1/60)
        self.assertEqual(q.lives,2)
        g=self.prepare();p,q=g.players;q.effects['Titan']=5
        for _ in range(30):g.update(1/60)
        self.assertEqual([p.lives,q.lives],[3,3])
