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

    def test_catalog_versions_and_authored_provenance(self):
        # First three retain the migration baseline; cyan v2 is a local correction.
        self.assertEqual([len(m.lanes) for m in catalog()], [577, 589, 579, 578])
        self.assertEqual([m.revision for m in catalog()], [1, 1, 1, 2])
        self.assertEqual(len({m.lanes for m in catalog()}), 4)
        for index, spec in enumerate(catalog()):
            self.assertEqual(get_map(index + 4), spec)
            self.assertIn('not a recovered DX map', spec.provenance)

    def test_cyan_house_perimeter_and_separate_vertical_walls(self):
        spec = get_map(3)
        perimeter = ({(x, y) for x in (21, 33) for y in range(13, 22)} |
                     {(x, y) for x in range(21, 34) for y in (13, 21)})
        self.assertTrue(perimeter <= spec.lanes)
        # Two separate narrow wall islands to the right of the house, with
        # single center-line corridors between them and around their ends.
        self.assertFalse({(x, y) for x in range(34, 37) for y in range(10, 21)} & spec.lanes)
        self.assertFalse({(x, y) for x in range(38, 41) for y in range(10, 25)} & spec.lanes)
        self.assertTrue({(37, y) for y in range(9, 26)} <= spec.lanes)
        self.assertTrue({(41, y) for y in range(9, 26)} <= spec.lanes)

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
