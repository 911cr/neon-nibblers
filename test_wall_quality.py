"""Photometric wall regressions: trace brightness, not exact palette pixels."""
import math
import os
import statistics
import unittest
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
import pygame as pg
from arcade_art import maze_background, maze_wall_mask, neon_sprite
from game import Arena


def luminance(color):
    return .2126*color[0]+.7152*color[1]+.0722*color[2]


def trace_energy(image, mask):
    groups = {'horizontal': [], 'vertical': [], 'curve': [], 'frame': []}
    width, height = image.get_size()
    for component in mask.connected_components(40):
        points = component.outline(2)
        for k, (x, y) in enumerate(points):
            if k % 2:
                continue
            previous, following = points[(k-2) % len(points)], points[(k+2) % len(points)]
            dx, dy = following[0]-previous[0], following[1]-previous[1]
            length = math.hypot(dx, dy)
            if not length:
                continue
            group = ('frame' if x < 12 or x > width-13 or y < 12 or y > height-13 else
                     'horizontal' if abs(dx) > 4*abs(dy) else
                     'vertical' if abs(dy) > 4*abs(dx) else 'curve')
            nx, ny = -dy/length, dx/length
            energy = 0
            for j in range(-14, 15):
                xx, yy = x+nx*j/4, y+ny*j/4
                if not (0 <= xx < width-1 and 0 <= yy < height-1):
                    continue
                x0, y0 = int(xx), int(yy)
                fx, fy = xx-x0, yy-y0
                energy += sum(luminance(image.get_at((x0+ox, y0+oy)))*weight
                              for ox, oy, weight in ((0,0,(1-fx)*(1-fy)),
                                  (1,0,fx*(1-fy)), (0,1,(1-fx)*fy), (1,1,fx*fy)))/4
            groups[group].append(energy)
    return groups


class WallQualityTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): pg.init()

    @classmethod
    def tearDownClass(cls): pg.quit()

    def test_all_map_straights_curves_and_frames_have_consistent_trace_energy(self):
        for index in range(4):
            arena = Arena(index)
            mask = maze_wall_mask(arena.space, 59, 31, 20, 26)
            image = maze_background(arena.space, 59, 31, 20, (74,91,255), 26)
            groups = trace_energy(image, mask)
            means = {name: statistics.mean(values) for name, values in groups.items()}
            with self.subTest(map=index):
                self.assertLess(abs(means['curve']/means['horizontal']-1), .05)
                self.assertLess(abs(means['vertical']/means['horizontal']-1), .05)
                self.assertLess(abs(means['frame']/means['horizontal']-1), .07)
                self.assertLess(statistics.pstdev(groups['curve'])/means['curve'], .06)

    def test_cached_background_and_geometry_cannot_be_mutated_by_callers(self):
        arena = Arena(0)
        args = (arena.space, 59, 31, 20)
        before = maze_background(*args, (74,91,255), 26)
        expected = pg.image.tobytes(before, 'RGB')
        before.fill('red')
        self.assertEqual(pg.image.tobytes(maze_background(*args, (74,91,255), 26), 'RGB'), expected)
        mask = maze_wall_mask(*args, 26)
        count = mask.count(); mask.clear()
        self.assertEqual(maze_wall_mask(*args, 26).count(), count)

    def test_hue_changes_reuse_geometry_basis(self):
        import arcade_art as art
        arena=Arena(0)
        art.maze_background(arena.space,59,31,20,(51,97,203),26)
        before=art._wall_basis.cache_info()
        art.maze_background(arena.space,59,31,20,(203,97,51),26)
        after=art._wall_basis.cache_info()
        self.assertEqual(after.misses,before.misses)
        self.assertGreater(after.hits,before.hits)
        self.assertEqual(after.maxsize,8)

    def test_smoke_has_soft_transparent_edges_and_time_variation(self):
        import arcade_art as art
        frames=[]
        for time in (0,.3):
            target=pg.Surface((128,128));target.fill((0,0,4))
            art.smoke_cloud(target,(64,64),time)
            self.assertEqual(tuple(target.get_at((10,64)))[:3],(0,0,4))
            self.assertGreater(sum(target.get_at((64,64))[:3]),40)
            frames.append(pg.image.tobytes(target,'RGB'))
        self.assertNotEqual(*frames)

    def test_shared_neon_compositor_retains_halo_alpha_on_opaque_target(self):
        ink = pg.Surface((80,80), pg.SRCALPHA)
        pg.draw.line(ink, (100,150,255), (20,40), (60,40), 3)
        sprite = neon_sprite(ink)
        target = pg.Surface((80,80)); target.fill((0,0,4))
        target.blit(sprite, (0,0), special_flags=pg.BLEND_PREMULTIPLIED)
        self.assertGreater(sum(target.get_at((40,35))[:3]), 4)
        self.assertGreater(sum(target.get_at((40,40))[:3]), sum(target.get_at((40,35))[:3]))


if __name__ == '__main__': unittest.main()
