"""Exercise real SDL joystick handles and cabinet ownership across processes."""
import ctypes
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
import pygame as pg
from cabinet import cabinet_session
from game import App


class ReleaseReliability(unittest.TestCase):
    def test_second_game_cannot_open_same_profile_and_crash_releases_it(self):
        with tempfile.TemporaryDirectory() as folder:
            program = ('from cabinet import cabinet_session\n'
                       'import sys, time\n'
                       'with cabinet_session(sys.argv[1]) as store:\n'
                       '    assert store.add_credit()\n'
                       '    print("ready", flush=True)\n'
                       '    time.sleep(60)')
            child = subprocess.Popen([sys.executable, '-c', program, folder],
                                     stdout=subprocess.PIPE, text=True,
                                     cwd=Path(__file__).resolve().parent)
            try:
                self.assertEqual(child.stdout.readline().strip(), 'ready')
                with self.assertRaises(BlockingIOError), cabinet_session(folder):
                    self.fail('A second cabinet opened the same save folder')
                with cabinet_session(Path(folder) / 'other') as other:
                    self.assertEqual(other.credits, 0)
            finally:
                child.kill()
                child.communicate(timeout=10)
            with cabinet_session(folder) as reopened:
                self.assertEqual(reopened.credits, 1)

    def test_virtual_device_start_and_disconnect_in_menus(self):
        package = Path(pg.__file__).resolve().parent
        candidates = ([package / 'SDL2.dll'] if os.name == 'nt' else
                      list(package.parent.glob('pygame*.libs/libSDL2-2*.so*')))
        if not candidates or not candidates[0].exists():
            self.skipTest('No bundled SDL2 library found for virtual devices')
        sdl = ctypes.CDLL(str(candidates[0]))
        pg.init()
        self.addCleanup(pg.quit)
        baseline = pg.joystick.get_count()
        for menu in ('operator_open', 'name_entry'):
            idx = sdl.SDL_JoystickAttachVirtual(1, 2, 4, 1)
            self.assertGreaterEqual(idx, 0)
            app = App()
            self.assertEqual(len(app.pads), baseline + 1)
            app.events()
            setattr(app, menu, True)
            self.assertEqual(sdl.SDL_JoystickDetachVirtual(idx), 0)
            app.events()
            self.assertEqual(len(app.pads), baseline)
            self.assertTrue(app.controller_status()['disconnected'])

    def test_enumeration_recovers_when_device_disappears_before_open(self):
        app = App()
        self.addCleanup(pg.quit)
        with patch.object(pg.joystick, 'get_count', return_value=1), \
                patch.object(pg.joystick, 'Joystick', side_effect=pg.error('disconnected')):
            app.refresh_pads()
        self.assertEqual(app.pads, {})
