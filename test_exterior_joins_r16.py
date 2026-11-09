"""Actual frame-to-gate continuity; original geometry, not commercial timing."""
import os
os.environ['SDL_VIDEODRIVER']='dummy'
os.environ['SDL_AUDIODRIVER']='dummy'
import unittest
from unittest.mock import patch
import game
from gate_art import draw_station_gate,gate_geometry


class ExteriorJoins(unittest.TestCase):
    def test_actual_all_maps_palettes_eight_gate_shoulders(self):
        app=game.App(simulate_controllers=True)
        try:
            app.count=8
            for theme in range(4):
                for palette,accent in enumerate(game.PALETTES):
                    app.theme=theme;app.palette_override=palette;app.start()
                    with patch.object(game,'muncher'):app.draw(0)
                    for spawn in app.match.arena.spawns:
                        sx=game.center(spawn)[0];upper=spawn[1]==0
                        ys=(game.TOP+1,game.TOP+7) if upper else (game.TOP+game.ROWS*game.TILE-8,game.TOP+game.ROWS*game.TILE-2)
                        for side in (-1,1):
                            for y in ys:
                                values=[sum(app.canvas.get_at((sx+side*x,y))[:3]) for x in range(39,49)]
                                self.assertGreater(min(values),sum(accent),(theme,palette,spawn,side,y))
                                self.assertLess(max(values)-min(values),20,(theme,palette,spawn,side,y,values))
                            midpoint=sum(ys)//2
                            for x in (sx+side*40,sx+side*46):
                                self.assertLess(sum(app.canvas.get_at((x,midpoint))[:3]),sum(app.canvas.get_at((x,ys[0]))[:3])*.8)
        finally:game.pg.quit()

    def test_pocket_parallel_core_spacing_and_patch_clip(self):
        for accent in game.PALETTES:
            for upper in (False,True):
                s=game.pg.Surface((240,220));s.fill((0,0,4))
                clip=game.pg.Rect(10,10,220,200);s.set_clip(clip)
                draw_station_gate(s,120,110,upper,accent,True)
                self.assertEqual(s.get_clip(),clip)
                y=90 if upper else 130
                for side in (-1,1):
                    values={x:sum(s.get_at((120+side*x,y))[:3]) for x in range(24,35)}
                    peaks=sorted(values,key=values.get,reverse=True)[:2]
                    self.assertEqual(sorted(peaks),[26,32])
                    self.assertLess(values[29],min(values[26],values[32])*.8)
                # Beyond the replacement region remains untouched.
                rect=gate_geometry(120,110,upper)['clear']
                self.assertEqual(tuple(s.get_at((rect.left-1,110)))[:3],(0,0,4))


if __name__=='__main__':unittest.main(verbosity=2)
