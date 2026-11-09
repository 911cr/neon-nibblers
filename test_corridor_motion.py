import unittest
from corridor_motion import CorridorTrack


class CorridorMotionTests(unittest.TestCase):
    def test_constant_speed_at_three_refresh_rates(self):
        for hz in (30, 60, 144):
            with self.subTest(hz=hz):
                track = CorridorTrack((0,0))
                for frame in range(hz):
                    # Logical targets arrive one cell ahead of presentation.
                    target = (20 * (int((frame+1)*4/hz) + 1), 0)
                    track.sample(target, 1/hz, 80)
                self.assertAlmostEqual(track.position[0],80,places=5)
                self.assertEqual(track.position[1],0)

    def test_ordered_corner_never_cuts_diagonal(self):
        track = CorridorTrack((0,0))
        self.assertEqual(track.sample((20,0),.1,100),(10,0))
        self.assertEqual(track.sample((20,20),.1,100),(20,0))
        self.assertEqual(track.sample((20,20),.1,100),(20,10))
        self.assertEqual(track.sample((20,20),.1,100),(20,20))

    def test_reversal_cancels_forward_endpoint(self):
        track = CorridorTrack((0,0))
        track.sample((20,0),.05,100)
        self.assertEqual(track.sample((0,0),.02,100),(3,0))
        self.assertEqual(track.sample((0,0),1,100),(0,0))

    def test_reversal_trims_queued_corner_without_cutting(self):
        track = CorridorTrack((0,0))
        track.sample((20,0),.01,100)
        track.sample((20,20),.01,100)
        self.assertEqual(track.sample((20,0),.1,100),(12,0))
        self.assertEqual(track.sample((20,0),1,100),(20,0))

    def test_wrap_uses_short_horizontal_route(self):
        for start, end, expected in ((1170,10,1180),(10,1170,0)):
            track = CorridorTrack((start,30))
            pos=track.sample((end,30),.1,100,(1180,None))
            self.assertAlmostEqual(pos[0],expected % 1180)
            self.assertEqual(pos[1],30)
            self.assertEqual(track.sample((end,30),.1,100,(1180,None)),(end,30))

    def test_wrap_then_corner_stays_on_path(self):
        track=CorridorTrack((1170,30))
        track.sample((10,30),.05,100,(1180,None))
        self.assertEqual(track.sample((10,50),.15,100,(1180,None)),(10,30))
        self.assertEqual(track.sample((10,50),.1,100,(1180,None)),(10,40))

    def test_teleport_diagonal_and_large_jump_snap(self):
        for target in ((20,20),(80,0)):
            track=CorridorTrack((0,0))
            self.assertEqual(track.sample(target,.01,10),target)
            self.assertEqual(track.sample(target,1,10),target)

    def test_gate_entry_and_no_overshoot(self):
        track=CorridorTrack((10,0))
        self.assertEqual(track.sample((10,50),.1,100),(10,10))
        self.assertEqual(track.sample((10,50),5,100),(10,50))

    def test_pause_ignores_target_and_resume_processes_it(self):
        track=CorridorTrack((0,0))
        self.assertEqual(track.sample((20,0),0,100),(0,0))
        self.assertEqual(track.sample((20,0),.1,100),(10,0))
        self.assertEqual(track.sample((20,20),0,100),(10,0))
        self.assertEqual(track.sample((20,20),.1,100),(20,0))

    def test_explicit_reset_clears_old_queue(self):
        track=CorridorTrack((0,0));track.sample((20,0),.01,100)
        track.reset((100,100))
        self.assertEqual(track.sample((100,100),.5,100),(100,100))

    def test_zero_speed_holds_and_target_inputs_unchanged(self):
        target=[20,0];track=CorridorTrack((0,0))
        self.assertEqual(track.sample(target,1,0),(0,0))
        self.assertEqual(target,[20,0])
        self.assertEqual(track.sample(target,.1,100),(10,0))


if __name__=='__main__': unittest.main()

