"""Score attribution, deterministic replay and station lifecycle regressions."""
import copy
import json
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'
import unittest
from game import App, Match, ITEMS, pg
from replay import FixedStepper, digest, record, replay, STEP


class LedgerTests(unittest.TestCase):
    def clean(self, count=2):
        g = Match(count, seed=7)
        g.items.clear()
        for p in g.players:
            p.pos = (1 + p.idx * 4, 1)
            p.entry = p.safe = p.stun = 0
            p.direction = p.wanted = (0, 0)
        g.foe_modes = ['house'] * 4
        g.dots.difference_update(p.pos for p in g.players)
        return g

    def check_total(self, g):
        totals = g.ledger.totals()
        for p in g.players:
            self.assertEqual(p.score, totals.get(p.idx+1, 0))
        for event in g.ledger.events:
            self.assertIn('tick', event)
            self.assertIn('context', event)

    def test_every_score_route_has_attributed_event(self):
        g = self.clean()
        p, q = g.players
        p.direction = p.wanted = (1, 0)
        g.update(.1)
        self.assertTrue(any(e['event'] == 'dot' for e in g.ledger.events))
        for name in ITEMS: g.collect(p, name)
        p.effects = {'Crown': 7}
        g.foes[0] = p.pos
        g.foe_modes[0] = 'roaming'
        g.combat()
        p.effects = {'Titan': 7}
        q.pos = p.pos; q.safe = 0
        g.combat()
        q.safe = 0; q.pos = (3, 1)
        p.pos = (1, 1); p.direction = (1, 0); p.effects = {'Flare': 3}
        g.foes[1] = (2, 1); g.foe_modes[1] = 'roaming'
        g.apply_fire()
        q.safe = 0; q.pos = (5, 1)
        p.effects = {'Lure': 7}
        g.foes[2] = q.pos; g.foe_modes[2] = 'carried'; g.foe_carriers[2] = 0
        g.combat()
        g.dots.clear(); g.update(.01)
        events = [e['event'] for e in g.ledger.events]
        for name in ('dot', 'pickup', 'ghost_eaten', 'rival_eaten', 'ghost_burned',
                     'rival_burned', 'carried_ghost_hit', 'stage_clear'):
            self.assertIn(name, events)
        self.check_total(g)
        for event in g.ledger.events:
            if event['delta']:
                self.assertEqual(event['player_id'], 1)
                self.assertIn('position', event['context'])

    def test_no_phantom_award_for_immune_or_repeated_attack(self):
        g = self.clean()
        p, q = g.players
        p.effects = {'Titan': 7}; q.pos = p.pos; q.safe = 3
        g.combat(); self.assertEqual(p.score, 0)
        q.safe = 0; g.combat()
        score = p.score
        g.combat(); self.assertEqual(p.score, score)
        self.check_total(g)

    def test_bonus_life_ledger_once_and_configurable_scores(self):
        g = Match(1, seed=2, score_values={'pickup': 10000})
        p = g.players[0]
        g.collect(p, 'Rush'); g.award_score_lives(); g.award_score_lives()
        self.assertEqual(p.lives, 4)
        self.assertEqual(sum(e['event']=='score_bonus_life' for e in g.ledger.events), 1)
        self.check_total(g)
        with self.assertRaises(ValueError): Match(score_values={'dot': -1})
        with self.assertRaises(ValueError): Match(score_values={'invented': 1})

    def test_pause_end_and_tie_ranking(self):
        g = self.clean(4)
        g.award(g.players[2], 'pickup'); g.award(g.players[0], 'pickup')
        self.assertEqual([r['rank'] for r in g.rankings()], [1, 1, 3, 3])
        before = digest(g)
        g.paused = True
        elapsed, tick = g.elapsed, g.tick
        g.update(1)
        self.assertEqual((g.elapsed, g.tick), (elapsed, tick))
        g.paused = False; self.assertEqual(digest(g), before)
        g.time = .001; g.update(.01); g.update(.01)
        self.assertEqual(sum(e['event']=='match_end' for e in g.ledger.events), 1)

    def test_station_join_preserves_other_scores_and_no_free_revival(self):
        g = self.clean(1)
        g.award(g.players[0], 'pickup')
        self.assertTrue(g.join_station(7))
        self.assertEqual(g.count, 2)
        self.assertEqual(g.players[7].pos, g.arena.spawns[7])
        self.assertEqual([r['player_id'] for r in g.rankings()], [1, 8])
        self.assertFalse(g.join_station(7))
        g.players[7].lives = 0
        self.assertFalse(g.join_station(7))
        g.paused = True; self.assertFalse(g.join_station(3))
        g.paused = False; g.over = True; self.assertFalse(g.join_station(3))
        self.check_total(g)

    def test_replay_json_roundtrip_all_counts_and_maps(self):
        for count in (1, 2, 4, 8):
            for theme in range(4):
                with self.subTest(count=count, theme=theme):
                    doc = record(count, theme, 100+theme, 100)
                    g = replay(json.loads(json.dumps(doc)))
                    self.check_total(g)

    def test_replay_rejects_divergence(self):
        doc = record(2, 0, 42, 180)
        bad = copy.deepcopy(doc); bad['initial']['seed'] = 43
        with self.assertRaisesRegex(ValueError, 'diverged'): replay(bad)
        bad = copy.deepcopy(doc); bad['commands'][0]['directions'][0] = [7, 2]
        with self.assertRaisesRegex(ValueError, 'direction'): replay(bad)
        bad = copy.deepcopy(doc); bad['events'][0]['context']['count'] = 8
        with self.assertRaisesRegex(ValueError, 'trace'): replay(bad)

    def test_seed_sweep_and_progression(self):
        for seed in range(1, 9):
            doc = record(8, seed%4, seed, 180)
            self.check_total(replay(json.loads(json.dumps(doc))))
        for policy in ('repeat', 'cycle', 'random'):
            a = Match(1, 2, 7, progression=policy)
            b = Match(1, 2, 7, progression=policy)
            for g in (a, b):
                for _ in range(5): g.dots.clear(); g.update(1/60)
            self.assertEqual(digest(a), digest(b))
            if policy == 'repeat': self.assertEqual(a.arena.theme, 2)
            if policy == 'cycle': self.assertEqual(a.arena.theme, 3)
        with self.assertRaises(ValueError): Match(progression='unverified')

    def test_sparse_station_join_replays_in_the_same_tick_order(self):
        g = Match(1, seed=42)
        commands = []
        for frame in range(90):
            joins = [7, 3] if frame == 12 else []
            for idx in joins: self.assertTrue(g.join_station(idx))
            command = {'join_stations': joins,
                       'directions': [list(p.wanted) for p in g.players]}
            commands.append(command); g.update(STEP)
        doc = {'schema_version': 1, 'step': STEP,
               'initial': {'count': 1, 'seed': 42}, 'commands': commands,
               'events': g.ledger.events, 'final_digest': digest(g)}
        result = replay(json.loads(json.dumps(doc)))
        self.assertEqual(result.count, 3)
        self.assertEqual([e['player_id'] for e in result.ledger.events
                          if e['event']=='station_join'], [8, 4])

    def test_fixed_step_grouping_preserves_state_and_events(self):
        matches = [Match(8, 2, 42) for _ in range(3)]
        def scripted(g, frame):
            for p in g.players:
                p.wanted = ((1, 0), (0, 1), (-1, 0), (0, -1))[(frame//37+p.idx)%4]
        for g, fps in zip(matches, (30, 60, 144)):
            stepper = FixedStepper(g, scripted)
            for _ in range(fps * 5): stepper.advance(1/fps)
            self.assertEqual(stepper.steps, 300)
        self.assertEqual(digest(matches[0]), digest(matches[1]))
        self.assertEqual(digest(matches[1]), digest(matches[2]))

    def test_render_keeps_logic_and_exact_separate_score_popups(self):
        app = App(simulate_controllers=True)
        try:
            app.match = Match(1, seed=42)
            player = app.match.players[0]
            player.pos = (5, 5)
            app.match.collect(player, 'Rush')
            app.match.collect(player, 'Mist')
            before = digest(app.match)
            app.draw(1/60)
            self.assertEqual(digest(app.match), before)
            self.assertEqual([p[0] for p in app.popups], ['75', '75'])
            app.draw(1/60)
            self.assertEqual([p[0] for p in app.popups], ['75', '75'])
            self.assertEqual(app.score_memory[0], player.score)
            self.assertEqual(app.ledger_cursor, len(app.match.ledger.events))
        finally: pg.quit()

    def test_paused_and_guide_locator_do_not_expire_or_catch_up(self):
        app = App(simulate_controllers=True)
        try:
            app.match = Match(0, seed=42)
            app.station_action(7)
            player = app.match.players[7]
            app.advance(1/120)  # A half-step must not leak across pause.
            self.assertGreater(app.fixed_accumulator, 0)
            for mode in ('paused', 'guide'):
                if mode == 'paused': app.match.paused = True
                else: app.help = True
                before = digest(app.match)
                app.advance(10)
                app.draw(.5)
                self.assertEqual(digest(app.match), before)
                self.assertEqual(player.locate_remaining, app.locator_seconds)
                self.assertEqual(app.fixed_accumulator, 0)
                app.match.paused = False; app.help = False
            app.advance(1/60)
            self.assertEqual(app.match.tick, 1)
            self.assertAlmostEqual(player.locate_remaining, app.locator_seconds-1/60)
            self.assertEqual([p.idx for p in app.match.players if p.joined], [7])
            self.assertTrue(all(p.bot and p.lives == app.match.rules['starting_lives'] and p.score == 0
                                for p in app.match.players if not p.joined))
        finally: pg.quit()


if __name__ == '__main__': unittest.main(verbosity=2)
