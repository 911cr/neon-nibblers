"""Prevent score/life/start text from obscuring any station bay."""
import os
os.environ['SDL_VIDEODRIVER']='dummy'
os.environ['SDL_AUDIODRIVER']='dummy'
import unittest
from unittest.mock import patch
import pygame as pg
import game

class HudTests(unittest.TestCase):
    def test_actual_scores_and_prompts_clear_all_bays(self):
        app=game.App(simulate_controllers=True)
        for theme in range(4):
            app.theme=theme; app.count=8; app.start()
            bays=[]
            for spawn in app.match.arena.spawns:
                sx=game.center(spawn)[0]; upper=spawn[1]==0
                mouth=game.TOP+4 if upper else game.TOP+game.ROWS*game.TILE-4
                bays.append(pg.Rect(sx-25,mouth-35 if upper else mouth-1,50,36))
            for value in (0,999999,1000000,999999999):
                for p in app.match.players:p.score=value
                calls=[]; original=game.arcade_digits
                def capture(target,label,x,y,color,scale=3):
                    if ':' not in str(label): calls.append(pg.Rect(x,y,(6*len(str(label))-1)*scale,7*scale))
                    return original(target,label,x,y,color,scale)
                with patch.object(game,'arcade_digits',capture):app.draw()
                self.assertEqual(len(calls),8)
                for rect in calls:
                    self.assertTrue(pg.Rect(0,0,game.W,game.H).contains(rect))
                    self.assertFalse(any(rect.colliderect(b) for b in bays))
                for p in app.match.players:
                    self.assertFalse(any(game.station_hud(app.match.arena.spawns[p.idx],value)['lives'].colliderect(b) for b in bays))
            app.match.players[7].joined=False
            labels=[]; original_text=app.text
            def capture_text(s,x,y,color=(224,234,247),font=None):
                if '/ START' in str(s):labels.append((font or app.font).render(str(s),True,color).get_rect(topleft=(x,y)))
                return original_text(s,x,y,color,font)
            with patch.object(app,'text',capture_text):app.draw()
            self.assertTrue(labels)
            for rect in labels:self.assertFalse(any(rect.colliderect(b) for b in bays))
        pg.quit()

if __name__=='__main__':unittest.main(verbosity=2)
