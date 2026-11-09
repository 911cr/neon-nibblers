"""Original ghost navigation correctness; no commercial algorithm asserted."""
import os
os.environ['SDL_VIDEODRIVER']='dummy'
os.environ['SDL_AUDIODRIVER']='dummy'
import unittest
from unittest.mock import patch
from game import Match, DIRS, COLS


class GhostNavigation(unittest.TestCase):
    def ghost(self,game,position):
        game.foes=[position];game.foe_previous=[position]
        game.foe_modes=['roaming'];game.foe_release=[0]
        game.foe_ticks=[0];game.foe_zapped=[0]

    def test_chase_uses_path_around_wall_instead_of_two_cell_oscillation(self):
        game=Match(1,seed=3)
        route=[(0,0),(0,1),(0,2),(1,2),(2,2),(2,1),(2,0)]
        game.arena.lanes=set(route);game.arena.portals=()
        game.players[0].pos=route[-1];self.ghost(game,route[0])
        self.assertEqual(game.lane_distances(route[-1])[route[0]],6)
        with patch.object(game.rng,'random',return_value=0):
            for expected in route[1:]:
                game.update_foes(.16);self.assertEqual(game.foes[0],expected)

    def test_chase_uses_shorter_tunnel_route_all_maps(self):
        for theme in range(4):
            game=Match(1,theme,seed=3);row=game.arena.portals[0]
            game.players[0].pos=(COLS-1,row);self.ghost(game,(1,row))
            self.assertEqual(game.lane_distances((COLS-1,row))[(1,row)],2)
            with patch.object(game.rng,'random',return_value=0):
                game.update_foes(.16);self.assertEqual(game.foes[0],(0,row))
                game.update_foes(.16);self.assertEqual(game.foes[0],(COLS-1,row))

    def test_frightened_route_increases_legal_distance(self):
        game=Match(1,seed=3)
        game.arena.lanes={(x,1) for x in range(7)};game.arena.portals=()
        game.players[0].pos=(1,1);game.players[0].effects={'Crown':7}
        self.ghost(game,(3,1))
        with patch.object(game.rng,'random',return_value=0):game.update_foes(.16)
        self.assertEqual(game.foes[0],(4,1))

    def test_random_wandering_does_not_immediately_reverse_with_alternatives(self):
        for theme in range(4):
            game=Match(1,theme,seed=3)
            game.players[0].effects={'Veil':100}
            start=sorted(game.arena.lanes)[20]
            self.ghost(game,start);previous=None
            for _ in range(60):
                old=game.foes[0]
                options=[game.arena.step(old,d) for d in DIRS
                         if game.arena.step(old,d) in game.arena.lanes]
                game.update_foes(.16)
                self.assertIn(game.foes[0],options)
                if previous is not None and len(options)>1:self.assertNotEqual(game.foes[0],previous)
                previous=old

    def test_dead_end_can_reverse_and_unreachable_goal_is_empty(self):
        game=Match(1,seed=3);game.arena.lanes={(0,1),(1,1)};game.arena.portals=()
        self.ghost(game,(1,1));game.foe_previous=[(0,1)]
        game.players[0].pos=game.arena.spawns[0]
        game.update_foes(.16);self.assertEqual(game.foes[0],(0,1))
        self.assertEqual(game.lane_distances((99,99)),{})


if __name__=='__main__':unittest.main(verbosity=2)
