"""Untimed mode is an explicit option, not a certified commercial rule."""
import json
import os
os.environ['SDL_VIDEODRIVER']='dummy'
os.environ['SDL_AUDIODRIVER']='dummy'
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from cabinet import CabinetStore, DEFAULTS, spectator_view, atomic_json
from game import App, Match
from replay import record, replay
from spectator import read_feed


class Survival(unittest.TestCase):
    def test_untimed_survives_elapsed_time_and_ends_on_human_elimination(self):
        game=Match(2,3,seed=42,rules={'match_seconds':0})
        game.fill_vacancies();game.foes=[];game.items.clear()
        for player in game.players:player.entry=0
        game.time=0
        for _ in range(361):game.update(1.)
        self.assertFalse(game.over)
        self.assertGreater(game.elapsed,360)
        game.players[0].lives=0;game.update(1/60);self.assertFalse(game.over)
        game.players[1].lives=0;game.update(1/60);self.assertTrue(game.over)
        self.assertEqual(game.ledger.events[-1]['context']['reason'],'elimination')
        self.assertTrue(any(player.bot and player.lives>0 for player in game.players))

    def test_untimed_progression_pause_and_replay(self):
        game=Match(1,3,seed=42,rules={'match_seconds':0})
        player=game.players[0];game.award(player,'dot')
        score=player.score;game.dots.clear();game.update(1/60)
        self.assertEqual(game.stage,2);self.assertFalse(game.over)
        self.assertGreater(player.score,score);self.assertEqual(game.time,0)
        game.paused=True;before=game.snapshot();game.update(30)
        self.assertEqual(game.snapshot(),before)
        document=record(1,3,42,120,fill_bots=True,rules={'match_seconds':0})
        restored=replay(json.loads(json.dumps(document)))
        self.assertEqual(restored.rules['match_seconds'],0)
        self.assertFalse(restored.over)

    def test_operator_save_and_cli_style_override_are_distinct(self):
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as folder:
            store=CabinetStore(folder)
            app=App(cabinet=store)
            try:
                app.untimed=True;app.count=1;app.start()
                self.assertEqual(app.match.rules['match_seconds'],0)
                self.assertEqual(store.settings['match_seconds'],180)
                app.match=None;app.station_action(7)
                self.assertEqual(app.match.rules['match_seconds'],0)
                app.draw()
                self.assertTrue(store.configure(dict(DEFAULTS,match_seconds=0)))
                self.assertEqual(CabinetStore(folder).settings['match_seconds'],0)
                app.operator_draft=dict(store.settings);app.operator_open=True;app.draw()
            finally:
                import pygame as pg
                pg.quit()

    def test_spectator_protocol_and_render_label_untimed(self):
        import pygame as pg
        game=Match(1,seed=42,rules={'match_seconds':0})
        feed=spectator_view(game,'playing')
        self.assertFalse(feed['timed'])
        with tempfile.TemporaryDirectory(dir=Path.cwd()) as folder:
            path=Path(folder)/'feed.json';atomic_json(path,feed)
            self.assertFalse(read_feed(path)['timed'])
            feed['timed']='no';atomic_json(path,feed);self.assertIsNone(read_feed(path))
        from spectator import draw_scoreboard
        pg.font.init();surface=pg.Surface((960,720));labels=[]
        font=pg.font.Font(None,24)
        class Font:
            def render(self,label,*args):labels.append(str(label));return font.render(str(label),*args)
        with patch.object(pg.font,'Font',return_value=Font()):
            feed['timed']=False;draw_scoreboard(surface,feed)
        self.assertTrue(any('LIFE SURVIVAL' in label for label in labels))
        pg.quit()


if __name__=='__main__':unittest.main(verbosity=2)
