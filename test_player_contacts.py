import os
os.environ.setdefault('SDL_VIDEODRIVER','dummy')
os.environ.setdefault('SDL_AUDIODRIVER','dummy')
import unittest
import math
from game import Match


class PlayerContactTests(unittest.TestCase):
    def match(self, count=2):
        g=Match(count,0,seed=15)
        g.foes=[];g.foe_modes=[];g.items.clear()
        for p in g.players:
            p.entry=0;p.safe=0;p.effects.clear();p.clock=0
        return g

    def test_crossing_rolls_back_without_extra_instant_shove(self):
        g=self.match();p,q=g.players
        p.pos=(10,1);q.pos=(11,1)
        p.direction=p.wanted=(1,0);q.direction=q.wanted=(-1,0)
        g.update(g.tuning['player_step_seconds'])
        self.assertEqual((p.pos,q.pos),((10,1),(11,1)))
        self.assertEqual((p.direction,q.direction),((-1,0),(1,0)))
        # Buffered controls are retained; the first subsequent step still recoils.
        for _ in range(math.ceil((.12+g.tuning['player_step_seconds'])*60)):g.update(1/60)
        self.assertEqual((p.pos,q.pos),((9,1),(12,1)))
        self.assertEqual((p.wanted,q.wanted),((1,0),(-1,0)))
        self.assertEqual([p.lives,q.lives],[3,3])

    def test_crowd_reservation_rolls_back_follower(self):
        g=self.match(3);p,q,r=g.players
        previous=[(10,1),(12,1),(9,1)]
        p.pos=q.pos=(11,1);r.pos=(10,1)
        p.direction=(1,0);q.direction=(-1,0);r.direction=(1,0)
        g.combat(previous)
        self.assertEqual([p.pos for p in g.players],previous)
        self.assertEqual(len({p.pos for p in g.players}),3)

    def test_repeated_contact_does_not_reset_recoil_or_event(self):
        g=self.match();p,q=g.players
        p.pos=q.pos=(10,1);p.direction=(1,0);q.direction=(-1,0)
        prior=[(9,1),(11,1)]
        g.combat(prior)
        p.pos=q.pos=(10,1)
        p.stun=q.stun=.03
        g.combat(prior)
        self.assertEqual(p.stun,.03)
        self.assertEqual(sum(e['event']=='player_bump' for e in g.ledger.events),1)

    def test_all_counts_held_contacts_are_local_and_legal(self):
        for count in (2,4,8):
            g=self.match(count)
            for i,p in enumerate(g.players):
                p.pos=(7+i*3,1)
                p.direction=p.wanted=(1 if i<count//2 else -1,0)
            for tick in range(600):
                before=[p.pos for p in g.players]
                g.update(1/60)
                self.assertEqual(len({p.pos for p in g.players}),count)
                for p,old in zip(g.players,before):
                    self.assertIn(p.pos,g.arena.floor)
                    self.assertLessEqual(abs(p.pos[0]-old[0])+abs(p.pos[1]-old[1]),1)
            self.assertTrue(any(e['event']=='player_bump' for e in g.ledger.events))

    def test_equal_giants_bump_but_giant_eats_small(self):
        g=self.match();p,q=g.players
        p.effects['Titan']=q.effects['Titan']=7
        p.pos=q.pos=(10,1);g.combat([(9,1),(11,1)])
        self.assertEqual([p.lives,q.lives],[3,3])
        q.effects.clear();p.pos=q.pos=(10,1);q.safe=0
        g.combat()
        self.assertEqual(q.lives,2)
        self.assertEqual(p.score,g.score_values['rival_eaten'])

    def test_recoil_clears_on_death_and_stage(self):
        g=self.match();p=g.players[0]
        p.recoil=(1,0);g.hurt(p);self.assertEqual(p.recoil,(0,0))
        p.recoil=(1,0);g.new_arena(1);self.assertEqual(p.recoil,(0,0))

    def test_later_giant_hit_does_not_rollback_respawn(self):
        g=self.match(3);p,q,giant=g.players
        p.pos=q.pos=giant.pos=(10,1);giant.effects['Titan']=7
        g.combat([(9,1),(11,1),(10,1)])
        self.assertEqual(p.pos,g.arena.spawns[0])
        self.assertEqual(q.pos,g.arena.spawns[1])
        self.assertEqual((p.lives,q.lives),(2,2))


if __name__=='__main__':unittest.main()
