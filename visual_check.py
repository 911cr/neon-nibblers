"""Build a reproducible visual contact sheet for every arena / 1,2,8 players."""
import os
os.environ['SDL_VIDEODRIVER']='dummy'
os.environ['SDL_AUDIODRIVER']='dummy'
import pygame as pg
from game import App, Match, THEMES

app=App()
sheet=pg.Surface((1920,1440))
for row,theme in enumerate(range(4)):
    for col,count in enumerate((1,2,8)):
        app.match=Match(count,theme,seed=10)
        app.visual_positions={}; app.visual_foes={}; app.visual_items={}; app.score_memory={}; app.popups=[]
        app.draw()
        sheet.blit(pg.transform.smoothscale(app.canvas,(640,360)),(col*640,row*360))

pg.image.save(sheet,'arena_checks.png')
pg.quit()

