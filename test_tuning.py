"""Measured timing can be substituted without changing physics source code."""
import json
import math
import os
os.environ['SDL_VIDEODRIVER'] = 'dummy'
os.environ['SDL_AUDIODRIVER'] = 'dummy'
import tempfile
import unittest
from pathlib import Path
from game import Match, App
from gameplay_tuning import DEFAULT_TUNING, validate_tuning, load_tuning
from replay import record, replay, digest


class Tuning(unittest.TestCase):
    def test_validation_copy_and_invalid_configs(self):
        source = {'durations': {'Titan': 1.25}}
        first = validate_tuning(source)
        source['durations']['Titan'] = 999
        first['durations']['Crown'] = 2
        self.assertEqual(validate_tuning()['durations']['Crown'], 7)
        self.assertEqual(first['durations']['Titan'], 1.25)
        for invalid in ([], {'duration': 2}, {'durations': {'Heart': 2}},
                        {'durations': {'Titan': True}}, {'durations': {'Titan': math.inf}},
                        {'spawn_seconds': 0}, {'ghost_step_seconds': math.nan},
                        {'spark_radius': 1.5}, {'max_items': 0}, {'quake_multiplier': .5}):
            with self.subTest(invalid=invalid), self.assertRaises(ValueError): validate_tuning(invalid)

    def ready(self, tuning):
        game = Match(2, 3, seed=42, tuning=tuning)
        game.items.clear(); game.foes=[]
        for player in game.players:
            player.entry=0; player.direction=player.wanted=(0,0)
        return game

    def test_actual_nondefault_power_expiration_and_refresh(self):
        for name in ('Crown','Titan','Rush','Mist','Slick','Veil','Flare','Lure'):
            game=self.ready({'durations': {name: .5}, 'spawn_seconds': 120})
            player=game.players[0]; game.collect(player,name)
            pickup=game.ledger.events[-1]
            self.assertEqual(pickup['context']['duration'],.5)
            self.assertEqual(pickup['context']['expires_at'],.5)
            # Banana's random motion is valid; keep foes/items absent.
            for _ in range(29):game.update(1/60)
            self.assertTrue(game.active(player,name),name)
            game.collect(player,name)
            for _ in range(29):game.update(1/60)
            self.assertTrue(game.active(player,name),name)
            game.update(1/60)
            self.assertFalse(game.active(player,name),name)

    def test_nondefault_lightning_range_and_duration(self):
        game=self.ready({'durations': {'Spark': .5}, 'spark_radius': 2})
        player,other=game.players;player.pos=(1,1);other.pos=(4,1)
        game.collect(player,'Spark');self.assertEqual(other.stun,0)
        other.pos=(3,1);game.collect(player,'Spark')
        for _ in range(29):game.update(1/60)
        self.assertGreater(other.stun,0)
        game.update(1/60);self.assertEqual(other.stun,0)

    def test_quake_spawn_cap_and_flame_ranges_use_config(self):
        game=self.ready({'durations': {'Quake': .5}, 'spawn_seconds': .5,
                         'max_items': 1, 'flame_cells': 2})
        player=game.players[0];player.pos=(1,1);player.direction=(1,0)
        self.assertEqual(game.fire_cells(player),[(2,1),(3,1)])
        game.collect(player,'Quake')
        for _ in range(29):game.update(1/60)
        self.assertGreater(game.quake,0);self.assertEqual(len(game.items),0)
        game.update(1/60);self.assertEqual(game.quake,0);self.assertEqual(len(game.items),1)
        for _ in range(60):game.update(1/60)
        self.assertLessEqual(len(game.items),1)
        game.new_arena(1);self.assertEqual(len(game.items),1)

    def test_modified_movement_intervals_and_ghost_clock(self):
        game=self.ready({'player_step_seconds': .2, 'ghost_step_seconds': .3})
        player=game.players[0];player.pos=(1,1);player.wanted=(1,0)
        for _ in range(11):game.update(1/60)
        self.assertEqual(player.pos,(1,1))
        game.update(1/60);self.assertEqual(player.pos,(2,1))
        game=Match(1,seed=42,tuning={'ghost_step_seconds': .3})
        game.foes=[(5,1)];game.foe_modes=['roaming'];game.foe_release=[0]
        game.foe_ticks=[0];game.foe_zapped=[0]
        game.update_foes(.29);self.assertEqual(game.foes,[(5,1)])
        game.update_foes(.01);self.assertNotEqual(game.foes,[(5,1)])

    def test_profile_replay_and_app_restart_retain_effective_values(self):
        tuning={'durations': {'Titan': 1.25},'spark_radius':3,'spawn_seconds':1.5}
        document=record(1,3,42,180,fill_bots=True,tuning=tuning)
        restored=replay(json.loads(json.dumps(document)))
        self.assertEqual(digest(restored),document['final_digest'])
        self.assertEqual(document['initial']['tuning'],restored.tuning)
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as temp:
            path=Path(temp)/'timing.json';path.write_text(json.dumps(tuning),encoding='utf-8')
            self.assertEqual(load_tuning(path),validate_tuning(tuning))
            from cabinet import CabinetStore
            app=App(cabinet=CabinetStore(temp))
            try:
                app.tuning=load_tuning(path);app.count=1;app.start()
                self.assertEqual(app.match.tuning,validate_tuning(tuning))
                app.match.over=True;app.start()
                self.assertEqual(app.match.tuning['durations']['Titan'],1.25)
            finally:
                import pygame as pg
                pg.quit()


if __name__=='__main__':unittest.main(verbosity=2)
