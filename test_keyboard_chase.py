import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')

import game
from cabinet import CabinetStore
from gameplay_tuning import load_tuning


class KeyboardChase(unittest.TestCase):
    def test_human_can_wait_then_exit_once_after_spawn_and_respawn(self):
        profile=load_tuning(Path(__file__).with_name('tuning.keyboard-playtest.json'))
        for theme in range(4):
            match=game.Match(8,theme,seed=4,tuning=profile)
            match.foes=[];match.items.clear()
            for respawn in (False,True):
                for p in match.players:
                    if respawn:
                        p.safe=0
                        self.assertTrue(match.hurt(p))
                    p.wanted=(1,0)
                for _ in range(120):match.update(1/60)
                self.assertEqual([p.pos for p in match.players], match.arena.spawns)
                for p in match.players:
                    p.wanted=(0,1 if p.pos[1]==0 else -1)
                match.update(1/60)
                self.assertEqual([p.pos for p in match.players], match.arena.entries)
                for p in match.players:
                    self.assertFalse(match.arena.can_enter(match.arena.spawns[p.idx],p))

    def test_straight_chase_with_and_without_caffeine(self):
        profile = load_tuning(Path(__file__).with_name('tuning.keyboard-playtest.json'))
        for tuning in (None, profile):
            for boosted in (False, True):
                match = game.Match(1, 0, seed=3, tuning=tuning)
                player = match.players[0]
                player.pos = (8, 1)
                player.entry = player.clock = 0
                player.direction = player.wanted = (1, 0)
                match.items.clear()
                match.foes[0] = (3, 1)
                match.foe_previous[0] = (2, 1)
                match.foe_modes[0] = 'roaming'
                match.foe_release[1:] = [100] * 3
                if boosted:
                    match.collect(player, 'Rush')
                with patch.object(match.rng, 'random', return_value=0):
                    for tick in range(93):
                        match.update(1/60)
                        if not boosted:
                            self.assertEqual(player.pos[0] - match.foes[0][0], 5)
                self.assertEqual(match.foes[0], (13, 1))
                self.assertEqual(player.pos, (23 if boosted else 18, 1))

    def test_visible_count_tracks_lives_and_clears_on_elimination(self):
        with tempfile.TemporaryDirectory() as directory:
            app = game.App(simulate_controllers=True, cabinet=CabinetStore(directory))
            try:
                app.count = 2
                app.cabinet.settings['fill_bots'] = False
                app.start()
                player = app.match.players[0]
                other = app.match.players[1]
                def drawn_labels():
                    with patch.object(app, 'text', wraps=app.text) as draw:
                        app.draw(0)
                    return [call.args[:3] for call in draw.call_args_list]
                def lives_label(actor):
                    spawn = app.match.arena.spawns[actor.idx]
                    rect = game.station_hud(spawn)['lives']
                    return (f'LIVES {actor.lives}', *rect.topleft)
                for expected in (3, 2, 1):
                    self.assertEqual(player.lives, expected)
                    labels = drawn_labels()
                    self.assertIn(lives_label(player), labels)
                    self.assertIn(lives_label(other), labels)
                    player.safe = 0
                    app.match.hurt(player)
                labels = drawn_labels()
                self.assertFalse(any(label.startswith('LIVES') and x == lives_label(player)[1]
                                     for label, x, y in labels))
            finally:
                game.pg.quit()

    def test_quake_countdown_and_first_giant_pickup(self):
        with tempfile.TemporaryDirectory() as directory:
            app = game.App(simulate_controllers=True, cabinet=CabinetStore(directory))
            try:
                app.count = 2
                app.cabinet.settings['fill_bots'] = False
                app.start()
                match = app.match
                collector, rival = match.players
                match.collect(collector, 'Titan')
                with patch.object(game, 'maze_background', side_effect=AssertionError('built during pickup')):
                    app.draw(0)
                base_interval = match.player_interval(collector)
                match.collect(collector, 'Quake')
                self.assertEqual(match.player_interval(collector), base_interval * 2)
                self.assertEqual(match.player_interval(rival), base_interval * 2)
                for seconds, expected in ((5,'EARTHQUAKE 5s'),(.2,'EARTHQUAKE 1s'),(0,None)):
                    match.quake = seconds
                    with patch.object(app,'text',wraps=app.text) as draw:
                        app.draw(0)
                    labels = [call.args[0] for call in draw.call_args_list
                              if call.args[0].startswith('EARTHQUAKE')]
                    self.assertEqual(labels, [expected] if expected else [])
                self.assertEqual(match.player_interval(collector), base_interval)
            finally:
                game.pg.quit()
