"""Neon Nibblers — original local arcade maze battle. Python 3.10+."""
import os
import sys
import math
import random
import argparse
from collections import deque
from array import array
from dataclasses import dataclass, field
import pygame as pg
from arcade_art import maze_background, muncher, foe, power_icon, arcade_digits, dot_sprite

W, H, TILE, TOP = 1280, 720, 20, 45
COLS, ROWS = 59, 31
OX = (W - COLS * TILE) // 2
GATE_HATCH=(238,221,85)  # Yellow thresholds observed even on cyan Deluxe mazes.
COLORS = [(255,222,45),(255,108,195),(75,226,245),(255,83,80),
          (111,235,90),(255,155,55),(185,109,255),(90,141,255)]
DIRS = [(1,0),(-1,0),(0,1),(0,-1)]
THEMES = [('Golden Junction',(238,221,85)),('Violet Switchback',(194,117,255)),
          ('Ember Crossroads',(255,140,71)),('Cyan Circuit',(75,227,239))]
SPAWN_INTERVAL=3.0  # Custom tuning; commercial cadence is not published.
MAX_ITEMS=12
ITEM_STEP_INTERVAL=.24
ITEMS = {
 'Crown': ('CR','Hunt foes for 7s.'),
 'Titan': ('TI','Grow giant and eat smaller rivals for 7s.'),
 'Rush': ('RU','Move faster for 7s.'),
 'Mist': ('MI','Leave a smoke trail that slows foes.'),
 'Slick': ('SL','Skid uncontrollably for 2 seconds.'),
 'Spark': ('SP','Zap nearby rivals and foes.'),
 'Veil': ('VE','Ghosts cannot track you; rivals still can.'),
 'Flare': ('FL','Breathe fire down your corridor.'),
 'Quake': ('QU','Slow everyone with a quake.'),
 'Heart': ('HE','Gain a life, up to 5.'),
 'Lure': ('LU','Carry a captured ghost as a weapon.')}
DISPLAY_NAMES={'Crown':'Gold Orb','Titan':'Giant Orb','Rush':'Caffeine','Mist':'Smoke Bomb',
               'Slick':'Banana Peel','Spark':'Lightning','Veil':'Ghost Sheet','Flare':'Chili Pepper',
               'Quake':'Earthquake','Heart':'Extra Life','Lure':'Ghost Magnet'}
KEYS = [(pg.K_RIGHT,pg.K_LEFT,pg.K_DOWN,pg.K_UP),
        (pg.K_d,pg.K_a,pg.K_s,pg.K_w),(pg.K_l,pg.K_j,pg.K_k,pg.K_i),
        (pg.K_KP6,pg.K_KP4,pg.K_KP2,pg.K_KP8),
        (pg.K_h,pg.K_f,pg.K_g,pg.K_t),(pg.K_v,pg.K_x,pg.K_c,pg.K_e),
        (pg.K_n,pg.K_b,pg.K_m,pg.K_y),(pg.K_6,pg.K_4,pg.K_5,pg.K_8)]
KEYLABELS = ['Arrows','WASD','IJKL','Numpad 8246','TFGH','EXCV','YBNM','8456']

@dataclass
class Player:
    idx: int
    pos: tuple
    lives: int = 3
    score: int = 0
    direction: tuple = (0,0)
    wanted: tuple = (0,0)
    clock: float = 0
    effects: dict = field(default_factory=dict)
    safe: float = 2.5
    stun: float = 0
    last: str = ''
    entry: float = 0.
    bonus_life: bool = False

class Arena:
    def __init__(self, theme):
        self.theme = theme
        self.floor = {(x,y) for y in range(1,ROWS-1) for x in range(1,COLS-1)}
        # Original narrow-stroke L/T/U wall forms, based on visual study of
        # the arcade genre, not a traced or extracted commercial maze.
        paths = [
            [(3,3),(10,3)], [(15,3),(15,3)], [(35,3),(35,3)], [(42,3),(51,3)],
            [(13,7),(19,7),(19,3),(31,3),(31,7),(38,7)],
            [(3,7),(6,7)], [(9,7),(10,7)], [(42,7),(46,7)], [(50,7),(53,7)],
            [(3,15),(3,11),(10,11)], [(6,15),(17,15)], [(13,11),(20,11)],
            [(23,7),(28,7)], [(23,11),(30,11)], [(34,11),(42,11)],
            [(46,11),(53,11),(53,15)], [(20,15),(20,19)], [(35,15),(35,19)],
            [(3,19),(3,23)], [(6,19),(9,19),(9,22)],
            [(17,19),(13,19),(13,25),(19,25),(19,28)],
            [(23,23),(30,23)], [(23,27),(30,27)],
            [(35,27),(35,23),(39,23)], [(39,18),(42,18),(42,22)],
            [(46,23),(46,18),(50,18)], [(53,19),(53,23),(50,23)],
            [(3,27),(7,27),(7,24)], [(10,27),(16,27)],
            [(39,27),(46,27)], [(50,27),(53,27)]]
        if theme==1:
            paths=[[(COLS-1-x,y) for x,y in path] for path in paths]
        elif theme==2:
            paths=[[(x,ROWS-1-y) for x,y in path] for path in paths]
        elif theme==3:
            paths=[[(COLS-1-x,ROWS-1-y) for x,y in path] for path in paths]
            paths[1]=[(13,3),(17,3),(17,5)]
        # One center-line graph is the source of truth for collision AND art.
        # Wall vertices snap between lanes, never onto a movement center-line.
        snap=lambda n: max(3,4*int((n-3)/4+.5)+3)
        blocked=set()
        for path in paths:
            path=[(snap(x),snap(y)) for x,y in path]
            for a,b in zip(path,path[1:]):
                dx=0 if a[0]==b[0] else (1 if b[0]>a[0] else -1)
                dy=0 if a[1]==b[1] else (1 if b[1]>a[1] else -1)
                c=a; blocked.add(c)
                while c!=b:
                    c=add(c,(dx,dy)); blocked.add(c)
        self.den=(23,15,9,5)
        blocked.update((x,y) for x in range(23,32) for y in range(15,20))
        nodes={(x,y) for x in range(1,COLS-1,4) for y in range(1,ROWS-1,4)
               if (x,y) not in blocked}
        edges=[]
        for x,y in sorted(nodes):
            for dx,dy in ((1,0),(0,1)):
                end=(x+4*dx,y+4*dy)
                cells={(x+i*dx,y+i*dy) for i in range(5)}
                if end in nodes and not cells & blocked: edges.append(((x,y),end,cells))
        # Eliminate blind approach stubs at wall ends. All visible corridors are
        # traversable; no invisible modulo-grid restrictions or painted openings.
        changed=True
        while changed:
            degrees={n:0 for n in nodes}
            for a,b,_ in edges: degrees[a]+=1; degrees[b]+=1
            ends={n for n,d in degrees.items() if d<2}
            changed=bool(ends)
            if changed:
                nodes-=ends; edges=[e for e in edges if not ({e[0],e[1]} & ends)]
        self.lanes=set().union(*(e[2] for e in edges))
        self.entries=[(5,29),(53,29),(53,1),(5,1),(17,29),(29,29),(41,1),(17,1)]
        self.spawns=[(x,0 if y==1 else ROWS-1) for x,y in self.entries]
        self.gate_owner={c:i for i,c in enumerate(self.spawns)}
        self.portals=(9,25)
        for y in self.portals:
            self.lanes.update(((0,y),(1,y),(COLS-2,y),(COLS-1,y)))
        self.floor=self.lanes | set(self.spawns)
        self.space=self.floor  # renderer receives precisely the movement graph
        seen={self.entries[0]}; queue=list(seen)
        while queue:
            c=queue.pop()
            for d in DIRS:
                n=self.step(c,d)
                if n in self.floor and n not in seen: seen.add(n); queue.append(n)
        assert seen==self.floor, 'Disconnected authored corridor'
        assert all(c in self.lanes for c in self.entries), 'Disconnected gate'

    def can_enter(self, cell, player):
        return cell in self.floor and self.gate_owner.get(cell,player.idx)==player.idx

    def step(self,pos,direction):
        target=add(pos,direction)
        if pos[1] in self.portals and target[0] in (-1,COLS):
            target=(target[0]%COLS,target[1])
        return target

class Match:
    def __init__(self, count=2, theme=0, seed=None):
        self.rng = random.Random(seed)
        self.count, self.stage = count, 1
        self.time, self.item_clock, self.foe_clock = 180., 0., 0.
        self.item_walk_clock=0.; self.item_directions={}
        self.over, self.paused = False, False
        self.players = [Player(i,(0,0)) for i in range(count)]
        self.new_arena(theme)

    def new_arena(self, theme):
        self.arena = Arena(theme%4)
        self.dots = set(self.arena.lanes) - set(self.arena.entries)
        self.items, self.traps = {}, {}
        self.smoke={}; self.quake=0.; self.bump_cooldowns={}
        self.zaps=[]
        self.item_directions={}
        self.item_clock=self.item_walk_clock=0.
        for p in self.players:
            p.pos = self.arena.spawns[p.idx]
            p.safe, p.direction, p.wanted = 2.5, (0,1) if p.pos[1]==0 else (0,-1), (0,0)
            p.entry=.8; p.stun=0.; p.clock=0.
            p.effects.clear()
        exits=[c for c in ((21,17),(33,17),(25,13),(29,21),(21,13)) if c in self.arena.floor]
        self.foes = [(24+i*2,17) for i in range(4)]
        self.foe_modes=['house']*4
        self.foe_release=[.9+i*.6 for i in range(4)]
        self.foe_carriers={}
        self.foe_ticks=[0.]*4
        self.foe_zapped=[0.]*4
        self.foe_stun = 0.
        self.foe_clock=0.
        for c in ((1,1),(COLS-2,1),(1,ROWS-2),(COLS-2,ROWS-2)):
            if c in self.arena.floor: self.items[c]='Crown'
        for anchor in ((COLS//2,9),(COLS//2,21)):
            c=min(self.arena.lanes,key=lambda c:(distance(c,anchor),c))
            self.items[c]='Titan'
        for name in self.rng.sample([k for k in ITEMS if k not in ('Crown','Titan')],3): self.spawn_item(name)

    def spawn_item(self, name=None):
        if len(self.items)>=MAX_ITEMS: return
        cells = sorted(self.arena.lanes - set(self.items) - {p.pos for p in self.players})
        if cells: self.items[self.rng.choice(cells)] = name or self.rng.choice(list(ITEMS))

    def reset_foe(self, index, returning=True):
        self.foe_carriers.pop(index,None)
        self.foe_modes[index]='eyes' if returning else 'house'
        self.foe_release[index]=1.2
        if not returning: self.foes[index]=(24+index*2,17)

    def next_toward(self, start, goal):
        queue=deque([(start,None)]); seen={start}
        while queue:
            cell,first=queue.popleft()
            if cell==goal: return first or start
            for d in DIRS:
                nxt=self.arena.step(cell,d)
                if nxt in self.arena.lanes and nxt not in seen:
                    seen.add(nxt); queue.append((nxt,first or nxt))
        return start

    def sync_carriers(self):
        for i,owner in list(self.foe_carriers.items()):
            holder=self.players[owner]
            if holder.lives<=0 or not self.active(holder,'Lure'):
                self.reset_foe(i)
            else:
                candidate=self.arena.step(holder.pos,holder.direction)
                self.foes[i]=candidate if candidate in self.arena.lanes else holder.pos

    def update_foes(self, dt):
        self.sync_carriers()
        self.foe_clock+=dt
        self.foe_stun=max(0,self.foe_stun-dt)
        for i in range(len(self.foes)):
            self.foe_release[i]=max(0,self.foe_release[i]-dt)
            self.foe_ticks[i]+=dt
            self.foe_zapped[i]=max(0,self.foe_zapped[i]-dt)
        if self.foe_clock<.16: return
        self.foe_clock=0
        for i,f in enumerate(self.foes):
            mode=self.foe_modes[i]
            if mode=='carried':
                holder=self.players[self.foe_carriers[i]]
                if holder.lives<=0 or not self.active(holder,'Lure'):
                    self.reset_foe(i)
                else:
                    candidate=self.arena.step(holder.pos,holder.direction)
                    self.foes[i]=candidate if candidate in self.arena.lanes else holder.pos
                continue
            if mode=='house':
                if self.foe_release[i]>0: continue
                self.foe_modes[i]='leaving'
                mode='leaving'
            if mode=='leaving':
                x,y=f
                if x!=27: self.foes[i]=(x+(1 if x<27 else -1),y)
                elif y>13: self.foes[i]=(x,y-1)
                else: self.foe_modes[i]='roaming'
                continue
            if mode=='entering':
                x,y=f; home=24+i*2
                if y<17: self.foes[i]=(x,y+1)
                elif x!=home: self.foes[i]=(x+(1 if x<home else -1),y)
                else:
                    self.foe_modes[i]='house'; self.foe_release[i]=1.2
                continue
            if mode=='eyes':
                if f==(27,13):
                    self.foe_modes[i]='entering'
                else: self.foes[i]=self.next_toward(f,(27,13))
                continue
            slow=2 if self.quake>0 else 1
            if any(distance(f,c)<=2 for c in self.smoke): slow*=2
            if self.foe_stun>0 or self.foe_zapped[i]>0 or self.foe_ticks[i]<.16*slow: continue
            self.foe_ticks[i]=0.
            targets=[p for p in self.players if p.lives>0 and p.pos in self.arena.lanes
                     and not self.active(p,'Veil')]
            options=[self.arena.step(f,d) for d in DIRS if self.arena.step(f,d) in self.arena.lanes]
            if not options: continue
            if targets and self.rng.random()<.7:
                target=min(targets,key=lambda p:distance(p.pos,f))
                options.sort(key=lambda c:distance(c,target.pos),reverse=self.active(target,'Crown') or self.active(target,'Titan'))
                self.foes[i]=options[0]
            else: self.foes[i]=self.rng.choice(options)

    def active(self,p,key): return p.effects.get(key,0)>0

    def hurt(self,p):
        if p.lives<=0 or p.safe>0 or self.active(p,'Titan'): return False
        p.lives -= 1
        p.pos, p.safe = self.arena.spawns[p.idx], 3.
        p.direction, p.wanted = (0,0),(0,0)
        p.entry=.8; p.stun=0.; p.clock=0.
        p.effects.clear()
        return True

    def collect(self,p,name):
        p.score += 75
        p.last = name
        if name == 'Heart': p.lives = min(5,p.lives+1)
        elif name=='Spark':
            self.zaps.append((p.pos,.5))
            for q in self.players:
                if q is not p and distance(q.pos,p.pos)<=8: q.stun=2.
            for i,f in enumerate(self.foes):
                if distance(f,p.pos)<=8: self.foe_zapped[i]=2.
        elif name=='Quake': self.quake=5.
        elif name=='Slick': p.effects[name]=2.
        elif name=='Flare': p.effects[name]=3.
        else: p.effects[name]=7.

    def fire_cells(self, p):
        cells=[]; c=p.pos
        if p.direction==(0,0): return cells
        for _ in range(5):
            c=self.arena.step(c,p.direction)
            if c not in self.arena.lanes: break
            cells.append(c)
        return cells

    def apply_fire(self):
        for p in self.players:
            if p.lives<=0 or not self.active(p,'Flare'): continue
            cells=self.fire_cells(p)
            for i,f in enumerate(self.foes):
                if f in cells and self.foe_modes[i]=='roaming':
                    p.score+=200; self.reset_foe(i)
            for q in self.players:
                if q is not p and q.pos in cells and self.hurt(q): p.score+=300

    def bump(self,p,q,previous):
        pair=tuple(sorted((p.idx,q.idx)))
        crossed=previous and previous[p.idx]!=previous[q.idx] and previous[p.idx]==q.pos and previous[q.idx]==p.pos
        if crossed:
            # Rewind a head-on swap before applying the outward impulse.
            p.pos,q.pos=previous[p.idx],previous[q.idx]
            for actor in (p,q):
                reverse=(-actor.direction[0],-actor.direction[1])
                other=q if actor is p else p
                cell=self.arena.step(actor.pos,reverse)
                if self.arena.can_enter(cell,actor) and cell!=other.pos: actor.pos=cell
                actor.direction=actor.wanted=reverse; actor.stun=.12
            self.bump_cooldowns[pair]=.28
            return
        if pair in self.bump_cooldowns and p.pos!=q.pos: return
        self.bump_cooldowns[pair]=.28
        occupied={r.pos for r in self.players if r.lives>0}
        for actor,other in ((p,q),(q,p)):
            options=[self.arena.step(actor.pos,d) for d in DIRS
                     if self.arena.can_enter(self.arena.step(actor.pos,d),actor)
                     and self.arena.step(actor.pos,d) not in occupied]
            if not options: continue
            chosen=max(options,key=lambda c:distance(c,other.pos))
            actor.direction=(chosen[0]-actor.pos[0],chosen[1]-actor.pos[1])
            if abs(actor.direction[0])>1: actor.direction=(-1 if actor.direction[0]>0 else 1,0)
            actor.wanted=actor.direction; actor.pos=chosen; actor.stun=.12
            occupied.add(chosen)

    def separate_overlaps(self):
        # Resolve a crowd without leaving multiple living bodies in one cell.
        occupied=set()
        for p in self.players:
            if p.lives<=0: continue
            if p.pos in occupied:
                queue=deque([p.pos]); seen={p.pos}
                while queue:
                    c=queue.popleft()
                    if c not in occupied:
                        p.pos=c; p.stun=max(p.stun,.12); break
                    for d in DIRS:
                        nxt=self.arena.step(c,d)
                        if self.arena.can_enter(nxt,p) and nxt not in seen:
                            seen.add(nxt); queue.append(nxt)
            occupied.add(p.pos)

    def award_score_lives(self):
        for p in self.players:
            if p.score>=10000 and not p.bonus_life:
                p.bonus_life=True
                if p.lives>0: p.lives=min(5,p.lives+1)

    def combat(self,previous=None,old_foes=None):
        for p in self.players:
            if p.lives<=0: continue
            for i,f in enumerate(self.foes):
                crossed=previous and old_foes and previous[p.idx]==f and p.pos==old_foes[i]
                if (p.pos!=f and not crossed) or self.foe_modes[i] in ('eyes','entering','house','leaving'): continue
                if self.foe_modes[i]=='carried':
                    owner=self.foe_carriers[i]
                    if self.players[owner].lives<=0 or not self.active(self.players[owner],'Lure'):
                        self.reset_foe(i); continue
                    if owner!=p.idx and self.hurt(p): self.players[owner].score+=300
                    continue
                if self.active(p,'Lure'):
                    self.foe_carriers[i]=p.idx; self.foe_modes[i]='carried'; continue
                if self.active(p,'Crown') or self.active(p,'Titan'):
                    p.score += 200
                    self.reset_foe(i)
                else: self.hurt(p)
        for i,p in enumerate(self.players):
            for q in self.players[i+1:]:
                if min(p.lives,q.lives)<=0: continue
                crossed = previous and previous[p.idx]==q.pos and previous[q.idx]==p.pos
                if p.pos!=q.pos and not crossed: continue
                a = self.active(p,'Titan')
                b = self.active(q,'Titan')
                if a and not b and self.hurt(q): p.score+=300
                if b and not a and self.hurt(p): q.score+=300
                if a==b: self.bump(p,q,previous)
        self.separate_overlaps()

    def update(self,dt):
        if self.over or self.paused: return []
        sounds=[]
        self.time=max(0,self.time-dt)
        previous=[p.pos for p in self.players]
        old_foes=list(self.foes)
        self.quake=max(0,self.quake-dt)
        self.smoke={c:t-dt for c,t in self.smoke.items() if t>dt}
        self.zaps=[(c,t-dt) for c,t in self.zaps if t>dt]
        self.bump_cooldowns={pair:t-dt for pair,t in self.bump_cooldowns.items() if t>dt}
        for p in self.players:
            p.safe=max(0,p.safe-dt); p.stun=max(0,p.stun-dt)
            for k in list(p.effects):
                p.effects[k]-=dt
                if p.effects[k]<=0: del p.effects[k]
            if p.lives<=0 or p.stun>0: continue
            if p.entry>0 and p.pos==self.arena.spawns[p.idx]:
                p.entry=max(0,p.entry-dt)
                if p.entry==0:
                    p.pos=self.arena.entries[p.idx]
                    p.direction=(0,1) if p.pos[1]==1 else (0,-1)
                continue
            p.entry=0
            p.clock+=dt
            speed=.065 if self.active(p,'Rush') else .10
            if self.active(p,'Slick'): speed=.055
            if self.quake>0: speed*=2
            if p.clock>=speed:
                p.clock=0
                if self.active(p,'Slick'):
                    if not self.arena.can_enter(self.arena.step(p.pos,p.direction),p) or p.direction==(0,0):
                        options=[d for d in DIRS if self.arena.can_enter(self.arena.step(p.pos,d),p)]
                        if options: p.direction=self.rng.choice(options)
                elif self.arena.can_enter(self.arena.step(p.pos,p.wanted),p): p.direction=p.wanted
                if self.active(p,'Mist') and p.pos in self.arena.lanes: self.smoke[p.pos]=2.5
                if self.arena.can_enter(self.arena.step(p.pos,p.direction),p): p.pos=self.arena.step(p.pos,p.direction)
                if p.pos in self.dots:
                    self.dots.remove(p.pos); p.score+=10; sounds.append('dot')
                if p.pos in self.items:
                    self.collect(p,self.items.pop(p.pos)); sounds.append('power')
                if p.pos in self.traps and self.traps[p.pos][0]!=p.idx:
                    p.stun=1.5; del self.traps[p.pos]
        self.update_foes(dt)
        lives=sum(p.lives for p in self.players)
        self.combat(previous,old_foes)
        self.apply_fire()
        self.award_score_lives()
        if sum(p.lives for p in self.players)<lives: sounds.append('hurt')
        for cell,(owner,t) in list(self.traps.items()):
            if t<=dt: del self.traps[cell]
            else: self.traps[cell]=(owner,t-dt)
        self.item_clock+=dt
        if self.item_clock>=SPAWN_INTERVAL:
            self.item_clock=0
            if len(self.items)<MAX_ITEMS: self.spawn_item()
        self.item_walk_clock+=dt
        if self.item_walk_clock>=ITEM_STEP_INTERVAL:
            self.item_walk_clock=0
            moved={}; directions={}
            occupied=set(self.items)
            for cell,name in list(self.items.items()):
                target=cell; direction=self.item_directions.get(cell)
                if name not in ('Crown','Titan'):
                    options=[d for d in DIRS if self.arena.step(cell,d) in self.arena.lanes
                             and self.arena.step(cell,d) not in occupied
                             and self.arena.step(cell,d) not in moved]
                    if options:
                        direction=direction if direction in options and self.rng.random()<.8 else self.rng.choice(options)
                        target=self.arena.step(cell,direction)
                moved[target]=name; directions[target]=direction
            self.items=moved; self.item_directions=directions
        if self.time<=0 or not any(p.lives>0 for p in self.players): self.over=True
        elif not self.dots:
            for p in self.players:
                if p.lives>0: p.score+=500
            self.stage+=1
            self.new_arena(self.arena.theme+1)
            self.award_score_lives()
            sounds.append('power')
        return sounds

def add(a,b): return a[0]+b[0],a[1]+b[1]
def distance(a,b): return abs(a[0]-b[0])+abs(a[1]-b[1])
def center(c): return OX+c[0]*TILE+TILE//2,TOP+c[1]*TILE+TILE//2

class App:
    def __init__(self, simulate_controllers=False):
        pg.init()
        self.screen=pg.display.set_mode((W,H),pg.RESIZABLE)
        pg.display.set_caption('Neon Nibblers | Local Maze Battle')
        icon=pg.Surface((64,64),pg.SRCALPHA)
        muncher(icon,(32,32),COLORS[0],(1,0),.1,24)
        pg.display.set_icon(icon)
        self.canvas=pg.Surface((W,H))
        self.font=pg.font.Font(None,25); self.small=pg.font.Font(None,20)
        self.big=pg.font.Font(None,65)
        self.clock=pg.time.Clock(); self.running=True
        self.count=2; self.theme=0; self.match=None; self.help=False; self.muted=False
        self.simulate_controllers=simulate_controllers
        self.controller_notice_until=0
        self.pads={}; self.refresh_pads(); self.sounds={}
        self.demo=False; self.visual_positions={}; self.animation_time=0.
        self.backgrounds={}; self.visual_foes={}; self.score_memory={}; self.popups=[]; self.visual_items={}
        self.micro=pg.font.Font(None,16)
        try:
            if not pg.mixer.get_init(): pg.mixer.init(44100,-16,1)
            rate,_,channels=pg.mixer.get_init()
            for name,freq,dur in [('dot',640,.035),('power',980,.18),('hurt',140,.22)]:
                samples=array('h')
                for i in range(int(rate*dur)):
                    v=int(3500*math.sin(2*math.pi*freq*i/rate)*(1-i/(rate*dur)))
                    samples.extend([v]*channels)
                self.sounds[name]=pg.mixer.Sound(buffer=samples)
        except pg.error: pass

    def refresh_pads(self):
        previous=set(self.pads)
        for i in range(pg.joystick.get_count()):
            joy=pg.joystick.Joystick(i)
            self.pads[joy.get_instance_id()]=joy
        self.pads={k:v for k,v in self.pads.items() if v.get_init() and v.get_attached()}
        if previous-set(self.pads): self.controller_notice_until=pg.time.get_ticks()+5000
        elif set(self.pads)-previous: self.controller_notice_until=0

    def controller_status(self):
        expected=self.match.count if self.match else self.count
        actual=min(8,len(self.pads))
        simulated=self.simulate_controllers
        effective=expected if simulated else actual
        missing=max(0,expected-effective)
        disconnected=not simulated and pg.time.get_ticks()<self.controller_notice_until
        if simulated:
            message=f'DEV: {expected} controllers assumed connected (SIMULATED)'
        elif disconnected:
            message=f'Controller disconnected | {actual}/{expected} connected | keyboard fallback available'
        elif missing:
            message=f'Missing {missing} of {expected} controllers | {actual} connected | keyboard fallback available'
        else:
            message=f'{actual} controllers connected | {expected} players'
        return {'expected':expected,'actual':actual,'effective':effective,'missing':missing,
                'simulated':simulated,'disconnected':disconnected,'message':message}

    def text(self,s,x,y,color=(224,234,247),font=None):
        self.canvas.blit((font or self.font).render(str(s),True,color),(x,y))

    def events(self):
        for e in pg.event.get():
            if e.type==pg.QUIT: self.running=False
            if e.type in (pg.JOYDEVICEADDED,pg.JOYDEVICEREMOVED): self.refresh_pads()
            if e.type==pg.JOYBUTTONDOWN and e.button==0 and (self.match is None or self.match.over): self.start()
            if e.type!=pg.KEYDOWN: continue
            if self.match and not self.match.over:
                for p in self.match.players:
                    for k,d in zip(KEYS[p.idx],DIRS):
                        if e.key==k: p.wanted=d
            if e.key==pg.K_ESCAPE:
                if self.help: self.help=False
                elif self.match: self.match=None
                else: self.running=False
            elif e.key==pg.K_F1: self.help=not self.help
            elif e.key==pg.K_F2: self.muted=not self.muted
            elif e.key==pg.K_RETURN and (not self.match or self.match.over): self.start()
            elif e.key==pg.K_p and self.match: self.match.paused=not self.match.paused
            elif not self.match:
                if pg.K_1<=e.key<=pg.K_8: self.count=e.key-pg.K_0
                if e.key==pg.K_TAB: self.theme=(self.theme+1)%4

    def start(self):
        self.match=Match(self.count,self.theme); self.help=False
        self.visual_positions={}; self.visual_foes={}; self.score_memory={}; self.popups=[]; self.visual_items={}

    def inputs(self):
        keys=pg.key.get_pressed()
        pads=list(self.pads.values())[:8]
        for p in self.match.players:
            wanted=None
            for k,d in zip(KEYS[p.idx],DIRS):
                if keys[k]: wanted=d
            if p.idx<len(pads):
                joy=pads[p.idx]
                x=joy.get_axis(0) if joy.get_numaxes()>0 else 0
                y=joy.get_axis(1) if joy.get_numaxes()>1 else 0
                if joy.get_numhats():
                    hx,hy=joy.get_hat(0)
                    if hx or hy: x,y=hx,-hy
                if max(abs(x),abs(y))>.35:
                    wanted=(1 if x>0 else -1,0) if abs(x)>abs(y) else (0,1 if y>0 else -1)
            if wanted: p.wanted=wanted

    def draw(self):
        self.canvas.fill((0,0,4))
        self.animation_time+=1/60
        if not self.match:
            for i in range(8):
                muncher(self.canvas,(325+i*90,190),COLORS[i],(1,0),self.animation_time+i,25)
            self.text('NEON NIBBLERS',W//2-200,58,(255,222,72),self.big)
            self.text('A snack-sized rivalry. An oversized appetite.',W//2-185,125)
            status=self.controller_status()
            message=status['message']
            color=(255,188,87) if status['missing'] or status['disconnected'] else (134,204,244)
            self.text(message,(W-self.small.size(message)[0])//2,242,color,self.small)
            self.text('Press 1-8 to choose players. TAB changes starting arena.',W//2-245,280)
            self.text('Arena: '+THEMES[self.theme][0],W//2-125,317,COLORS[self.theme])
            self.text('ENTER or controller button 1 to start',W//2-160,365)
            self.text('Collect dots. Claim powers. Outscore your friends in 3 minutes.',W//2-265,408)
            for i in range(8):
                self.text(f'P{i+1}  {KEYLABELS[i]}',W//2-190+(i//4)*300,462+(i%4)*33,COLORS[i])
            self.text('Controllers map to P1-P8 in connection order. Keyboard also works.',W//2-280,620)
            self.text('F1: power guide   |   F2: sound   |   ESC: quit',W//2-190,667)
        else:
            g=self.match
            accent=THEMES[g.arena.theme][1]
            if g.arena.theme not in self.backgrounds:
                self.backgrounds[g.arena.theme]=maze_background(g.arena.space,COLS,ROWS,TILE,accent)
            self.canvas.blit(self.backgrounds[g.arena.theme],(OX,TOP))
            # Thin enclosure and colored border stations, leaving the maze dominant.
            dx,dy,dw,dh=g.arena.den
            gate=pg.Rect(OX+dx*TILE+5,TOP+dy*TILE+5,dw*TILE-10,dh*TILE-10)
            pg.draw.rect(self.canvas,(0,0,4),gate,border_radius=4)
            pg.draw.rect(self.canvas,accent,gate,2,border_radius=4)
            door_x=center((27,15))[0]
            pg.draw.rect(self.canvas,(0,0,4),(door_x-20,gate.top-12,40,16))
            pg.draw.line(self.canvas,(224,211,255),(door_x-19,gate.top),(door_x+19,gate.top),2)
            for idx,spawn in enumerate(g.arena.spawns):
                sx=center(spawn)[0]
                upper=spawn[1]<ROWS//2
                mouth_y=TOP+4 if upper else TOP+ROWS*TILE-4
                by=mouth_y-34 if upper else mouth_y
                box=pg.Rect(sx-24,by,48,34)
                pg.draw.rect(self.canvas,(0,0,4),box,border_radius=7)
                pg.draw.rect(self.canvas,accent,box,2,border_radius=7)
                pg.draw.rect(self.canvas,accent,box.inflate(-7,-7),1,border_radius=4)
                pg.draw.rect(self.canvas,(0,0,4),(sx-20,mouth_y-6,40,12))
                active=idx<len(g.players)
                color=COLORS[idx] if active else tuple(c//4 for c in COLORS[idx])
                occupant=g.players[idx] if active else None
                inward=(0,-1) if upper else (0,1)
                visual=self.visual_positions.get(idx,center(spawn))
                crossing=occupant and abs(visual[1]-mouth_y)<22
                opening=occupant and occupant.lives>0 and (occupant.entry>0 or occupant.pos==spawn
                    or (occupant.pos==g.arena.entries[idx] and occupant.wanted==inward) or crossing)
                if not opening:
                    pg.draw.line(self.canvas,GATE_HATCH,(sx-20,mouth_y),(sx+20,mouth_y),2)
                    for hatch in range(-18,19,6):
                        pg.draw.line(self.canvas,GATE_HATCH,(sx+hatch,mouth_y-4),(sx+hatch+4,mouth_y+3),1)
                sy=4 if upper else TOP+ROWS*TILE+10
                if active:
                    p=g.players[idx]
                    arcade_digits(self.canvas,f'{p.score:06}',sx+22,sy,color,3)
                    for life in range(p.lives): pg.draw.circle(self.canvas,color,(sx+25+life*9,sy+27),2)
                    if p.lives<=0: self.text('OUT',sx+137,sy,color,self.small)
                else: self.text('PRESS START',sx+21,sy+1,color,self.small)
            arcade_digits(self.canvas,f'{int(g.time)//60}:{int(g.time)%60:02}',W//2-36,1,(250,250,235),3)
            self.text(f'STAGE {g.stage}',W//2-30,25,accent,self.small)
            # Tunnel necks project beyond the board, as in the cabinet footage.
            for row in g.arena.portals:
                cy=center((0,row))[1]
                for side in (-1,1):
                    edge=OX if side<0 else OX+COLS*TILE
                    for dy in (-27,-23,23,27):
                        pg.draw.line(self.canvas,accent,(edge,cy+dy),(edge+side*26,cy+dy),1)
            self.canvas.set_clip(pg.Rect(OX-28,TOP-32,COLS*TILE+56,ROWS*TILE+64))
            self.canvas.set_clip(pg.Rect(OX,TOP,COLS*TILE,ROWS*TILE))
            for c,life in g.smoke.items():
                cx,cy=center(c)
                fog=pg.Surface((70,62),pg.SRCALPHA)
                for n in range(4):
                    pg.draw.circle(fog,(150,163,180,int(65*min(1,life))),
                        (18+n*10,30+round(math.sin(self.animation_time*3+n)*7)),15)
                self.canvas.blit(fog,(cx-35,cy-31))
            for c,life in g.zaps:
                cx,cy=center(c)
                for n in range(8):
                    angle=n*math.pi/4
                    ex=cx+math.cos(angle)*100; ey=cy+math.sin(angle)*100
                    pg.draw.lines(self.canvas,(140,230,255),False,[(cx,cy),((cx+ex)/2+8,(cy+ey)/2-8),(ex,ey)],2)
            for p in g.players:
                if g.active(p,'Flare'):
                    for n,c in enumerate(g.fire_cells(p)):
                        cx,cy=center(c)
                        radius=max(5,16-n*2)
                        pg.draw.circle(self.canvas,(246,82,32),(cx,cy),radius)
                        pg.draw.circle(self.canvas,(255,225,85),(cx,cy),max(3,radius-5))
            for c in g.dots:
                cx,cy=center(c); self.canvas.blit(dot_sprite(),(cx-3,cy-3))
            for c,(owner,_) in g.traps.items(): pg.draw.circle(self.canvas,COLORS[owner],center(c),11,2)
            self.canvas.set_clip(pg.Rect(OX-28,TOP,COLS*TILE+56,ROWS*TILE))
            counts={}
            for c,name in sorted(g.items.items()):
                idx=counts.get(name,0); counts[name]=idx+1; key=(name,idx)
                target=center(c); old=self.visual_items.get(key,target)
                if c[1] in g.arena.portals and abs(target[0]-old[0])>COLS*TILE/2:
                    target=(target[0]+(COLS*TILE if old[0]>target[0] else -COLS*TILE),target[1])
                elif distance(old,target)>TILE*3: old=target
                smooth=(old[0]+(target[0]-old[0])*.3,old[1]+(target[1]-old[1])*.3)
                if c[1] in g.arena.portals:
                    if smooth[0]<OX: smooth=(smooth[0]+COLS*TILE,smooth[1])
                    elif smooth[0]>OX+COLS*TILE: smooth=(smooth[0]-COLS*TILE,smooth[1])
                self.visual_items[key]=smooth
                power_icon(self.canvas,tuple(map(round,smooth)),name,self.animation_time)
                if c[1] in g.arena.portals and (smooth[0]<=OX+20 or smooth[0]>=OX+COLS*TILE-20):
                    twin=smooth[0]+COLS*TILE if smooth[0]<OX+COLS*TILE/2 else smooth[0]-COLS*TILE
                    power_icon(self.canvas,(round(twin),round(smooth[1])),name,self.animation_time)
            self.canvas.set_clip(pg.Rect(OX-28,TOP-32,COLS*TILE+56,ROWS*TILE+64))
            for i,c in enumerate(g.foes):
                target=center(c); old=self.visual_foes.get(i,target)
                if c[1] in g.arena.portals and abs(target[0]-old[0])>COLS*TILE/2:
                    target=(target[0]+(COLS*TILE if old[0]>target[0] else -COLS*TILE),target[1])
                elif distance(old,target)>TILE*3: old=target
                smooth=(old[0]+(target[0]-old[0])*.3,old[1]+(target[1]-old[1])*.3)
                if c[1] in g.arena.portals:
                    if smooth[0]<OX: smooth=(smooth[0]+COLS*TILE,smooth[1])
                    elif smooth[0]>OX+COLS*TILE: smooth=(smooth[0]-COLS*TILE,smooth[1])
                self.visual_foes[i]=smooth
                look=(1 if target[0]>old[0] else -1 if target[0]<old[0] else 0,
                      1 if target[1]>old[1] else -1 if target[1]<old[1] else 0)
                edible=any(g.active(p,'Crown') or g.active(p,'Titan') for p in g.players if p.lives>0)
                foe(self.canvas,tuple(map(round,smooth)),COLORS[(3,1,2,5)[i%4]],self.animation_time,g.foe_stun>0,look,edible and g.foe_modes[i]=='roaming',g.foe_modes[i] in ('eyes','entering'))
                if c[1] in g.arena.portals and (smooth[0]<OX+30 or smooth[0]>OX+COLS*TILE-30):
                    twin=smooth[0]+COLS*TILE if smooth[0]<OX+30 else smooth[0]-COLS*TILE
                    foe(self.canvas,(round(twin),round(smooth[1])),COLORS[(3,1,2,5)[i%4]],self.animation_time,
                        False,look,edible and g.foe_modes[i]=='roaming',g.foe_modes[i] in ('eyes','entering'))
            for p in g.players:
                if p.lives<=0: continue
                target=center(p.pos)
                if p.pos==g.arena.spawns[p.idx]:
                    target=(target[0],TOP-5 if p.pos[1]==0 else TOP+ROWS*TILE+5)
                old=self.visual_positions.get(p.idx,target)
                wrap=p.pos[1] in g.arena.portals and abs(target[0]-old[0])>COLS*TILE/2
                if wrap: target=(target[0]+(COLS*TILE if old[0]>target[0] else -COLS*TILE),target[1])
                elif distance(old,target)>TILE*3: old=target
                smooth=(old[0]+(target[0]-old[0])*.38,old[1]+(target[1]-old[1])*.38)
                if p.pos[1] in g.arena.portals:
                    if smooth[0]<OX: smooth=(smooth[0]+COLS*TILE,smooth[1])
                    elif smooth[0]>OX+COLS*TILE: smooth=(smooth[0]-COLS*TILE,smooth[1])
                self.visual_positions[p.idx]=smooth
                cx,cy=map(round,smooth); r=36 if g.active(p,'Titan') else 17
                if g.active(p,'Rush') or g.active(p,'Slick'):
                    for n in range(1,4):
                        pg.draw.circle(self.canvas,tuple(v//(n*4) for v in COLORS[p.idx]),
                                       (cx-p.direction[0]*n*12,cy-p.direction[1]*n*12),max(2,9-n*2))
                muncher(self.canvas,(cx,cy),COLORS[p.idx],p.direction,self.animation_time+p.idx,r,
                        g.active(p,'Crown') or g.active(p,'Titan'),p.safe>0,150 if g.active(p,'Veil') else 255)
                if p.pos[1] in g.arena.portals and (cx<=OX+r+9 or cx>=OX+COLS*TILE-r-9):
                    twin=cx+COLS*TILE if cx<OX+COLS*TILE/2 else cx-COLS*TILE
                    muncher(self.canvas,(twin,cy),COLORS[p.idx],p.direction,self.animation_time+p.idx,r,
                            g.active(p,'Crown') or g.active(p,'Titan'),p.safe>0,150 if g.active(p,'Veil') else 255)
                delta=p.score-self.score_memory.get(p.idx,p.score)
                if delta>10: self.popups.append([str(delta),cx,cy-r,1.,COLORS[p.idx]])
                self.score_memory[p.idx]=p.score
                if p.stun>0:
                    self.text('* *',cx-12,cy-r-14,(255,255,230),self.small)
                if g.active(p,'Lure'): power_icon(self.canvas,(cx,cy-r-12),'Lure',self.animation_time,22)
            self.canvas.set_clip(pg.Rect(OX,TOP,COLS*TILE,ROWS*TILE))
            for popup in self.popups[:]:
                label,px,py,life,color=popup
                arcade_digits(self.canvas,label,px-14,round(py),color,2)
                popup[2]-=.5; popup[3]-=1/60
                if popup[3]<=0: self.popups.remove(popup)
            self.canvas.set_clip(None)
            footer='AUTOPLAY - COMPUTER PLAYERS' if self.demo else 'LOCAL ARCADE BATTLE'
            status=self.controller_status()
            message=footer+' | '+status['message']+' | F1 guide  P pause  F2 sound  ESC lobby'
            color=(255,188,87) if status['missing'] or status['disconnected'] else (127,168,198)
            self.text(message,OX,H-12,color,self.micro)
            if g.paused: self.overlay('PAUSED','Press P to continue')
            if g.over:
                best=max(p.score for p in g.players)
                winners=', '.join(f'P{p.idx+1}' for p in g.players if p.score==best)
                self.overlay(f'{winners} WINS!',f'{best} points  |  ENTER: rematch  |  ESC: lobby')
        if self.help:
            panel=pg.Surface((1160,650)); panel.fill((12,18,31)); self.canvas.blit(panel,(60,35))
            self.text('POWER FIELD GUIDE',105,55,(104,242,209),self.big)
            for i,(name,(code,desc)) in enumerate(ITEMS.items()):
                power_icon(self.canvas,(125,140+i*43),name,self.animation_time,42)
                self.text(f'{DISPLAY_NAMES[name]}: {desc}',165,130+i*43)
            self.text('F1 closes. Guide pauses play. Titans bite rivals; equal powers are safe.',105,617)
            self.text('3 starting lives. 3-minute score attack. Clearing dots rotates arenas.',105,653)
        sw,sh=self.screen.get_size(); factor=min(sw/W,sh/H)
        size=(max(1,round(W*factor)),max(1,round(H*factor)))
        scaled=pg.transform.smoothscale(self.canvas,size)
        self.screen.fill((0,0,0))
        self.screen.blit(scaled,((sw-size[0])//2,(sh-size[1])//2)); pg.display.flip()

    def overlay(self,title,subtitle):
        box=pg.Surface((900,180),pg.SRCALPHA); box.fill((7,12,25,235))
        ox,oy=(W-900)//2,(H-180)//2
        self.canvas.blit(box,(ox,oy))
        title_font=self.big
        if title_font.size(title)[0]>780:
            title_font=pg.font.Font(None,max(22,int(65*780/title_font.size(title)[0])))
        self.text(title,ox+65,oy+25,(104,242,209),title_font)
        self.text(subtitle,ox+65,oy+110)

    def run(self,frames=0):
        n=0
        while self.running:
            dt=min(.05,self.clock.tick(60)/1000)
            self.events()
            if self.match:
                if self.demo: steer_demo(self.match)
                else: self.inputs()
                if not self.help:
                    sounds=self.match.update(dt)
                    if not self.muted:
                        for name in set(sounds):
                            if name in self.sounds: self.sounds[name].play()
            self.draw(); n+=1
            if frames and n>=frames: break
        pg.quit()

def steer_demo(g):
    """Greedy breadth-first navigation for a visible, reproducible attract demo."""
    for p in g.players:
        if p.lives<=0: continue
        nearby={c for c in g.items if distance(c,p.pos)<=14}
        goals=nearby or g.dots
        if g.active(p,'Crown') or g.active(p,'Titan'):
            goals=set(g.foes)
        if g.active(p,'Titan'):
            goals.update(q.pos for q in g.players if q is not p and q.lives>0 and q.safe<=0)
        goals.discard(p.pos)
        queue=deque([(p.pos,None)]); seen={p.pos}
        # Different rotations keep the bots from always choosing identical paths.
        directions=DIRS[p.idx%4:]+DIRS[:p.idx%4]
        while queue:
            cell,first=queue.popleft()
            if cell in goals:
                p.wanted=first
                break
            for d in directions:
                nxt=g.arena.step(cell,d)
                if g.arena.can_enter(nxt,p) and nxt not in seen:
                    seen.add(nxt); queue.append((nxt,first or d))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--frames',type=int,default=0,help='Exit after N frames (smoke checks).')
    parser.add_argument('--players',type=int,choices=range(1,9),help='Start immediately with 1-8 players.')
    parser.add_argument('--simulate-controllers',action='store_true',help='Development only: assume controller availability; label it simulated. Does not generate input.')
    parser.add_argument('--demo',action='store_true',help='Computer-controlled attract demo; defaults to 8 players.')
    args=parser.parse_args()
    app=App(simulate_controllers=args.simulate_controllers)
    app.demo=args.demo
    if args.demo and not args.players: args.players=8
    if args.players: app.count=args.players; app.start()
    app.run(args.frames)


