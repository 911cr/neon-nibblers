import os
os.environ.setdefault('SDL_VIDEODRIVER','dummy')
os.environ.setdefault('SDL_AUDIODRIVER','dummy')
import tempfile
import unittest
import pygame as pg
from game import App,COLORS,PALETTES
from cabinet import CabinetStore


class PaletteProgressionTests(unittest.TestCase):
    def test_automatic_maze_change_retains_hue(self):
        with tempfile.TemporaryDirectory() as path:
            app=App(cabinet=CabinetStore(path));app.theme=2;app.start()
            before=app.wall_palette();old=app.match.arena.map_id
            app.match.dots.clear();app.match.update(1/60)
            self.assertNotEqual(app.match.arena.map_id,old)
            self.assertEqual(app.wall_palette(),before)
            pg.event.post(pg.event.Event(pg.KEYDOWN,key=pg.K_F12))
            app.events();self.assertEqual(app.wall_palette(),3)
            pg.quit()

    def test_station_start_and_override_persist(self):
        with tempfile.TemporaryDirectory() as path:
            app=App(cabinet=CabinetStore(path));app.theme=2;app.station_action(0)
            app.match.new_arena(0);self.assertEqual(app.wall_palette(),2)
            app.palette_override=4;app.match.new_arena(1)
            self.assertEqual(app.wall_palette(),4)
            pg.quit()

    def test_active_giant_colors_cycle_and_expire_without_logic_mutation(self):
        from replay import digest
        with tempfile.TemporaryDirectory() as path:
            app=App(cabinet=CabinetStore(path));app.count=8;app.palette_override=4;app.start()
            g=app.match
            g.players[3].effects['Titan']=7;g.players[7].effects['Titan']=7
            g.elapsed=0;before=digest(g)
            self.assertEqual(app.wall_style(),(('giant',3),COLORS[3]))
            self.assertEqual(digest(g),before)
            g.elapsed=1.25;self.assertEqual(app.wall_style(),(('giant',7),COLORS[7]))
            g.players[7].effects.clear();self.assertEqual(app.wall_style()[1],COLORS[3])
            g.players[3].lives=0;self.assertEqual(app.wall_style(),(4,PALETTES[4]))
            g.players[0].effects['Crown']=7;self.assertEqual(app.wall_style(),(4,PALETTES[4]))
            pg.quit()


if __name__=='__main__':unittest.main()
