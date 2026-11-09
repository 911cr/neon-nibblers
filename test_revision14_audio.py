"""Actual simulation events reach sound cues; dummy mixer is not audibility proof."""
import os
os.environ['SDL_VIDEODRIVER']='dummy'
os.environ['SDL_AUDIODRIVER']='dummy'
import unittest
import pygame as pg
from arcade_audio import ArcadeAudio
from game import Match

class ActualEventAudio(unittest.TestCase):
    def tearDown(self):pg.quit()
    def test_real_heart_and_threshold_life_events_emit_bonus_once(self):
        for kind in ('Heart','threshold'):
            g=Match(1,seed=1);p=g.players[0];audio=ArcadeAudio()
            audio.consume(g.ledger)
            if kind=='Heart':g.collect(p,'Heart')
            else:
                p.score=g.rules['bonus_threshold'];g.award_score_lives()
            cues=audio.consume(g.ledger)
            self.assertEqual(cues.count('bonus'),1)
            self.assertEqual(audio.consume(g.ledger),[])
            self.assertEqual(p.lives,4)

    def test_capped_life_does_not_claim_an_extra_life_sound(self):
        for kind in ('Heart','threshold'):
            g=Match(1,seed=1);p=g.players[0];p.lives=5;audio=ArcadeAudio()
            audio.consume(g.ledger)
            if kind=='Heart':g.collect(p,'Heart')
            else:p.score=g.rules['bonus_threshold'];g.award_score_lives()
            cues=audio.consume(g.ledger)
            self.assertNotIn('bonus',cues)
            if kind=='Heart':self.assertIn('power',cues)
            self.assertEqual(p.lives,5)

    def test_real_continue_emits_join_once_without_replaying_death(self):
        g=Match(1,seed=1,continue_seconds=10,continue_delay=0)
        audio=ArcadeAudio();audio.consume(g.ledger)
        p=g.players[0];p.lives=1;p.safe=0
        self.assertTrue(g.hurt(p));self.assertIn('hurt',audio.consume(g.ledger))
        self.assertTrue(g.continue_station(0));cues=audio.consume(g.ledger)
        self.assertEqual(cues,['join']);self.assertEqual(audio.consume(g.ledger),[])

if __name__=='__main__':unittest.main(verbosity=2)
