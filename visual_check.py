"""Build a reproducible visual contact sheet for every arena / 1,2,8 players."""
import os
os.environ['SDL_VIDEODRIVER']='dummy'
os.environ['SDL_AUDIODRIVER']='dummy'
import pygame as pg
from game import App, Match, THEMES

app=App(simulate_controllers=True);app.demo=True
sheet=pg.Surface((1920,1440))
for row,theme in enumerate(range(4)):
    for col,count in enumerate((1,2,8)):
        app.count=count;app.theme=theme;app.seed=10
        app.palette_override=4 if theme==0 else None
        app.start()
        for _ in range(90):app.advance(1/60);app.draw(1/60)
        sheet.blit(pg.transform.smoothscale(app.canvas,(640,360)),(col*640,row*360))

pg.image.save(sheet,'arena_checks.png')
pg.quit()

