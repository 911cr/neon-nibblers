"""A new layout must not perform expensive first-time contour work mid-match."""
import os
os.environ['SDL_VIDEODRIVER']='dummy'
os.environ['SDL_AUDIODRIVER']='dummy'
import unittest
from unittest.mock import patch
import game
from replay import digest

class MazePreparation(unittest.TestCase):
    def tearDown(self):game.pg.quit()

    def test_quick_start_prepares_every_map_without_advancing_time(self):
        app=game.App(simulate_controllers=True);app.seed=7;app.count=8;app.start()
        g=app.match
        self.assertEqual((g.tick,g.elapsed,g.stage),(0,0,1))
        for theme in range(4):
            arena=game.Arena(theme)
            self.assertIn((arena.map_id,arena.map_revision,app.wall_style()[0]),app.backgrounds)
        before=digest(g)
        with patch.object(game,'maze_background',side_effect=AssertionError('unexpected rebuild')):
            app.prepare_mazes()
            for theme in range(4):
                g.transition_arena(theme);app.draw(0)
        self.assertEqual(g.elapsed,0)

    def test_independent_first_station_prepares_maps_and_keeps_identity(self):
        app=game.App(simulate_controllers=True);app.station_action(7)
        self.assertTrue(app.match.players[7].joined)
        self.assertEqual(app.match.count,1)
        self.assertEqual(app.match.tick,0)
        self.assertEqual(len(app.backgrounds),4)

if __name__=='__main__':unittest.main()
