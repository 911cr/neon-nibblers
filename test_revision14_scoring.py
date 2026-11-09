"""Pickup legend mapping from the observed DX instruction screen.

Only ordinary dots, yellow Gold and green Giant awards are supported here;
other item and combat values remain independently authored estimates.
"""
import os
os.environ['SDL_VIDEODRIVER']='dummy'
os.environ['SDL_AUDIODRIVER']='dummy'
import unittest
from game import Match,ITEMS

class RecoveredScoring(unittest.TestCase):
    def test_distinct_gold_giant_and_other_item_awards(self):
        for name in ITEMS:
            g=Match(1,seed=7);p=g.players[0]
            g.collect(p,name)
            expected=100 if name=='Crown' else 1000 if name=='Titan' else 75
            self.assertEqual(p.score,expected,name)
            events=[e for e in g.ledger.events if e['event']=='pickup']
            self.assertEqual(len(events),1)
            self.assertEqual(events[0]['delta'],expected)
            self.assertEqual(events[0]['context']['score_rule'],
                             'gold_pickup' if name=='Crown' else 'giant_pickup' if name=='Titan' else 'pickup')
            self.assertEqual(g.ledger.totals()[1],expected)

    def test_profile_override_is_specific_and_bonus_awarded_once(self):
        g=Match(1,seed=7,score_values={'gold_pickup':123,'giant_pickup':456,'pickup':12},
                rules={'bonus_threshold':500})
        p=g.players[0]
        for name in ('Crown','Titan','Rush'):g.collect(p,name)
        g.award_score_lives();g.award_score_lives()
        self.assertEqual(p.score,591);self.assertEqual(p.lives,4)
        self.assertEqual(sum(e['event']=='score_bonus_life' for e in g.ledger.events),1)
        self.assertEqual(g.ledger.totals()[1],591)

if __name__=='__main__':unittest.main(verbosity=2)
