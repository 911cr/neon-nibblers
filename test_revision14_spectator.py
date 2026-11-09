"""A failed spectator image export must not crash the arcade session."""
import os
os.environ['SDL_VIDEODRIVER']='dummy';os.environ['SDL_AUDIODRIVER']='dummy'
from pathlib import Path
import tempfile,unittest
from unittest.mock import patch
import pygame as pg
from game import App
from cabinet import CabinetStore

class SpectatorExport(unittest.TestCase):
    def test_image_io_failure_is_visible_and_play_continues(self):
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as folder:
            app=App(simulate_controllers=True,cabinet=CabinetStore(folder))
            app.count=1;app.demo=True;app.start();app.spectator_path=Path(folder)/'feed.json'
            app.publish_clock=1
            with patch.object(pg.image,'save',side_effect=pg.error('Cannot write image')):
                app.run(frames=3)
            self.assertIn('could not be saved',app.status_notice)
            self.assertFalse(app.match.over)
            self.assertGreater(app.match.tick,0)

if __name__=='__main__':unittest.main(verbosity=2)
