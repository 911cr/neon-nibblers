"""Optional independent spectator scoreboard. Its layout is original."""
import argparse
import json
from pathlib import Path
import time
import math
import pygame as pg

COLORS=[(255,222,45),(255,108,195),(75,226,245),(255,83,80),
        (111,235,90),(255,155,55),(185,109,255),(90,141,255)]

def read_feed(path):
    try:
        value=json.loads(Path(path).read_text(encoding='utf-8'))
        if value.get('schema_version')!=1 or not isinstance(value.get('ranking'),list):return None
        if type(value.get('updated')) not in (int,float) or not math.isfinite(value['updated']):return None
        if type(value.get('remaining')) not in (int,float) or not math.isfinite(value['remaining']) or not 0<=value['remaining']<=86400:return None
        if 'timed' in value and type(value['timed']) is not bool:return None
        if type(value.get('stage')) is not int or not 0<=value['stage']<=100000:return None
        if value.get('phase') not in ('attract','playing','paused','guide','results'):return None
        if not isinstance(value.get('map',''),str):return None
        value['map']=''.join(c for c in value.get('map','') if c.isprintable())[:80]
        rows=[]
        for row in value['ranking'][:8]:
            if not isinstance(row,dict) or any(type(row.get(k)) is not int for k in ('rank','player_id','score','lives')):return None
            if not 1<=row['player_id']<=8 or row['rank']<1 or row['score']<0 or row['lives']<0:return None
            rows.append(row)
        value['ranking']=rows
        return value
    except (OSError,ValueError,TypeError,AttributeError):return None

def draw_scoreboard(surface,feed,now=None):
    surface.fill((5,10,20));w,h=surface.get_size()
    title=pg.font.Font(None,max(24,int(h*.075)))
    font=pg.font.Font(None,max(18,int(h*.045)))
    small=pg.font.Font(None,max(15,int(h*.032)))
    def text(label,x,y,color=(225,235,250),f=font):surface.blit(f.render(str(label),True,color),(x,y))
    text('NEON NIBBLERS LIVE',w*.08,h*.045,(255,225,90),title)
    if feed is None:
        text('Waiting for the game feed...',w*.1,h*.3);return
    stale=(time.time() if now is None else now)-feed['updated']>3
    phase=str(feed.get('phase','')).upper()
    text(('FEED DISCONNECTED  |  ' if stale else '')+phase,w*.08,h*.15,(255,170,95) if stale else (110,235,215),small)
    remaining=max(0,int(feed.get('remaining',0)))
    timer=f'{remaining//60}:{remaining%60:02}' if feed.get('timed',True) else 'LIFE SURVIVAL'
    text(f"{feed.get('map','')}   STAGE {feed.get('stage',0)}   {timer}",w*.08,h*.21,f=small)
    rows=feed['ranking']
    if not rows:text('Press Start at a station to join.',w*.1,h*.4)
    for i,row in enumerate(rows):
        y=h*(.31+i*.073);color=COLORS[row['player_id']-1]
        text(f"{row['rank']:>2}   P{row['player_id']}",w*.1,y,color)
        text(f"{row['score']:06}",w*.48,y,color)
        text(f"{row['lives']} lives",w*.76,y,color)
    text('Independent spectator view  |  Escape closes',w*.08,h*.94,f=small)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--state',required=True,type=Path)
    parser.add_argument('--frames',type=int,default=0)
    parser.add_argument('--width',type=int,default=960)
    parser.add_argument('--height',type=int,default=720)
    parser.add_argument('--mode',choices=('auto','game','scores'),default='auto',help='Auto mirrors active play and shows rankings otherwise; exact DX behavior by state is unverified.')
    parser.add_argument('--capture',type=Path,help='Save the final spectator frame for verification.')
    args=parser.parse_args()
    if args.width<640 or args.height<480:parser.error('Minimum window size is640x480')
    pg.init();screen=pg.display.set_mode((args.width,args.height),pg.RESIZABLE)
    pg.display.set_caption('Neon Nibblers | Spectator');clock=pg.time.Clock();running=True;n=0
    while running:
        for event in pg.event.get():
            if event.type==pg.QUIT or event.type==pg.KEYDOWN and event.key==pg.K_ESCAPE:running=False
        feed=read_feed(args.state)
        show_game=args.mode=='game' or args.mode=='auto' and feed and feed['phase'] in ('playing','paused','guide')
        frame=args.state.with_suffix('.frame.jpg')
        mirrored=False
        if show_game and feed and time.time()-feed['updated']<=3:
            try:
                image=pg.image.load(str(frame));iw,ih=image.get_size();sw,sh=screen.get_size()
                factor=min(sw/iw,sh/ih);size=(max(1,round(iw*factor)),max(1,round(ih*factor)))
                screen.fill((0,0,0));screen.blit(pg.transform.smoothscale(image,size),((sw-size[0])//2,(sh-size[1])//2))
                mirrored=True
            except (OSError,pg.error,ZeroDivisionError):pass
        if not mirrored:draw_scoreboard(screen,feed)
        pg.display.flip();clock.tick(30);n+=1
        if args.frames and n>=args.frames:break
    if args.capture:pg.image.save(screen,str(args.capture))
    pg.quit()

if __name__=='__main__':main()
