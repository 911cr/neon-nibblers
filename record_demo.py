"""Record actual rendered game simulation. Requires Pillow (preview tool only)."""
import os
os.environ['SDL_VIDEODRIVER']='dummy'
os.environ['SDL_AUDIODRIVER']='dummy'
import pygame as pg
import argparse
from PIL import Image
from game import App, Match, steer_demo

app=App(); app.demo=True
frames=[]
parser=argparse.ArgumentParser()
parser.add_argument('--quick',action='store_true',help='12-second 8-player preview')
parser.add_argument('--players',type=int,choices=(1,2,8),help='Record a separate player-count demonstration')
parser.add_argument('--simulate-controllers',action='store_true',help='Label development controller availability as simulated')
parser.add_argument('--seconds',type=int,default=12)
args=parser.parse_args()
app.simulate_controllers=args.simulate_controllers
single=args.quick or args.players is not None
for theme in (range(1) if single else range(4)):
    for count in ((args.players or 8,) if single else (1,2,8)):
        app.match=Match(count,theme,seed=20+theme)
        app.visual_positions={}
        app.visual_foes={}; app.visual_items={}; app.score_memory={}; app.popups=[]
        # Capture 6 simulation seconds per scenario at 12 frames per second.
        for tick in range(args.seconds*60 if single else 360):
            steer_demo(app.match)
            app.match.update(1/60)
            app.draw()
            if tick%5==0:
                small=pg.transform.smoothscale(app.canvas,(960,540))
                frames.append(Image.frombytes('RGB',small.get_size(),pg.image.tobytes(small,'RGB')))
filename=f'gameplay_{args.players}_player.gif' if args.players else 'gameplay_preview.gif' if args.quick else 'gameplay.gif'
frames[0].save(filename,save_all=True,append_images=frames[1:],duration=83,loop=0,optimize=False)
pg.quit()
print('Recorded '+filename)
