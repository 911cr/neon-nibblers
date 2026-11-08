"""Real dummy-mixer and application event audio QA; not speaker/hardware proof."""
import os
os.environ.setdefault('SDL_VIDEODRIVER','dummy')
os.environ.setdefault('SDL_AUDIODRIVER','dummy')
import unittest
from types import SimpleNamespace
from unittest.mock import patch
import pygame as pg
from arcade_audio import ArcadeAudio, PATTERNS, EVENT_CUES, synthesize
from game import App

class AudioQA(unittest.TestCase):
    def tearDown(self): pg.quit()
    def ledger(self,*names): return SimpleNamespace(events=[{'event':n} for n in names])
    def test_every_cue_real_pcm_and_channel(self):
        audio=ArcadeAudio()
        self.assertEqual(set(audio.sounds),set(PATTERNS))
        for name,sound in audio.sounds.items():
            self.assertAlmostEqual(sound.get_length(),PATTERNS[name][1],places=3)
            pcm=synthesize(name)
            self.assertGreater(len(set(pcm)),10)
        cues=audio.consume(self.ledger(*EVENT_CUES))
        self.assertEqual(set(cues),set(PATTERNS))
        self.assertTrue(all(pg.mixer.Channel(i).get_busy() for i in range(10)))
    def test_cursor_no_replay_and_new_match(self):
        a=ArcadeAudio(); ledger=self.ledger('match_start','dot')
        self.assertEqual(a.consume(ledger),['join','dot'])
        self.assertEqual(a.consume(ledger),[])
        ledger.events.append({'event':'player_hurt'})
        self.assertEqual(a.consume(ledger),['hurt'])
        self.assertEqual(a.consume(self.ledger('match_start')),['join'])
    def test_mute_discards_and_stops_existing(self):
        a=ArcadeAudio(); ledger=self.ledger('match_end')
        a.consume(ledger); self.assertTrue(pg.mixer.Channel(9).get_busy())
        ledger.events.append({'event':'dot'})
        self.assertEqual(a.consume(ledger,True),[])
        self.assertFalse(pg.mixer.Channel(9).get_busy())
        self.assertEqual(a.consume(ledger,False),[])
    def test_mixer_failure_and_shutdown_are_safe(self):
        pg.mixer.quit()
        with patch.object(pg.mixer,'init',side_effect=pg.error('unavailable')):
            a=ArcadeAudio()
        self.assertFalse(a.sounds)
        a.consume(self.ledger('match_start'))
        a=ArcadeAudio();pg.mixer.quit()
        a.consume(self.ledger('match_end'))
    def test_unsupported_mixer_format_is_silent(self):
        pg.mixer.init(22050,8,1)
        a=ArcadeAudio();self.assertFalse(a.sounds)
        a.consume(self.ledger('dot'))
    def test_mono_supported(self):
        pg.mixer.init(22050,-16,1)
        a=ArcadeAudio();self.assertEqual(len(a.sounds),10)
        a.consume(self.ledger('match_start'))
        self.assertTrue(pg.mixer.Channel(5).get_busy())
    def test_simultaneous_events_coalesce_without_losing_ledger(self):
        a=ArcadeAudio();ledger=self.ledger(*(['dot']*8+['player_hurt','bonus_life']))
        cues=a.consume(ledger)
        self.assertEqual(cues.count('dot'),8)
        self.assertTrue(all(pg.mixer.Channel(i).get_busy() for i in (0,2,7)))
        self.assertEqual(len(ledger.events),10)
    def test_f2_stops_immediately_in_lobby_without_match(self):
        app=App(simulate_controllers=True)
        app.audio.consume(self.ledger('match_end'))
        self.assertTrue(pg.mixer.Channel(9).get_busy())
        pg.event.post(pg.event.Event(pg.KEYDOWN,key=pg.K_F2,mod=0));app.events()
        self.assertTrue(app.muted)
        self.assertFalse(pg.mixer.Channel(9).get_busy())
    def test_render_loop_consumes_once_and_preserves_scores(self):
        app=App(simulate_controllers=True);app.count=8;app.start()
        app.match.paused=True
        scores=[p.score for p in app.match.players]
        ledger=list(app.match.ledger.events)
        original=app.audio.consume; consumed=[]
        def consume(*args,**kwargs):
            result=original(*args,**kwargs);consumed.append(result);return result
        with patch.object(app.audio,'consume',side_effect=consume):app.run(frames=3)
        self.assertEqual(len(consumed),3)
        self.assertIn('join',consumed[0])
        self.assertEqual(consumed[1:],[[],[]])
        self.assertEqual([p.score for p in app.match.players],scores)
        self.assertEqual(app.match.ledger.events,ledger)

    def test_all_counts_app_render_pause_and_restart(self):
        for count in range(1,9):
            with self.subTest(count=count):
                app=App(simulate_controllers=True);app.count=count;app.start()
                self.assertIn('join',app.audio.consume(app.match.ledger))
                before=len(app.match.ledger.events)
                app.draw();app.draw()
                self.assertEqual(len(app.match.ledger.events),before)
                self.assertEqual(app.audio.consume(app.match.ledger),[])
                app.station_action(count-1)
                self.assertIn('find',app.audio.consume(app.match.ledger))
                pg.event.post(pg.event.Event(pg.KEYDOWN,key=pg.K_p,mod=0));app.events()
                app.advance(.1)
                self.assertEqual(app.audio.consume(app.match.ledger),[])
                app.start()
                self.assertIn('join',app.audio.consume(app.match.ledger))
                pg.quit()

if __name__=='__main__':unittest.main(verbosity=2)
