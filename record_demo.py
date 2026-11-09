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
parser.add_argument('--players',type=int,choices=range(1,9),help='Record a separate player-count demonstration')
parser.add_argument('--simulate-controllers',action='store_true',help='Label development controller availability as simulated')
parser.add_argument('--seconds',type=int,default=12)
parser.add_argument('--theme',type=int,choices=range(4),default=0,help='Starting map index for a single-count capture')
parser.add_argument('--tour',action='store_true',help='Show every map for the selected player count; --seconds is time per map')
parser.add_argument('--untimed',action='store_true',help='Show the optional life-survival mode.')
args=parser.parse_args()
app.simulate_controllers=args.simulate_controllers
app.untimed=args.untimed
single=args.quick or args.players is not None
for theme in (range(4) if args.tour or not single else (args.theme,)):
    for count in ((args.players or 8,) if single else (1,2,8)):
        app.count=count;app.theme=theme;app.seed=20+theme;app.start()
        # Capture 6 simulation seconds per scenario at 12 frames per second.
        for tick in range(args.seconds*60 if single else 360):
            if tick==120:
                app.station_action(0)  # Show the independently drawn locator in real play.
            app.advance(1/60)
            app.draw()
            if tick%5==0:
                small=pg.transform.smoothscale(app.canvas,(960,540))
                frames.append(Image.frombytes('RGB',small.get_size(),pg.image.tobytes(small,'RGB')))
filename=f'gameplay_{args.players}_player.gif' if args.players else 'gameplay_preview.gif' if args.quick else 'gameplay.gif'
frames[0].save(filename,save_all=True,append_images=frames[1:],duration=83,loop=0,optimize=False)
pg.quit()
print('Recorded '+filename)
