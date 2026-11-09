"""Map data validation and configurable progression regression checks."""
import copy
import json
import os
from pathlib import Path
import random
import unittest
from map_library import catalog, get_map, next_map_index, parse_catalog


class MapTests(unittest.TestCase):
    def document(self):
        return json.loads(Path(__file__).with_name('maps.json').read_text(encoding='utf-8'))

    def test_catalog_versions_and_explicit_provenance(self):
        self.assertEqual([len(m.lanes) for m in catalog()], [582, 569, 569, 582])
        self.assertEqual([m.revision for m in catalog()], [3, 3, 3, 3])
        self.assertEqual(len({m.lanes for m in catalog()}), 2)
        for index, spec in enumerate(catalog()):
            self.assertEqual(get_map(index + 4), spec)
            self.assertIn('Independent topology reconstruction', spec.provenance)
            self.assertIn('Not an exact commercial map', spec.provenance)
            self.assertEqual(spec.lane_radius, 26)
        self.assertEqual(get_map(0).lanes, get_map(3).lanes)
        self.assertEqual(get_map(1).lanes, get_map(2).lanes)
        records = self.document()['maps']
        self.assertEqual([r['layout_family'] for r in records],
                         ['observed-A', 'observed-B', 'observed-B', 'observed-A'])
        self.assertEqual(len({tuple(r['accent']) for r in records}), 4)

    def test_observed_layout_landmarks_and_gate_positions(self):
        a, b = get_map(3), get_map(1)
        self.assertEqual(a.portals, (5, 25))
        self.assertEqual(b.portals, (17,))
        for spec in (a, b):
            self.assertEqual(spec.den, (25, 15, 9, 5))
            self.assertEqual({x for x, y in spec.entries}, {6, 20, 38, 52})
        # A: the upper central arch separates inside/outside horizontal routes.
        self.assertNotIn((22, 5), a.lanes)
        self.assertTrue({(x, 5) for x in range(24, 36)} <= a.lanes)
        # B: central T divides top flow; only its flanks connect vertically.
        self.assertNotIn((29, 5), b.lanes)
        self.assertIn((24, 5), b.lanes)
        self.assertIn((35, 5), b.lanes)
        self.assertNotEqual(a.lanes, b.lanes)
        for index in range(4):
            record = self.document()['maps'][index]
            self.assertTrue(record['observations'][0]['inferred_regions'])
            self.assertIn('-cNOhumVZ74', record['observations'][0]['source'])

    def test_actual_radius_keeps_visible_routes_and_thin_wall_stems(self):
        os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
        os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
        import pygame as pg
        from arcade_art import maze_background
        from game import Arena, DIRS, TILE, COLS, ROWS
        pg.init()
        try:
            backgrounds = {}
            for index, spec in enumerate(catalog()):
                a = Arena(index)
                art = maze_background(a.space, COLS, ROWS, TILE, spec.accent, spec.lane_radius)
                backgrounds[index] = art
                # Both observed families have a single-contour upper-left capsule.
                # A broad-island inset heuristic must not add interior rectangles.
                contour_y = [y for y in range(40, 100)
                             if tuple(art.get_at((150, y)))[:3] == spec.accent]
                runs = sum(i == 0 or y != contour_y[i-1]+1
                           for i, y in enumerate(contour_y))
                self.assertEqual(runs, 2, (spec.id, 'extra capsule contours', contour_y))
                for x, y in a.lanes:
                    for direction in DIRS:
                        nxt = a.step((x, y), direction)
                        if nxt not in a.lanes or abs(nxt[0]-x)+abs(nxt[1]-y) != 1:
                            continue
                        for t in range(TILE):
                            pixel = (x*TILE+10+direction[0]*t, y*TILE+10+direction[1]*t)
                            self.assertEqual(tuple(art.get_at(pixel))[:3], (0, 0, 4),
                                             (spec.id, (x, y), nxt, pixel))
            # These narrow stems disappeared with a 26px carve plus 5px rounding.
            # Pin both continuity and actual rendered pixels, not just graph data.
            for index, x, y0, y1 in ((3, 440, 320, 380), (3, 740, 90, 130),
                                      (1, 580, 100, 200)):
                for y in range(y0, y1+1):
                    self.assertNotEqual(tuple(backgrounds[index].get_at((x, y)))[:3], (0, 0, 4),
                                        ('missing wall stem', index, x, y))
        finally:
            pg.quit()

    def test_invalid_lane_radius_is_rejected(self):
        for radius in (0, 16, 37, True, 26.5):
            doc = self.document()
            doc['maps'][0]['lane_radius'] = radius
            with self.subTest(radius=radius), self.assertRaises(ValueError):
                parse_catalog(doc)

    def test_every_map_house_loop_and_door_are_traversable(self):
        from game import Arena, DIRS
        for index, spec in enumerate(catalog()):
            with self.subTest(map=spec.id):
                x, y, width, height = spec.den
                left, right, top, bottom = x-2, x+width+1, y-2, y+height+1
                loop = ([(xx, top) for xx in range(left, right+1)] +
                        [(right, yy) for yy in range(top+1, bottom+1)] +
                        [(xx, bottom) for xx in range(right-1, left-1, -1)] +
                        [(left, yy) for yy in range(bottom-1, top-1, -1)])
                a = Arena(index)
                for source, target in zip(loop, loop[1:]):
                    self.assertIn(source, a.lanes)
                    direction = (target[0]-source[0], target[1]-source[1])
                    self.assertIn(direction, DIRS)
                    self.assertEqual(a.step(source, direction), target)
                self.assertIn((x+width//2, top), a.lanes)

    def test_each_map_rejects_removed_house_door_approach(self):
        for index in range(len(catalog())):
            doc = self.document()
            raw = doc['maps'][index]
            x, y, width, _ = raw['den']
            door_x, approach_y = x+width//2, y-2
            row = raw['lane_rows'][approach_y]
            raw['lane_rows'][approach_y] = row[:door_x]+'#'+row[door_x+1:]
            with self.subTest(map=raw['id']), self.assertRaises(ValueError):
                parse_catalog(doc)

    def test_rejects_invalid_schema_and_duplicate_maps(self):
        for doc in ({'schema_version':2}, {'schema_version':1, 'maps':[]}):
            with self.assertRaises(ValueError): parse_catalog(doc)
        doc = self.document()
        doc['maps'].append(copy.deepcopy(doc['maps'][0]))
        with self.assertRaises(ValueError): parse_catalog(doc)

    def test_rejects_geometry_corruption(self):
        changes = (
            ('lane_rows', ['.']),
            ('entries', [[0, 0]] * 8),
            ('spawns', [[5, 0]] * 8),
            ('portals', [8, 25]),
            ('den', [-1, 15, 9, 5]),
            ('den', [1, 1, 2, 2]),
            ('accent', [0, -1, 256]),
        )
        for field, value in changes:
            with self.subTest(field=field, value=value):
                doc = self.document()
                doc['maps'][0][field] = value
                with self.assertRaises(ValueError): parse_catalog(doc)
        doc = self.document()
        rows = doc['maps'][0]['lane_rows']
        rows[17] = rows[17][:27] + '.' + rows[17][28:]
        with self.assertRaises(ValueError): parse_catalog(doc)

    def test_progression_is_explicit_and_seeded(self):
        self.assertEqual([next_map_index(i) for i in range(4)], [1, 2, 3, 0])
        self.assertEqual([next_map_index(i, 'repeat') for i in range(4)], list(range(4)))
        a, b = random.Random(19), random.Random(19)
        self.assertEqual([next_map_index(0, 'random', a) for _ in range(30)],
                         [next_map_index(0, 'random', b) for _ in range(30)])
        with self.assertRaises(ValueError): next_map_index(0, 'random')
        with self.assertRaises(ValueError): next_map_index(0, 'invented')

    def test_integrated_all_counts_all_maps_and_transitions(self):
        os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
        os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
        from game import Arena, Match, steer_demo
        for theme in range(4):
            spec = get_map(theme)
            a = Arena(theme)
            self.assertEqual(a.lanes, spec.lanes)
            self.assertEqual(a.floor, spec.lanes | set(spec.spawns))
            for count in range(1, 9):
                with self.subTest(theme=theme, count=count):
                    g = Match(count, theme, seed=100 + count)
                    for _ in range(180):
                        steer_demo(g)
                        g.update(1/60)
                    self.assertFalse(g.over)
                    for p in g.players:
                        self.assertIn(p.pos, a.floor)
                    lives = [p.lives for p in g.players]
                    scores = [p.score for p in g.players]
                    remaining = g.time
                    g.dots.clear()
                    g.update(0)
                    self.assertEqual(g.stage, 2)
                    self.assertEqual(g.arena.map_id, get_map(theme+1).id)
                    self.assertEqual(g.time, remaining)
                    self.assertEqual([p.lives for p in g.players], lives)
                    for i, p in enumerate(g.players):
                        self.assertEqual(p.pos, g.arena.spawns[p.idx])
                        self.assertGreaterEqual(p.score, scores[i])

    def test_sparse_station_identity_survives_map_transition(self):
        from game import Match
        for theme in range(4):
            for station in range(8):
                with self.subTest(theme=theme, station=station):
                    g = Match(0, theme, seed=88)
                    self.assertTrue(g.join_station(station))
                    self.assertEqual(g.count, 1)
                    self.assertEqual([p.idx for p in g.players if p.joined], [station])
                    g.dots.clear()
                    g.update(0)
                    self.assertFalse(g.over)
                    self.assertEqual(g.stage, 2)
                    self.assertEqual(g.count, 1)
                    for p in g.players:
                        self.assertEqual(p.pos, g.arena.spawns[p.idx])
                        self.assertEqual(p.joined, p.idx == station)
                        self.assertEqual(p.lives, 3 if p.joined else 0)
                        self.assertEqual(p.score, 500 if p.joined else 0)
                    self.assertEqual([r['player_id'] for r in g.rankings()], [station+1])

    def test_locator_labels_stay_visible_at_all_station_bays(self):
        os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
        os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
        from game import App, Match, OX, TOP, COLS, ROWS, TILE
        app = App(simulate_controllers=True)
        labels = []
        original = app.text
        def capture(text, x, y, color=(224,234,247), font=None):
            if text in {f'P{i}' for i in range(1, 9)}:
                width, height = (font or app.font).size(text)
                labels.append((x, y, width, height))
            return original(text, x, y, color, font)
        app.text = capture
        for theme in range(4):
            for giant in (False, True):
                app.match = Match(8, theme, seed=7)
                app.reset_visuals()
                for p in app.match.players:
                    p.locate_remaining = 2
                    if giant: p.effects['Titan'] = 7
                labels.clear()
                app.draw()
                self.assertEqual(len(labels), 8)
                for x, y, width, height in labels:
                    self.assertGreaterEqual(x, OX)
                    self.assertGreaterEqual(y, TOP)
                    self.assertLessEqual(x+width, OX+COLS*TILE)
                    self.assertLessEqual(y+height, TOP+ROWS*TILE)


if __name__ == '__main__':
    unittest.main(verbosity=2)
