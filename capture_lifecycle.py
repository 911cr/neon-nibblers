"""Optional Pillow tool: isolated original lifecycle animation storyboard."""
import os
os.environ.setdefault('SDL_VIDEODRIVER','dummy')
os.environ.setdefault('SDL_AUDIODRIVER','dummy')
from pathlib import Path
import pygame as pg
from PIL import Image,ImageDraw
from game import Match,center,COLORS,OX,TOP,COLS,ROWS,TILE,W,H
from arcade_art import muncher
from presentation import LifecyclePresentation


def main():
    pg.init()
    times=(0,.08,.16,.25,.35,.45)
    sheet=Image.new('RGB',(1200,760),(8,12,22));text=ImageDraw.Draw(sheet)
    for row,title in enumerate(('Growth: radius 17 to 36','Shrink: radius 36 to 17',
                                'Death: dissolve at previous position','Respawn: arrival pulse in bay')):
        text.text((9,row*190+5),title,fill=(230,236,245))
        g=Match(1,seed=12);p=g.players[0];fx=LifecyclePresentation();fx.update(g,0)
        if row in (0,1):
            g.collect(p,'Titan');fx.update(g,0)
            if row==1:
                fx.update(g,.25);p.effects.clear();fx.update(g,0)
        else:
            p.pos=(5,9);p.safe=0;g.hurt(p);fx.update(g,0)
        previous=0.
        for col,time in enumerate(times):
            fx.update(g,time-previous);previous=time
            frame=pg.Surface((W,H),pg.SRCALPHA)
            if row<2:
                point=(160,235)
                muncher(frame,point,COLORS[0],(1,0),time,fx.radius(0),row==0)
            else:
                point=center((5,9)) if row==2 else (center(g.arena.spawns[0])[0],TOP+ROWS*TILE+5)
                fx.draw_effects(frame,center,COLORS,pg.Rect(OX,TOP,COLS*TILE,ROWS*TILE),g.arena.portals)
                if row==3:
                    pg.draw.rect(frame,(125,132,145),(point[0]-24,TOP+ROWS*TILE-4,48,34),1,border_radius=7)
                    muncher(frame,point,COLORS[0],(0,-1),time,17,safe=True)
            raw=Image.frombytes('RGBA',(W,H),pg.image.tobytes(frame,'RGBA'))
            x,y=point
            crop=raw.crop((x-60,y-60,x+60,y+60)).resize((150,150))
            sheet.paste(crop,(col*200+25,row*190+36),crop)
            text.text((col*200+85,row*190+22),f'{time:.2f}s',fill=(230,236,245))
    path=Path(__file__).with_name('lifecycle_animation.png')
    sheet.save(path);pg.quit();print(path)


if __name__=='__main__':main()
