"""Independent contact QA: grid rollback/recoil is original, not measured DX physics."""
import os
os.environ['SDL_VIDEODRIVER']='dummy';os.environ['SDL_AUDIODRIVER']='dummy'
import unittest
from game import Match,COLS

class ContactCriticalQA(unittest.TestCase):
    def ready(self,count=2,theme=0):
        g=Match(count,theme,seed=73,tuning={'spawn_seconds':120})
        g.foes=[];g.items={}
        for p in g.players:p.entry=p.safe=0;p.clock=.09;p.effects={}
        return g
    def test_stationary_receiver_recoils_with_incoming_direction(self):
        g=self.ready();p,q=g.players
        p.pos=(10,1);q.pos=(11,1);p.direction=p.wanted=(1,0);q.direction=q.wanted=(0,0)
        g.update(1/60)
        self.assertEqual((p.pos,q.pos),((10,1),(11,1)))
        self.assertEqual(q.recoil,(1,0))
        for _ in range(14):g.update(1/60)
        self.assertEqual(q.pos,(12,1))
        self.assertEqual(q.wanted,(0,0))
    def test_stationary_receiver_uses_tunnel_topology_not_coordinate_sign(self):
        for theme in range(4):
            g=self.ready(theme=theme);p,q=g.players;row=g.arena.portals[0]
            p.pos=(COLS-1,row);q.pos=(0,row)
            p.direction=p.wanted=(1,0);q.direction=q.wanted=(0,0)
            g.update(1/60)
            self.assertEqual((p.pos,q.pos),((COLS-1,row),(0,row)))
            self.assertEqual(q.recoil,(1,0),(theme,q.recoil))
    def test_head_on_tunnel_rolls_back_and_retains_controls(self):
        for theme in range(4):
            g=self.ready(theme=theme);p,q=g.players;row=g.arena.portals[0]
            p.pos=(COLS-1,row);q.pos=(0,row)
            p.direction=p.wanted=(1,0);q.direction=q.wanted=(-1,0)
            g.update(1/60)
            self.assertEqual((p.pos,q.pos),((COLS-1,row),(0,row)))
            self.assertEqual((p.recoil,q.recoil),((-1,0),(1,0)))
            self.assertEqual((p.wanted,q.wanted),((1,0),(-1,0)))
    def test_all_maps_eight_held_players_never_jump_or_share_cell(self):
        for theme in range(4):
            g=self.ready(8,theme)
            for idx,p in enumerate(g.players):
                p.pos=(7+idx*3,1);self.assertIn(p.pos,g.arena.lanes)
                p.direction=p.wanted=(1 if idx<4 else -1,0)
            for _ in range(360):
                before=[p.pos for p in g.players];g.update(1/60)
                self.assertEqual(len({p.pos for p in g.players}),8)
                for p,old in zip(g.players,before):
                    dx=abs(p.pos[0]-old[0]);delta=min(dx,COLS-dx)+abs(p.pos[1]-old[1])
                    self.assertLessEqual(delta,1,(theme,p.idx,old,p.pos))
                    self.assertIn(p.pos,g.arena.floor)
            self.assertTrue(any(e['event']=='player_bump' for e in g.ledger.events))

class RadiusContactQA(unittest.TestCase):
    def test_approaching_normal_and_giant_radius_all_maps(self):
        from player_contacts import approaching_contact
        for theme in range(4):
            for giant,separation in ((False,2),(True,4)):
                g=Match(2,theme,seed=1);p,q=g.players
                p.pos=(11,1);q.pos=(10+separation,1)
                if giant:p.effects=q.effects={'Titan':7}
                before=[(10,1),(10+separation,1)]
                self.assertTrue(approaching_contact(g,p,q,before),(theme,giant))
    def test_following_equal_bodies_do_not_repeatedly_bump(self):
        from player_contacts import approaching_contact
        g=Match(2,seed=1);p,q=g.players
        p.pos=(11,1);q.pos=(12,1)
        self.assertFalse(approaching_contact(g,p,q,[(10,1),(11,1)]))
        self.assertFalse(approaching_contact(g,p,q,[p.pos,q.pos]))
    def test_stationary_growth_is_a_hazard_to_smaller_body(self):
        from player_contacts import approaching_contact
        g=Match(2,seed=1);p,q=g.players
        p.pos=(10,1);q.pos=(12,1)
        before=[p.pos,q.pos]
        self.assertFalse(approaching_contact(g,p,q,before))
        p.effects={'Titan':7}
        self.assertTrue(approaching_contact(g,p,q,before))
    def test_wrap_approach_all_maps_and_private_bay_exclusion(self):
        from player_contacts import approaching_contact
        for theme in range(4):
            g=Match(2,theme,seed=1);p,q=g.players;row=g.arena.portals[0]
            p.pos=(COLS-1,row);q.pos=(0,row)
            self.assertTrue(approaching_contact(g,p,q,[(COLS-2,row),(1,row)]))
            p.pos=g.arena.spawns[0];q.pos=g.arena.entries[0]
            self.assertFalse(approaching_contact(g,p,q,[p.pos,q.pos]))
    def test_parallel_corridors_do_not_collide_through_wall(self):
        from types import SimpleNamespace
        from player_contacts import approaching_contact
        g=Match(2,seed=1);p,q=g.players
        lanes={(0,0),(0,1),(0,2),(1,2),(2,2),(2,1),(2,0)}
        g.arena=SimpleNamespace(lanes=lanes,step=lambda c,d:(c[0]+d[0],c[1]+d[1]))
        p.pos=(0,0);q.pos=(2,0);p.effects={'Titan':7}
        self.assertFalse(approaching_contact(g,p,q,[(0,1),(2,1)]))
    def test_cadence_stationary_target_with_buffered_direction_recoils_outward(self):
        from player_contacts import resolve_bumps
        g=Match(2,seed=1);p,q=g.players
        before=[(10,1),(11,1)];p.pos=q.pos=(11,1)
        p.direction=q.direction=p.wanted=q.wanted=(1,0)
        resolve_bumps(g,[(p,q)],before)
        self.assertEqual((p.recoil,q.recoil),((-1,0),(1,0)))
    def test_integrated_radius_contact_stops_before_visual_overlap_and_growth_hurts(self):
        g=Match(2,seed=1);p,q=g.players;g.foes=[];g.items={}
        p.pos=(10,1);q.pos=(12,1);p.entry=q.entry=p.safe=q.safe=0
        p.direction=p.wanted=(1,0);q.direction=q.wanted=(0,0);p.clock=.09;q.clock=0
        g.update(1/60)
        self.assertEqual((p.pos,q.pos),((10,1),(12,1)))
        self.assertEqual(p.lives,3);self.assertEqual(q.lives,3)
        p.effects={'Titan':7};p.stun=q.stun=0
        g.combat([p.pos,q.pos])
        self.assertEqual(q.lives,2)
        self.assertEqual(q.pos,g.arena.spawns[q.idx])

if __name__=='__main__':unittest.main(verbosity=2)
