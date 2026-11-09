"""Map data validation and configurable progression regression checks."""
import copy
import json
import os
from pathlib import Path
import random
import unittest
from map_library import catalog, get_map, next_map_index, parse_catalog


class MapTests(unittest.TestCase):
    def test_exterior_core_spacing_all_maps_and_palettes(self):
        import pygame as pg
        from game import App,Match,PALETTES,OX,TOP,COLS,ROWS,TILE
        app=App(simulate_controllers=True)
        for theme in range(4):
            app.match=Match(8,theme,seed=321)
            app.reset_visuals()
            for palette in range(len(PALETTES)):
                app.palette_override=palette;app.draw(0)
                for label,points in (
                    ('top',[(OX+300,TOP+i) for i in range(11)]),
                    ('bottom',[(OX+300,TOP+ROWS*TILE-1-i) for i in range(11)]),
                    ('left',[(OX+i,TOP+240) for i in range(11)]),
                    ('right',[(OX+COLS*TILE-1-i,TOP+240) for i in range(11)])):
                    values=[sum(app.canvas.get_at(p)[:3]) for p in points]
                    outer=max(range(0,4),key=values.__getitem__)
                    inner=max(range(5,10),key=values.__getitem__)
                    with self.subTest(map=theme,palette=palette,edge=label):
                        self.assertEqual(inner-outer,6)
                        self.assertLess(values[4],min(values[outer],values[inner])*.8)
        pg.quit()

    def test_exterior_corners_are_concentric(self):
        import pygame as pg
        from game import Arena
        from arcade_art import maze_wall_mask,FRAME_THICKNESS
        expected=pg.Surface((1180,620),pg.SRCALPHA)
        pg.draw.rect(expected,'white',expected.get_rect(),border_radius=16)
        pg.draw.rect(expected,(0,0,0,0),expected.get_rect().inflate(-18,-18),border_radius=7)
        expected=pg.mask.from_surface(expected)
        self.assertEqual(FRAME_THICKNESS,9)
        for theme in range(4):
            actual=maze_wall_mask(Arena(theme).space,59,31,20,26)
            for x0,y0 in ((0,0),(1156,0),(0,596),(1156,596)):
                for y in range(y0,y0+24):
                    for x in range(x0,x0+24):
                        self.assertEqual(actual.get_at((x,y)),expected.get_at((x,y)))

    def document(self):
        return json.loads(Path(__file__).with_name('maps.json').read_text(encoding='utf-8'))

    def test_catalog_versions_and_explicit_provenance(self):
        self.assertEqual([len(m.lanes) for m in catalog()], [569, 569, 585, 582])
        self.assertEqual([m.revision for m in catalog()], [4, 3, 4, 3])
        self.assertEqual(len({m.lanes for m in catalog()}), 4)
        for index, spec in enumerate(catalog()):
            self.assertEqual(get_map(index + 4), spec)
            self.assertIn('Independent topology reconstruction', spec.provenance)
            self.assertIn('Not an exact commercial map', spec.provenance)
            self.assertEqual(spec.lane_radius, 26)
        records = self.document()['maps']
        self.assertEqual([r['layout_family'] for r in records],
                         ['observed-D', 'observed-B', 'observed-C', 'observed-A'])
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
            self.assertIn('-cNOhumVZ74' if index in (1,3) else 'qcO9tzgsdjo', record['observations'][0]['source'])

    def test_actual_radius_keeps_visible_routes_and_thin_wall_stems(self):
        os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
        os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
        import pygame as pg
        from arcade_art import maze_background, wall_highlight, maze_wall_mask, _wall_ink
        from game import Arena, DIRS, TILE, COLS, ROWS
        pg.init()
        try:
            backgrounds = {}
            for index, spec in enumerate(catalog()):
                a = Arena(index)
                art = maze_background(a.space, COLS, ROWS, TILE, spec.accent, spec.lane_radius)
                backgrounds[index] = art
                # Each profile has a single-contour upper horizontal wall band.
                # A broad-island inset heuristic must not add interior rectangles.
                contour_y = [y for y in range(40, 100)
                             if max(tuple(art.get_at((150, y)))[:3]) > max(spec.accent)*.65]
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

    def test_observed_capsule_end_is_round_without_losing_wall_body(self):
        os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
        import pygame as pg
        from arcade_art import maze_background, wall_highlight, maze_wall_mask, _wall_ink
        from game import Arena
        pg.init()
        try:
            for index, spec in enumerate(catalog()):
                a = Arena(index)
                art = maze_background(a.space, 59, 31, 20, spec.accent, spec.lane_radius)
                # A top-left corner must recede; its rounded side midpoint and
                # long straight upper edge remain. Both source families show this.
                mask = maze_wall_mask(a.space, 59, 31, 20, spec.lane_radius)
                self.assertFalse(mask.get_at((60, 56)))
                self.assertTrue(mask.get_at((150, 70)))
                for point in ((56, 70), (150, 56)):
                    self.assertGreater(max(tuple(art.get_at(point))[:3]), max(spec.accent)*.65)
        finally:
            pg.quit()

    def test_actual_app_house_has_only_two_border_contours(self):
        os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
        os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
        import pygame as pg
        from game import App, Match, OX, TOP, TILE
        from arcade_art import wall_highlight
        app = App()
        try:
            for index, spec in enumerate(catalog()):
                app.match = Match(8, index, seed=1)
                app.reset_visuals()
                app.draw()
                dx, dy, dw, dh = spec.den
                box = pg.Rect(OX+dx*TILE+5, TOP+dy*TILE+5, dw*TILE-10, dh*TILE-10)
                scans = ([(box.centerx, y) for y in range(box.bottom-12, box.bottom+15)],
                         [(x, box.bottom-20) for x in range(box.left-15, box.left+12)])
                for points in scans:
                    hits = [i for i, point in enumerate(points)
                            if max(tuple(app.canvas.get_at(point))[:3]) > max(spec.accent)*.65]
                    runs = sum(i == 0 or n != hits[i-1]+1 for i, n in enumerate(hits))
                    self.assertEqual(runs, 2, (spec.id, 'house third contour', hits))
        finally:
            pg.quit()

    def test_normal_actor_body_clearance_on_every_rendered_route(self):
        os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
        import pygame as pg
        from arcade_art import maze_background, wall_highlight, maze_wall_mask, _wall_ink
        from game import Arena
        pg.init()
        try:
            for index, spec in enumerate(catalog()):
                a = Arena(index)
                art = maze_background(a.space, 59, 31, 20, spec.accent, spec.lane_radius)
                clearance = pg.Surface(art.get_size(), pg.SRCALPHA)
                for x, y in a.lanes:
                    cx, cy = x*20+10, y*20+10
                    pg.draw.circle(clearance, 'white', (cx, cy), 20)
                    for dx, dy in ((1, 0), (0, 1)):
                        if (x+dx, y+dy) in a.lanes:
                            rect = (cx, cy-20, 20, 40) if dx else (cx-20, cy, 40, 20)
                            pg.draw.rect(clearance, 'white', rect)
                # Glow is translucent presentation; only opaque fill/contour
                # count as walls. A20px radius exceeds normal player/foe bodies.
                walls = maze_wall_mask(a.space, 59, 31, 20, spec.lane_radius)
                # Include actual high-opacity antialiased stroke samples too.
                walls.draw(pg.mask.from_surface(_wall_ink(walls, spec.accent), 190), (0, 0))
                overlap = walls.overlap(pg.mask.from_surface(clearance), (0, 0))
                self.assertIsNone(overlap, (spec.id, 'actor body intersects wall', overlap))
        finally:
            pg.quit()

    def test_isolated_quantized_stems_have_bounded_width(self):
        os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
        import pygame as pg
        from arcade_art import maze_background, wall_highlight, maze_wall_mask, _wall_ink
        from game import Arena
        pg.init()
        try:
            for index, spec in enumerate(catalog()):
                a = Arena(index)
                art = maze_background(a.space, 59, 31, 20, spec.accent, spec.lane_radius)
                mask = maze_wall_mask(a.space, 59, 31, 20, spec.lane_radius)
                centers = (440, 740) if index in (0, 3) else (300, 880) if index == 2 else (880,)
                for center_x in centers:
                    opaque = [x for x in range(center_x-20, center_x+21)
                              if mask.get_at((x, 350))]
                    self.assertEqual(len(opaque), 16, (spec.id, center_x, opaque))
        finally:
            pg.quit()

    def test_new_observed_courtyard_and_rails_routes(self):
        c, d = get_map(2), get_map(0)
        self.assertEqual(c.portals, (5, 25))
        self.assertEqual(d.portals, (17,))
        # C has offset side-column corridors and a route below its outer U.
        self.assertTrue({(x, 11) for x in range(1, 14)} <= c.lanes)
        self.assertTrue({(x, 25) for x in range(20, 39)} <= c.lanes)
        self.assertNotIn((9, 25), c.lanes)  # solid lower-left rectangular island
        # D's long upper rail blocks a vertical shortcut at the board center.
        self.assertNotIn((29, 3), d.lanes)
        self.assertTrue({(x, 9) for x in range(1, 58)} <= d.lanes)

    def test_wall_photo_treatment_has_soft_halo_and_bright_inner_ink(self):
        os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
        import pygame as pg
        from arcade_art import maze_background, wall_highlight, maze_wall_mask, _wall_ink
        from game import Arena
        pg.init()
        try:
            for index, spec in enumerate(catalog()):
                a = Arena(index)
                art = maze_background(a.space, 59, 31, 20, spec.accent, spec.lane_radius)
                outer = tuple(art.get_at((180, 56)))[:3]
                core = tuple(art.get_at((180, 57)))[:3]
                self.assertGreater(max(outer), max(spec.accent)*.65)
                self.assertGreater(sum(core), sum(outer))
                self.assertGreater(sum(tuple(art.get_at((180, 51)))[:3]), 4)
                self.assertEqual(tuple(art.get_at((180, 30)))[:3], (0, 0, 4))
        finally:
            pg.quit()

    def test_photo_outer_frame_corners_are_round_but_edges_remain(self):
        os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
        import pygame as pg
        from arcade_art import maze_background, wall_highlight, maze_wall_mask, _wall_ink
        from game import Arena
        pg.init()
        try:
            for index, spec in enumerate(catalog()):
                a = Arena(index)
                art = maze_background(a.space, 59, 31, 20, spec.accent, spec.lane_radius)
                mask = maze_wall_mask(a.space, 59, 31, 20, spec.lane_radius)
                for point in ((0, 0), (1179, 0), (0, 619), (1179, 619)):
                    self.assertFalse(mask.get_at(point))
                for point in ((0, 60), (60, 0), (1179, 60), (60, 619)):
                    self.assertGreater(max(tuple(art.get_at(point))[:3]), max(spec.accent)*.65)
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
                    positions = [p.pos for p in g.players]
                    target = Arena(theme+1)
                    legal = {p.idx for p in g.players if target.can_enter(p.pos,p)}
                    g.dots.clear()
                    g.update(0)
                    self.assertEqual(g.stage, 2)
                    self.assertEqual(g.arena.map_id, get_map(theme+1).id)
                    self.assertEqual(g.time, remaining)
                    self.assertEqual([p.lives for p in g.players], lives)
                    for i, p in enumerate(g.players):
                        self.assertTrue(g.arena.can_enter(p.pos,p))
                        if p.idx in legal:
                            self.assertEqual(p.pos,positions[i])
                        else:
                            # Valid actors reserve their cells before displaced
                            # actors move to the nearest remaining public lane.
                            occupied={g.players[j].pos for j in legal}
                            occupied.update(g.players[j].pos for j in range(i) if j not in legal)
                            free=g.arena.lanes-occupied
                            from game import distance
                            nearest=min(distance(positions[i],cell) for cell in free)
                            self.assertEqual(distance(positions[i],p.pos),nearest)
                        self.assertGreaterEqual(p.score, scores[i])
                    stage_events=[e for e in g.ledger.events if e['event']=='stage_start']
                    self.assertTrue(stage_events[-1]['context']['actors_preserved'])
                    self.assertTrue(g.refill_pending)
                    self.assertFalse(g.dots)

    def test_sparse_station_identity_survives_map_transition(self):
        from game import Match
        for theme in range(4):
            for station in range(8):
                with self.subTest(theme=theme, station=station):
                    g = Match(0, theme, seed=88)
                    self.assertTrue(g.join_station(station))
                    self.assertEqual(g.count, 1)
                    self.assertEqual([p.idx for p in g.players if p.joined], [station])
                    positions=[p.pos for p in g.players]
                    g.dots.clear()
                    g.update(0)
                    self.assertFalse(g.over)
                    self.assertEqual(g.stage, 2)
                    self.assertEqual(g.count, 1)
                    for p in g.players:
                        self.assertEqual(p.pos, positions[p.idx])
                        if p.joined:self.assertEqual(p.pos,g.arena.spawns[p.idx])
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
