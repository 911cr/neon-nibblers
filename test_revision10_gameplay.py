"""Simultaneous-event timing, expiration and ghost-state regression checks."""
import os
os.environ['SDL_VIDEODRIVER']='dummy'
os.environ['SDL_AUDIODRIVER']='dummy'
import unittest
from unittest.mock import patch
from game import App, Match, ITEMS, pg
from replay import FixedStepper, digest, record, replay


class GameplayTimingQA(unittest.TestCase):
    def setup_spark(self,collector):
        g=Match(2,seed=19)
        g.items={(2,1):'Spark'}
        for p in g.players:
            p.entry=p.safe=0;p.clock=g.tuning['player_step_seconds']-1/60
            p.direction=p.wanted=(1,0)
        g.players[collector].pos=(1,1)
        g.players[1-collector].pos=(5,1)
        g.foes[0]=(9,1);g.foe_modes[0]='roaming'
        return g

    def test_lightning_pickup_order_does_not_change_this_ticks_movement(self):
        outcomes=[]
        for collector in (0,1):
            g=self.setup_spark(collector)
            g.update(1/60)
            victim=g.players[1-collector]
            outcomes.append((victim.pos,victim.stun,g.foe_zapped[0]))
        self.assertEqual(outcomes[0],outcomes[1])
        self.assertEqual(outcomes[0],((6,1),2.,2.))

    def test_simultaneous_lightning_pickups_both_complete_and_stun(self):
        g=self.setup_spark(0)
        g.items[(6,1)]='Spark'
        g.update(1/60)
        self.assertEqual([p.pos for p in g.players],[(2,1),(6,1)])
        self.assertEqual([p.stun for p in g.players],[2.,2.])
        self.assertEqual(sum(e['event']=='pickup' for e in g.ledger.events),2)

    def test_timed_effects_expire_on_configured_tick(self):
        from gameplay_tuning import DEFAULT_TUNING
        timed={name:int(seconds) for name,seconds in DEFAULT_TUNING['durations'].items()
               if name not in ('Spark','Quake')}
        for name,seconds in timed.items():
            with self.subTest(power=name):
                g=Match(1,seed=19);p=g.players[0]
                p.stun=p.safe=100;g.items.clear();g.collect(p,name)
                for _ in range(seconds*60-1):g.update(1/60)
                self.assertTrue(g.active(p,name))
                g.update(1/60)
                self.assertFalse(g.active(p,name))
        g=Match(1,seed=19);g.players[0].stun=g.players[0].safe=100
        g.collect(g.players[0],'Quake')
        for _ in range(300):g.update(1/60)
        self.assertEqual(g.quake,0)

    def test_match_timer_and_safety_have_no_positive_float_tail(self):
        g=Match(1,seed=19);p=g.players[0]
        p.stun=100;p.safe=2;g.time=2
        for _ in range(119):g.update(1/60)
        self.assertFalse(g.over);self.assertGreater(p.safe,0)
        g.update(1/60)
        self.assertTrue(g.over);self.assertEqual(g.time,0);self.assertEqual(p.safe,0)
        self.assertEqual(sum(e['event']=='match_end' for e in g.ledger.events),1)

    def test_ghost_targeting_excludes_bays_and_hidden_players(self):
        # This tests the stated adaptation rule, not an imported classic AI.
        g=Match(2,seed=19)
        g.players[0].effects={'Veil':7};g.players[0].pos=(10,1)
        g.players[1].pos=g.arena.spawns[1]
        g.foes[0]=(9,1);g.foe_modes[0]='roaming'
        with patch.object(g.rng,'random',return_value=0) as choose_target:
            for _ in range(30):
                previous=g.foes[0];g.update_foes(g.tuning['ghost_step_seconds'])
                self.assertIn(g.foes[0],g.arena.lanes)
                self.assertNotIn(g.foes[0],g.arena.spawns)
                self.assertIn(g.foes[0],[g.arena.step(previous,d)
                                         for d in ((1,0),(-1,0),(0,1),(0,-1))])
            choose_target.assert_not_called()

    def test_roaming_item_collects_on_stationary_or_stunned_contact(self):
        for stun in (0,1):
            g=Match(1,seed=7);p=g.players[0]
            p.pos=(5,1);p.entry=0;p.safe=100;p.stun=stun
            p.direction=p.wanted=(0,0)
            g.items={(4,1):'Rush'};g.item_directions={(4,1):(1,0)}
            g.item_walk_clock=g.tuning['item_step_seconds']-1/60
            sounds=g.update(1/60)
            self.assertEqual(p.pos,(5,1));self.assertTrue(g.active(p,'Rush'))
            self.assertEqual(p.score,75);self.assertIn('power',sounds)
            self.assertNotIn((5,1),g.items);self.assertNotIn((5,1),g.item_directions)
            self.assertEqual(sum(e['event']=='pickup' for e in g.ledger.events),1)
        # Contact during the final item phase still awards threshold life now.
        g=Match(1,seed=7);p=g.players[0]
        p.pos=(5,1);p.entry=0;p.safe=100;p.stun=1;p.score=9950
        g.items={(4,1):'Rush'};g.item_directions={(4,1):(1,0)}
        g.item_walk_clock=g.tuning['item_step_seconds']-1/60;g.update(1/60)
        self.assertEqual(p.score,10025);self.assertEqual(p.lives,4)
        self.assertTrue(p.bonus_life)

    def test_locator_boundary_and_pause_do_not_change_match_logic(self):
        app=App(simulate_controllers=True)
        try:
            app.match=Match(0,seed=19);app.station_action(7)
            p=app.match.players[7]
            for _ in range(119):app.advance(1/60)
            self.assertGreater(p.locate_remaining,0)
            app.match.paused=True;before=digest(app.match)
            app.advance(10);app.draw()
            self.assertEqual(digest(app.match),before)
            app.match.paused=False;app.advance(1/60)
            self.assertEqual(p.locate_remaining,0)
        finally:pg.quit()

    def test_updated_expiration_remains_deterministic_across_render_groupings(self):
        digests=[]
        for fps in (30,60,144):
            g=self.setup_spark(0)
            g.players[0].effects={'Rush':.7,'Lure':.5}
            stepper=FixedStepper(g)
            for _ in range(3*fps):stepper.advance(1/fps)
            digests.append(digest(g))
        self.assertEqual(len(set(digests)),1)
        document=record(8,3,19,180)
        self.assertEqual(digest(replay(document)),document['final_digest'])


if __name__=='__main__':unittest.main(verbosity=2)
