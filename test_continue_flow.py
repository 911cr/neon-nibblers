"""Original continue-window state machine; no physical coin/controller claims."""
import math
import unittest
from cabinet_flow import ContinueOffers

class ContinueOfferTests(unittest.TestCase):
    def test_eight_independent_offers_accept_once_and_do_not_refresh(self):
        flow=ContinueOffers(15,delay=0)
        for idx in range(8):self.assertTrue(flow.open(idx))
        flow.advance(4)
        self.assertFalse(flow.open(3));self.assertEqual(flow.remaining(3),11)
        self.assertTrue(flow.accept(3));self.assertFalse(flow.accept(3))
        self.assertTrue(flow.active)
        self.assertEqual(flow.advance(11),[0,1,2,4,5,6,7])
        self.assertFalse(flow.active)
        self.assertFalse(flow.can_accept(3))

    def test_exact_boundary_30_60_144_and_no_early_expiry(self):
        for hz in (30,60,144):
            flow=ContinueOffers(15,delay=0);flow.open(7)
            for _ in range(15*hz-1):self.assertEqual(flow.advance(1/hz),[])
            self.assertTrue(flow.can_accept(7))
            self.assertAlmostEqual(flow.remaining(7),1/hz)
            self.assertEqual(flow.advance(1/hz),[7])
            self.assertFalse(flow.accept(7))
            self.assertEqual(flow.remaining(7),0)

    def test_staggered_deaths_and_new_offer_after_accepted_continue(self):
        flow=ContinueOffers(15,delay=0);flow.open(0);flow.advance(5);flow.open(1)
        self.assertEqual(flow.advance(10),[0]);self.assertEqual(flow.remaining(1),5)
        self.assertTrue(flow.accept(1));self.assertTrue(flow.open(1))
        self.assertEqual(flow.remaining(1),15)
        self.assertEqual(flow.advance(100),[1])

    def test_zero_disables_and_snapshot_is_detached_stable(self):
        flow=ContinueOffers(0)
        self.assertFalse(flow.open(0));self.assertFalse(flow.active)
        flow=ContinueOffers(15,delay=0);flow.open(7);flow.open(0)
        before=flow.snapshot();before['offers'][0][1]=999
        self.assertEqual(flow.remaining(0),15)
        self.assertEqual(flow.snapshot()['offers'],[[0,15,0],[7,15,0]])
        flow.advance(0);self.assertEqual(flow.snapshot()['offers'],[[0,15,0],[7,15,0]])
        flow.clear();self.assertFalse(flow.active)

    def test_pending_death_delay_and_split_tick_leave_full_window(self):
        flow=ContinueOffers(seconds=10,delay=1)
        flow.open(0);self.assertTrue(flow.active);self.assertTrue(flow.pending(0))
        self.assertFalse(flow.can_accept(0));self.assertFalse(flow.accept(0))
        flow.advance(.75);self.assertEqual(flow.remaining(0),10)
        flow.advance(.5);self.assertFalse(flow.pending(0));self.assertAlmostEqual(flow.remaining(0),9.75)
        self.assertTrue(flow.can_accept(0));self.assertEqual(flow.advance(9.75),[0])

    def test_pending_and_ready_exact_boundary_across_frame_rates(self):
        for hz in (30,60,144):
            flow=ContinueOffers();flow.open(7)
            for _ in range(hz-1):flow.advance(1/hz)
            self.assertTrue(flow.pending(7));self.assertFalse(flow.accept(7))
            flow.advance(1/hz)
            self.assertFalse(flow.pending(7));self.assertTrue(flow.can_accept(7))
            self.assertAlmostEqual(flow.remaining(7),10)
            for _ in range(10*hz-1):self.assertEqual(flow.advance(1/hz),[])
            self.assertEqual(flow.advance(1/hz),[7])
        for value in (True,None,'1',-1,6,math.inf,math.nan):
            with self.assertRaises(ValueError):ContinueOffers(delay=value)

    def test_bad_types_values_rejected_without_mutating_state(self):
        for value in (True,False,None,'15',-1,61,math.inf,math.nan):
            with self.subTest(value=value),self.assertRaises(ValueError):ContinueOffers(value)
        flow=ContinueOffers();flow.open(0);before=flow.snapshot()
        for value in (True,None,'1',-1,math.inf,math.nan):
            with self.assertRaises(ValueError):flow.advance(value)
            self.assertEqual(flow.snapshot(),before)
        for idx in (True,False,None,'1',1.,-1,8):
            for method in (flow.open,flow.remaining,flow.can_accept,flow.accept):
                with self.assertRaises(ValueError):method(idx)
                self.assertEqual(flow.snapshot(),before)

if __name__=='__main__':unittest.main(verbosity=2)
