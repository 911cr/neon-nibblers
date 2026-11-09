"""Neon Nibblers — original local arcade maze battle. Python 3.10+."""
import os
import sys
import math
import random
import argparse
from collections import deque
from dataclasses import dataclass, field
import pygame as pg
from score_ledger import ScoreLedger, DEFAULT_SCORES
from stations import Phase, phase_for, StationBindings
from map_library import get_map, next_map_index
from arcade_art import maze_background, muncher, foe, power_icon, arcade_digits, dot_sprite, fire_plume
from arcade_audio import ArcadeAudio

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
    joined: bool = True
    locate_remaining: float = 0.

class Arena:
    def __init__(self, theme):
        spec=get_map(theme)
        self.theme=theme%4
        self.map_id=spec.id; self.map_revision=spec.revision
        self.lanes=set(spec.lanes)
        self.entries=list(spec.entries); self.spawns=list(spec.spawns)
        self.gate_owner={c:i for i,c in enumerate(self.spawns)}
        self.portals=spec.portals; self.den=spec.den
        self.floor=self.lanes | set(self.spawns)
        self.space=self.floor

    def can_enter(self, cell, player):
        return cell in self.floor and self.gate_owner.get(cell,player.idx)==player.idx

    def step(self,pos,direction):
        target=add(pos,direction)
        if pos[1] in self.portals and target[0] in (-1,COLS):
            target=(target[0]%COLS,target[1])
        return target

class Match:
    def __init__(self, count=2, theme=0, seed=None, score_values=None, progression='cycle'):
        if not 0 <= count <= 8: raise ValueError('Player count must be 0..8')
        if progression not in ('cycle', 'repeat', 'random'): raise ValueError('Unknown progression policy')
        self.progression = progression
        self.seed = seed if seed is not None else random.SystemRandom().randrange(2**63)
        self.rng = random.Random(self.seed)
        self.elapsed = 0.; self.tick = 0
        self.ledger = ScoreLedger()
        self.score_values = dict(DEFAULT_SCORES)
        if score_values is not None:
            if set(score_values) - set(DEFAULT_SCORES): raise ValueError('Unknown scoring event')
            if any(type(v) is not int or v < 0 for v in score_values.values()):
                raise ValueError('Scores must be non-negative integers')
            self.score_values.update(score_values)
        self.count, self.stage = count, 1
        self.time, self.item_clock, self.foe_clock = 180., 0., 0.
        self.item_walk_clock=0.; self.item_directions={}
        self.over, self.paused = False, False
        self.players = [Player(i,(0,0)) for i in range(count)]
        self.new_arena(theme)
        self.ledger.append(self, 'match_start', seed=self.seed, count=count,
                           theme=theme, score_values=self.score_values, progression=progression)

    def award(self, player, event, **context):
        """One score mutation path, shared by HUD totals, traces and replay checks."""
        delta = self.score_values[event]
        player.score += delta
        self.ledger.append(self, event, player, delta, position=list(player.pos), **context)

    def join_station(self, idx):
        """Development free-play policy; commercial joining windows remain unknown."""
        if not 0 <= idx < 8 or self.over or self.paused: return False
        if idx < len(self.players) and getattr(self.players[idx], 'joined', True): return False
        while len(self.players) < 8:
            p = Player(len(self.players), (0, 0), lives=0)
            p.joined = False
            self.players.append(p)
        p = Player(idx, self.arena.spawns[idx])
        p.joined = True
        p.entry = .8
        p.direction = (0, 1) if p.pos[1] == 0 else (0, -1)
        self.players[idx] = p
        self.count = sum(getattr(p, 'joined', True) for p in self.players)
        self.ledger.append(self, 'station_join', p, position=list(p.pos), lives=p.lives)
        return True

    def rankings(self):
        """Competition ranks preserve ties; station order only stabilizes display."""
        ordered = sorted((p for p in self.players if getattr(p, 'joined', True)),
                         key=lambda p: (-p.score, p.idx))
        return [{'rank': 1 + sum(q.score > p.score for q in ordered),
                 'player_id': p.idx + 1, 'score': p.score, 'lives': p.lives}
                for p in ordered]

    def snapshot(self):
        """JSON-safe complete logic state for deterministic regression comparisons."""
        def freeze(value):
            if isinstance(value, dict):
                return [[freeze(k), freeze(v)] for k, v in sorted(value.items(), key=lambda p: repr(p[0]))]
            if isinstance(value, set): return [freeze(v) for v in sorted(value)]
            if isinstance(value, (list, tuple)): return [freeze(v) for v in value]
            return value
        state = {k: freeze(v) for k, v in vars(self).items()
                 if k not in ('arena', 'players', 'rng', 'ledger')}
        state['arena_theme'] = self.arena.theme
        state['map_id'] = self.arena.map_id
        state['map_revision'] = self.arena.map_revision
        state['players'] = [freeze(vars(p)) for p in self.players]
        state['rng'] = freeze(self.rng.getstate())
        return state

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

    @staticmethod
    def countdown(value, dt):
        remaining=value-dt
        return remaining if remaining>1e-10 else 0.

    def age_foes(self,dt):
        self.foe_clock+=dt
        self.foe_stun=self.countdown(self.foe_stun,dt)
        for i in range(len(self.foes)):
            self.foe_release[i]=self.countdown(self.foe_release[i],dt)
            self.foe_ticks[i]+=dt
            self.foe_zapped[i]=self.countdown(self.foe_zapped[i],dt)

    def update_foes(self, dt, age=True):
        self.sync_carriers()
        if age: self.age_foes(dt)
        if self.foe_clock+1e-10<.16: return
        self.foe_clock=max(0.,self.foe_clock-.16)%.16
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
            if self.foe_stun>0 or self.foe_zapped[i]>0 or self.foe_ticks[i]+1e-10<.16*slow: continue
            self.foe_ticks[i]=max(0.,self.foe_ticks[i]-.16*slow)%(.16*slow)
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
        old_position = list(p.pos)
        p.lives -= 1
        p.pos, p.safe = self.arena.spawns[p.idx], 3.
        p.direction, p.wanted = (0,0),(0,0)
        p.entry=.8; p.stun=0.; p.clock=0.
        p.effects.clear()
        self.ledger.append(self, 'player_hurt', p, position=old_position, lives=p.lives)
        return True

    def collect(self,p,name):
        self.award(p, 'pickup', power=name)
        p.last = name
        if name == 'Heart':
            old_lives = p.lives
            p.lives = min(5,p.lives+1)
            self.ledger.append(self, 'extra_life', p, lives=p.lives, gained=p.lives-old_lives)
        elif name=='Spark':
            self.zaps.append((p.pos,.5))
            for q in self.players:
                if q is not p and q.lives>0 and distance(q.pos,p.pos)<=8: q.stun=2.
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

    def collect_contacts(self,sounds):
        """A moving item can touch a stationary/stunned player too."""
        for p in self.players:
            if p.lives>0 and p.pos in self.items:
                self.collect(p,self.items.pop(p.pos))
                self.item_directions.pop(p.pos,None)
                sounds.append('power')

    def apply_fire(self):
        for p in self.players:
            if p.lives<=0 or not self.active(p,'Flare'): continue
            cells=self.fire_cells(p)
            for i,f in enumerate(self.foes):
                if f in cells and self.foe_modes[i]=='roaming':
                    self.award(p, 'ghost_burned', ghost_id=i, target=list(f)); self.reset_foe(i)
            for q in self.players:
                if q is not p and q.pos in cells and self.hurt(q):
                    self.award(p, 'rival_burned', target_player_id=q.idx+1)

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
                old_lives = p.lives
                if p.lives>0: p.lives=min(5,p.lives+1)
                self.ledger.append(self, 'score_bonus_life', p, lives=p.lives, gained=p.lives-old_lives)

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
                    if owner!=p.idx and self.hurt(p):
                        self.award(self.players[owner], 'carried_ghost_hit', ghost_id=i, target_player_id=p.idx+1)
                    continue
                if self.active(p,'Lure'):
                    self.foe_carriers[i]=p.idx; self.foe_modes[i]='carried'
                    self.ledger.append(self, 'ghost_captured', p, ghost_id=i)
                    continue
                if self.active(p,'Crown') or self.active(p,'Titan'):
                    self.award(p, 'ghost_eaten', ghost_id=i, power='Titan' if self.active(p,'Titan') else 'Crown')
                    self.reset_foe(i)
                else: self.hurt(p)
        for i,p in enumerate(self.players):
            for q in self.players[i+1:]:
                if min(p.lives,q.lives)<=0: continue
                crossed = previous and previous[p.idx]==q.pos and previous[q.idx]==p.pos
                if p.pos!=q.pos and not crossed: continue
                a = self.active(p,'Titan')
                b = self.active(q,'Titan')
                if a and not b and self.hurt(q): self.award(p, 'rival_eaten', target_player_id=q.idx+1)
                if b and not a and self.hurt(p): self.award(q, 'rival_eaten', target_player_id=p.idx+1)
                if a==b: self.bump(p,q,previous)
        self.separate_overlaps()

    def update(self,dt):
        if self.over or self.paused: return []
        if not math.isfinite(dt) or dt < 0: raise ValueError('dt must be finite and non-negative')
        self.elapsed += dt; self.tick += 1
        sounds=[]
        self.time=self.countdown(self.time,dt)
        previous=[p.pos for p in self.players]
        old_foes=list(self.foes)
        self.quake=self.countdown(self.quake,dt)
        self.smoke={c:self.countdown(t,dt) for c,t in self.smoke.items() if t>dt+1e-10}
        self.zaps=[(c,self.countdown(t,dt)) for c,t in self.zaps if t>dt+1e-10]
        self.bump_cooldowns={pair:self.countdown(t,dt) for pair,t in self.bump_cooldowns.items() if t>dt+1e-10}
        # Age everybody before any pickup. Newly applied powers must not lose
        # a tick just because the recipient has a higher station number.
        self.age_foes(dt)
        for p in self.players:
            p.safe=self.countdown(p.safe,dt); p.stun=self.countdown(p.stun,dt)
            for k in list(p.effects):
                p.effects[k]=self.countdown(p.effects[k],dt)
                if p.effects[k]<=0: del p.effects[k]
        for p in self.players:
            if p.lives<=0 or p.stun>0: continue
            if p.entry>0 and p.pos==self.arena.spawns[p.idx]:
                p.entry=self.countdown(p.entry,dt)
                if p.entry==0:
                    p.pos=self.arena.entries[p.idx]
                    p.direction=(0,1) if p.pos[1]==1 else (0,-1)
                continue
            p.entry=0
            p.clock+=dt
            speed=.065 if self.active(p,'Rush') else .10
            if self.active(p,'Slick'): speed=.055
            if self.quake>0: speed*=2
            if p.clock+1e-10>=speed:
                p.clock=max(0.,p.clock-speed)%speed
                if self.active(p,'Slick'):
                    if not self.arena.can_enter(self.arena.step(p.pos,p.direction),p) or p.direction==(0,0):
                        options=[d for d in DIRS if self.arena.can_enter(self.arena.step(p.pos,d),p)]
                        if options: p.direction=self.rng.choice(options)
                elif self.arena.can_enter(self.arena.step(p.pos,p.wanted),p): p.direction=p.wanted
                if self.active(p,'Mist') and p.pos in self.arena.lanes: self.smoke[p.pos]=2.5
                if self.arena.can_enter(self.arena.step(p.pos,p.direction),p): p.pos=self.arena.step(p.pos,p.direction)
                if p.pos in self.dots:
                    self.dots.remove(p.pos); self.award(p, 'dot'); sounds.append('dot')
                if p.pos in self.traps and self.traps[p.pos][0]!=p.idx:
                    p.stun=1.5; del self.traps[p.pos]
        # Resolve pickups after all simultaneous player movement. A lightning
        # pickup cannot cancel only the movement of later-numbered stations.
        self.collect_contacts(sounds)
        self.update_foes(dt,age=False)
        combat_events=len(self.ledger.events)
        self.combat(previous,old_foes)
        self.apply_fire()
        self.award_score_lives()
        if any(e['event']=='player_hurt' for e in self.ledger.events[combat_events:]): sounds.append('hurt')
        for cell,(owner,t) in list(self.traps.items()):
            if t<=dt: del self.traps[cell]
            else: self.traps[cell]=(owner,t-dt)
        self.item_clock+=dt
        if self.item_clock+1e-10>=SPAWN_INTERVAL:
            self.item_clock=max(0.,self.item_clock-SPAWN_INTERVAL)%SPAWN_INTERVAL
            if len(self.items)<MAX_ITEMS: self.spawn_item()
        self.item_walk_clock+=dt
        if self.item_walk_clock+1e-10>=ITEM_STEP_INTERVAL:
            self.item_walk_clock=max(0.,self.item_walk_clock-ITEM_STEP_INTERVAL)%ITEM_STEP_INTERVAL
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
            self.collect_contacts(sounds)
            self.award_score_lives()
        if self.time<=0 or not any(p.lives>0 for p in self.players):
            self.over=True
            self.ledger.append(self, 'match_end', reason='time' if self.time<=0 else 'elimination', rankings=self.rankings())
        elif not self.dots:
            for p in self.players:
                if p.lives>0: self.award(p, 'stage_clear')
            self.stage+=1
            self.new_arena(next_map_index(self.arena.theme, self.progression, self.rng))
            self.ledger.append(self, 'stage_start', theme=self.arena.theme)
            self.award_score_lives()
            sounds.append('power')
        return sounds

def add(a,b): return a[0]+b[0],a[1]+b[1]
def distance(a,b): return abs(a[0]-b[0])+abs(a[1]-b[1])
def center(c): return OX+c[0]*TILE+TILE//2,TOP+c[1]*TILE+TILE//2

def station_hud(spawn,score=0):
    """Reserve clearance beside each bay for every digit, life and prompt."""
    sx=center(spawn)[0]
    sy=4 if spawn[1]<ROWS//2 else TOP+ROWS*TILE+10
    label=f'{score:06}'
    scale=max(1,min(3,108//(6*len(label))))
    return {'x':sx+50,'y':sy,'label':label,'scale':scale,
            'score':pg.Rect(sx+50,sy,(6*len(label)-1)*scale,7*scale),
            'lives':pg.Rect(sx+50,sy+25,48,7)}

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
        self.bindings=StationBindings(); self.pair_station=None
        self.pads={}; self.refresh_pads(); self.sounds={}
        self.fixed_accumulator=0.; self.ledger_cursor=0
        self.locator_seconds=2.0  # Original timing unknown; configurable approximation.
        self.seed=None; self.progression='cycle'; self.pair_error=''
        self.palette_override=None  # Presentation is independent of maze topology.
        self.demo=False; self.visual_positions={}; self.animation_time=0.
        self.backgrounds={}; self.visual_foes={}; self.score_memory={}; self.popups=[]; self.visual_items={}
        self.micro=pg.font.Font(None,16)
        self.audio=ArcadeAudio();self.sounds=self.audio.sounds

    def refresh_pads(self):
        previous=set(self.pads)
        for i in range(pg.joystick.get_count()):
            joy=pg.joystick.Joystick(i)
            self.pads[joy.get_instance_id()]=joy
        self.pads={k:v for k,v in self.pads.items() if v.get_init() and v.get_attached()}
        self.bindings.sync(self.pads)
        if previous-set(self.pads): self.controller_notice_until=pg.time.get_ticks()+5000
        elif set(self.pads)-previous: self.controller_notice_until=0

    def controller_status(self):
        expected=self.match.count if self.match else self.count
        self.bindings.sync(self.pads)
        required=[p.idx for p in self.match.players if p.joined] if self.match else list(range(expected))
        served={s for iid,s in self.bindings.by_instance.items() if iid in self.pads}
        missing_stations=[s+1 for s in required if s not in served]
        actual=min(8,len(self.pads))
        simulated=self.simulate_controllers
        effective=expected if simulated else len(set(required)&served)
        missing=max(0,expected-effective)
        disconnected=not simulated and pg.time.get_ticks()<self.controller_notice_until
        if simulated:
            message=f'DEV: {expected} controllers assumed connected (SIMULATED)'
        elif disconnected:
            message=f'Controller disconnected | {actual}/{expected} connected | keyboard fallback available'
        elif missing:
            names=','.join(f'P{s}' for s in missing_stations)
            message=f'Missing {missing} of {expected} station controllers ({names}) | {actual} connected | keyboard fallback available'
        else:
            message=f'{actual} controllers connected | {expected} players'
        return {'expected':expected,'actual':actual,'effective':effective,'missing':missing,
                'missing_stations':[] if simulated else missing_stations,
                'simulated':simulated,'disconnected':disconnected,'message':message}

    def text(self,s,x,y,color=(224,234,247),font=None):
        self.canvas.blit((font or self.font).render(str(s),True,color),(x,y))

    @property
    def phase(self):
        return phase_for(self.match,self.help)

    def station_action(self,idx):
        """Start/join/find policy for this adaptation; DX joining windows unknown."""
        if self.phase in (Phase.GUIDE,Phase.PAUSED): return
        if self.phase in (Phase.ATTRACT,Phase.RESULTS):
            self.match=Match(0,self.theme,seed=self.seed,progression=self.progression)
            self.reset_visuals()
        if idx>=len(self.match.players) or not self.match.players[idx].joined:
            self.match.join_station(idx)
        p=self.match.players[idx]
        if p.lives>0:
            p.locate_remaining=self.locator_seconds
            self.match.ledger.append(self.match,'locate',p,duration=self.locator_seconds)

    def events(self):
        for e in pg.event.get():
            if e.type==pg.QUIT: self.running=False
            if e.type in (pg.JOYDEVICEADDED,pg.JOYDEVICEREMOVED): self.refresh_pads()
            if e.type==pg.JOYBUTTONDOWN and e.button==0:
                iid=getattr(e,'instance_id',None)
                if self.pair_station is not None and self.match is None and iid in self.pads:
                    joy=self.pads[iid]
                    guid=joy.get_guid() if hasattr(joy,'get_guid') else ''
                    if self.bindings.bind(iid,self.pair_station,guid):
                        self.pair_station=None; self.pair_error=''
                    else: self.pair_error='Station occupied: move its controller to a free station first.'
                elif iid in self.bindings.by_instance:
                    self.station_action(self.bindings.by_instance[iid])
            if e.type!=pg.KEYDOWN: continue
            if pg.K_F3<=e.key<=pg.K_F10:
                idx=e.key-pg.K_F3
                if getattr(e,'mod',0)&pg.KMOD_SHIFT and self.match is None:
                    self.pair_station=idx; self.pair_error=''
                else: self.station_action(idx)
                continue
            if self.match and not self.match.over:
                for p in self.match.players:
                    for k,d in zip(KEYS[p.idx],DIRS):
                        if e.key==k: p.wanted=d
            if e.key==pg.K_ESCAPE:
                if self.help: self.help=False
                elif self.match: self.match=None
                else: self.running=False
            elif e.key==pg.K_F1: self.help=not self.help
            elif e.key==pg.K_F2:
                self.muted=not self.muted
                if self.muted:self.audio.silence()
            elif e.key==pg.K_F12:
                current=self.palette_override if self.palette_override is not None else (self.match.arena.theme if self.match else self.theme)
                self.palette_override=(current+1)%len(THEMES)
            elif e.key==pg.K_RETURN and (not self.match or self.match.over): self.start()
            elif e.key==pg.K_p and self.match: self.match.paused=not self.match.paused
            elif not self.match:
                if pg.K_1<=e.key<=pg.K_8: self.count=e.key-pg.K_0
                if e.key==pg.K_TAB: self.theme=(self.theme+1)%4

    def start(self):
        self.match=Match(self.count,self.theme,seed=self.seed,progression=self.progression); self.help=False
        self.reset_visuals()

    def reset_visuals(self):
        self.fixed_accumulator=0.; self.ledger_cursor=0
        self.visual_positions={}; self.visual_foes={}; self.score_memory={}; self.popups=[]; self.visual_items={}

    def item_tracks(self,items,portals):
        """Match equal-looking items by proximity, never by sorted-list index."""
        previous=self.visual_items
        pending=set(items); available=set(previous); assigned={}
        pairs=[]
        period=COLS*TILE
        for cell,name in items.items():
            x,y=center(cell)
            for key,(px,py) in previous.items():
                if key[0]!=name:continue
                dx=abs(x-px)
                if cell[1] in portals:dx=min(dx,abs(dx-period))
                pairs.append((dx+abs(y-py),cell,key))
        for _,cell,key in sorted(pairs):
            if cell in pending and key in available:
                assigned[cell]=key;pending.remove(cell);available.remove(key)
        serial=max((key[1] for key in previous),default=-1)+1
        for cell in sorted(pending):
            assigned[cell]=(items[cell],serial);serial+=1
        self.visual_items={key:previous[key] for key in assigned.values() if key in previous}
        return assigned

    def inputs(self):
        keys=pg.key.get_pressed()
        self.bindings.sync(self.pads)
        for p in self.match.players:
            wanted=None
            for k,d in zip(KEYS[p.idx],DIRS):
                if keys[k]: wanted=d
            joy=self.bindings.device_for(p.idx,self.pads)
            if joy is not None:
                x=joy.get_axis(0) if joy.get_numaxes()>0 else 0
                y=joy.get_axis(1) if joy.get_numaxes()>1 else 0
                if joy.get_numhats():
                    hx,hy=joy.get_hat(0)
                    if hx or hy: x,y=hx,-hy
                if max(abs(x),abs(y))>.35:
                    wanted=(1 if x>0 else -1,0) if abs(x)>abs(y) else (0,1 if y>0 else -1)
            if wanted: p.wanted=wanted

    def draw(self,dt=1/60):
        self.canvas.fill((0,0,4))
        if self.match and self.phase!=Phase.PLAYING:dt=0.
        self.animation_time+=dt
        smooth_item=1-.7**(dt*60)
        smooth_player=1-.62**(dt*60)
        if not self.match:
            if self.theme not in self.backgrounds:
                arena=Arena(self.theme)
                self.backgrounds[self.theme]=maze_background(arena.space,COLS,ROWS,TILE,THEMES[self.theme][1])
            self.canvas.blit(self.backgrounds[self.theme],(OX,TOP))
            shade=pg.Surface((W,H),pg.SRCALPHA); shade.fill((0,0,8,215))
            self.canvas.blit(shade,(0,0))
            for i in range(8):
                muncher(self.canvas,(325+i*90,190),COLORS[i],(1,0),self.animation_time+i,25)
            self.text('NEON NIBBLERS',W//2-200,58,(255,222,72),self.big)
            self.text('A snack-sized rivalry. An oversized appetite.',W//2-185,125)
            status=self.controller_status()
            message=status['message']
            color=(255,188,87) if status['missing'] or status['disconnected'] else (134,204,244)
            self.text(message,(W-self.small.size(message)[0])//2,242,color,self.small)
            self.text('F3-F10: START / FIND at stations P1-P8',W//2-190,280)
            self.text('Arena: '+THEMES[self.theme][0],W//2-125,317,COLORS[self.theme])
            self.text(f'ENTER: quick start {self.count} players  |  1-8 changes count',W//2-210,365)
            self.text('Collect dots. Claim powers. Outscore your friends in 3 minutes.',W//2-265,408)
            for i in range(8):
                self.text(f'P{i+1}  F{i+3} START   {KEYLABELS[i]}',W//2-270+(i//4)*360,462+(i%4)*33,COLORS[i])
            pairing=f'PAIR P{self.pair_station+1}: press controller button 1' if self.pair_station is not None else 'SHIFT + F3-F10: pair a controller to a station'
            self.text(pairing,(W-self.font.size(pairing)[0])//2,620,(255,222,72))
            if self.pair_error: self.text(self.pair_error,360,647,(255,155,110),self.small)
            self.text('TAB arena  |  F1 guide  |  F2 sound  |  ESC quit',W//2-190,667)
        else:
            g=self.match
            for event in g.ledger.events[self.ledger_cursor:]:
                if event['event']=='player_hurt' and event['player_id'] is not None:
                    self.visual_positions.pop(event['player_id']-1,None)
                elif event['event']=='stage_start':
                    self.visual_positions.clear();self.visual_foes.clear();self.visual_items.clear()
            palette=g.arena.theme if self.palette_override is None else self.palette_override
            accent=THEMES[palette][1]
            background_key=(g.arena.map_id,g.arena.map_revision,palette)
            if background_key not in self.backgrounds:
                self.backgrounds[background_key]=maze_background(g.arena.space,COLS,ROWS,TILE,accent)
            self.canvas.blit(self.backgrounds[background_key],(OX,TOP))
            # Thin enclosure and colored border stations, leaving the maze dominant.
            dx,dy,dw,dh=g.arena.den
            gate=pg.Rect(OX+dx*TILE+5,TOP+dy*TILE+5,dw*TILE-10,dh*TILE-10)
            # Replace the carved-background house edge before drawing its two
            # explicit contours; otherwise background + overlay creates three.
            pg.draw.rect(self.canvas,(0,0,4),gate.inflate(18,18))
            pg.draw.rect(self.canvas,(0,0,4),gate,border_radius=4)
            pg.draw.rect(self.canvas,accent,gate,2,border_radius=4)
            pg.draw.rect(self.canvas,accent,gate.inflate(-8,-8),1,border_radius=3)
            door_x=center((27,15))[0]
            pg.draw.rect(self.canvas,(0,0,4),(door_x-20,gate.top-12,40,21))
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
                active=idx<len(g.players) and g.players[idx].joined
                color=COLORS[idx] if active else tuple(max(85,c//2) for c in COLORS[idx])
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
                hud=station_hud(spawn,occupant.score if occupant else 0)
                sx_text,sy=hud['x'],hud['y']
                if active:
                    p=g.players[idx]
                    arcade_digits(self.canvas,hud['label'],sx_text,sy,color,hud['scale'])
                    for life in range(p.lives): pg.draw.circle(self.canvas,color,(sx_text+3+life*9,sy+28),2)
                    if p.lives<=0: self.text('OUT',sx_text,sy+22,color,self.small)
                else: self.text(f'F{idx+3} / START',sx_text,sy+1,color,self.small)
            arcade_digits(self.canvas,f'{int(g.time)//60}:{int(g.time)%60:02}',W//2-36,1,(250,250,235),3)
            self.text(f'STAGE {g.stage}',W//2-30,25,accent,self.small)
            self.text(THEMES[g.arena.theme][0],W//2+55,25,accent,self.micro)
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
                    jitter=8*math.sin(self.animation_time*37+n*2.1)
                    pg.draw.lines(self.canvas,(140,230,255),False,[(cx,cy),((cx+ex)/2+jitter,(cy+ey)/2-jitter),(ex,ey)],2)
            for p in g.players:
                if g.active(p,'Flare'):
                    cells=g.fire_cells(p)
                    origin=center(p.pos);end=origin;previous=p.pos
                    for cell in cells:
                        if abs(cell[0]-previous[0])>1:
                            edge=OX if p.direction[0]<0 else OX+COLS*TILE
                            fire_plume(self.canvas,origin,(edge,origin[1]),p.direction,self.animation_time)
                            origin=(OX+COLS*TILE if p.direction[0]<0 else OX,origin[1])
                        end=center(cell);previous=cell
                    if cells:fire_plume(self.canvas,origin,end,p.direction,self.animation_time)
            for c in g.dots:
                cx,cy=center(c); self.canvas.blit(dot_sprite(),(cx-3,cy-3))
            for c,(owner,_) in g.traps.items(): pg.draw.circle(self.canvas,COLORS[owner],center(c),11,2)
            self.canvas.set_clip(pg.Rect(OX-28,TOP,COLS*TILE+56,ROWS*TILE))
            tracks=self.item_tracks(g.items,g.arena.portals)
            for c,name in sorted(g.items.items()):
                key=tracks[c]
                target=center(c); old=self.visual_items.get(key,target)
                if c[1] in g.arena.portals and abs(target[0]-old[0])>COLS*TILE/2:
                    target=(target[0]+(COLS*TILE if old[0]>target[0] else -COLS*TILE),target[1])
                elif distance(old,target)>TILE*3: old=target
                smooth=(old[0]+(target[0]-old[0])*smooth_item,old[1]+(target[1]-old[1])*smooth_item)
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
                smooth=(old[0]+(target[0]-old[0])*smooth_item,old[1]+(target[1]-old[1])*smooth_item)
                if c[1] in g.arena.portals:
                    if smooth[0]<OX: smooth=(smooth[0]+COLS*TILE,smooth[1])
                    elif smooth[0]>OX+COLS*TILE: smooth=(smooth[0]-COLS*TILE,smooth[1])
                self.visual_foes[i]=smooth
                look=(1 if target[0]>old[0] else -1 if target[0]<old[0] else 0,
                      1 if target[1]>old[1] else -1 if target[1]<old[1] else 0)
                edible=any(g.active(p,'Crown') or g.active(p,'Titan') for p in g.players if p.lives>0)
                stunned=g.foe_stun>0 or (i<len(g.foe_zapped) and g.foe_zapped[i]>0)
                foe(self.canvas,tuple(map(round,smooth)),COLORS[(3,1,2,5)[i%4]],self.animation_time,stunned,look,edible and g.foe_modes[i]=='roaming',g.foe_modes[i] in ('eyes','entering'))
                if c[1] in g.arena.portals and (smooth[0]<OX+30 or smooth[0]>OX+COLS*TILE-30):
                    twin=smooth[0]+COLS*TILE if smooth[0]<OX+30 else smooth[0]-COLS*TILE
                    foe(self.canvas,(round(twin),round(smooth[1])),COLORS[(3,1,2,5)[i%4]],self.animation_time,
                        stunned,look,edible and g.foe_modes[i]=='roaming',g.foe_modes[i] in ('eyes','entering'))
            for p in g.players:
                if p.lives<=0: continue
                target=center(p.pos)
                if p.pos==g.arena.spawns[p.idx]:
                    target=(target[0],TOP-5 if p.pos[1]==0 else TOP+ROWS*TILE+5)
                old=self.visual_positions.get(p.idx,target)
                wrap=p.pos[1] in g.arena.portals and abs(target[0]-old[0])>COLS*TILE/2
                if wrap: target=(target[0]+(COLS*TILE if old[0]>target[0] else -COLS*TILE),target[1])
                elif distance(old,target)>TILE*3: old=target
                smooth=(old[0]+(target[0]-old[0])*smooth_player,old[1]+(target[1]-old[1])*smooth_player)
                if p.pos[1] in g.arena.portals:
                    if smooth[0]<OX: smooth=(smooth[0]+COLS*TILE,smooth[1])
                    elif smooth[0]>OX+COLS*TILE: smooth=(smooth[0]-COLS*TILE,smooth[1])
                self.visual_positions[p.idx]=smooth
                cx,cy=map(round,smooth); r=36 if g.active(p,'Titan') else 17
                if p.locate_remaining>0:
                    ring=r+12+round(4*math.sin(self.animation_time*12))
                    if cy<TOP+45 or cy>TOP+ROWS*TILE-45:
                        ring=min(ring,44)  # Keep even giant locators clear of station scores.
                    pg.draw.circle(self.canvas,COLORS[p.idx],(cx,cy),ring,3)
                    below=cy-ring-23<TOP
                    label_y=cy+ring+5 if below else cy-ring-23
                    label_x=max(OX,min(OX+COLS*TILE-26,cx-12))
                    self.text(f'P{p.idx+1}',label_x,label_y,COLORS[p.idx],self.font)
                    arrow_y=cy+ring+2 if below else cy-ring-2
                    sign=1 if below else -1
                    pg.draw.polygon(self.canvas,COLORS[p.idx],[(cx-6,arrow_y+sign*6),(cx+6,arrow_y+sign*6),(cx,arrow_y)])
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
                self.score_memory[p.idx]=p.score
                if p.stun>0:
                    self.text('* *',cx-12,cy-r-14,(255,255,230),self.small)
                if g.active(p,'Lure'): power_icon(self.canvas,(cx,cy-r-12),'Lure',self.animation_time,22)
            self.canvas.set_clip(pg.Rect(OX,TOP,COLS*TILE,ROWS*TILE))
            for event in g.ledger.events[self.ledger_cursor:]:
                if event['delta']>10 and event['player_id'] is not None:
                    idx=event['player_id']-1
                    px,py=center(tuple(event['context'].get('position',g.players[idx].pos)))
                    self.popups.append([str(event['delta']),px,py-22,1.,COLORS[idx]])
            self.ledger_cursor=len(g.ledger.events)
            for popup in self.popups[:]:
                label,px,py,life,color=popup
                arcade_digits(self.canvas,label,px-14,round(py),color,2)
                popup[2]-=30*dt; popup[3]-=dt
                if popup[3]<=0: self.popups.remove(popup)
            self.canvas.set_clip(None)
            footer='AUTOPLAY - COMPUTER PLAYERS' if self.demo else 'LOCAL ARCADE BATTLE'
            status=self.controller_status()
            message=footer+' | '+status['message']+' | F1 guide  P pause  F2 sound  ESC lobby'
            color=(255,188,87) if status['missing'] or status['disconnected'] else (127,168,198)
            self.text(message,OX,H-12,color,self.micro)
            if g.paused: self.overlay('PAUSED','Press P to continue')
            if g.over:
                self.draw_results()
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

    def advance(self,dt):
        """Fixed 60Hz logic independent of native display frame cadence."""
        if self.phase!=Phase.PLAYING:
            self.fixed_accumulator=0.; return []
        self.fixed_accumulator+=max(0,dt)
        sounds=[]
        while self.fixed_accumulator+1e-10>=1/60:
            if self.demo: steer_demo(self.match)
            for p in self.match.players:
                p.locate_remaining=self.match.countdown(p.locate_remaining,1/60)
            sounds.extend(self.match.update(1/60))
            self.fixed_accumulator-=1/60
        return sounds

    def draw_results(self):
        panel=pg.Surface((660,510),pg.SRCALPHA); panel.fill((7,12,25,245))
        self.canvas.blit(panel,(310,105))
        rows=self.match.rankings()
        tied=sum(r['rank']==1 for r in rows)>1
        self.text('TIED LEADERS' if tied else 'FINAL RANKING',355,125,(255,222,72),self.big)
        for i,row in enumerate(rows):
            idx=row['player_id']-1
            self.text(f"{row['rank']:>2}   P{idx+1}",365,210+i*39,COLORS[idx])
            arcade_digits(self.canvas,f"{row['score']:06}",565,210+i*39,COLORS[idx],3)
        self.text('ENTER replay preset  |  F3-F10 new station  |  ESC lobby',340,575,font=self.small)

    def run(self,frames=0):
        n=0
        while self.running:
            dt=min(.25,self.clock.tick(60)/1000)
            self.events()
            if self.match:
                if not self.demo: self.inputs()
                sounds=self.advance(dt)
                self.audio.consume(self.match.ledger,self.muted)
            self.draw(dt); n+=1
            if frames and n>=frames: break
        pg.quit()

def steer_demo(g):
    """Greedy breadth-first navigation for a visible, reproducible attract demo."""
    for p in g.players:
        if p.lives<=0: continue
        nearby={c for c in g.items if distance(c,p.pos)<=14}
        goals=nearby or set(g.dots)
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
    parser.add_argument('--seed',type=int,help='Reproducible simulation seed.')
    parser.add_argument('--progression',choices=('cycle','repeat','random'),default='cycle',help='Authored map selection policy, not a verified DX rule.')
    parser.add_argument('--locator-seconds',type=float,default=2.,help='Custom locator highlight duration.')
    parser.add_argument('--event-log',help='Save the final match event ledger as JSON on exit.')
    parser.add_argument('--palette',type=int,choices=range(4),help='Select wall palette independently of the starting maze layout. F12 cycles it.')
    args=parser.parse_args()
    if not math.isfinite(args.locator_seconds) or not 0<args.locator_seconds<=10: parser.error('Locator duration must be in (0,10].')
    app=App(simulate_controllers=args.simulate_controllers)
    app.seed=args.seed; app.progression=args.progression; app.locator_seconds=args.locator_seconds
    app.palette_override=args.palette
    app.demo=args.demo
    if args.demo and not args.players: args.players=8
    if args.players: app.count=args.players; app.start()
    app.run(args.frames)
    if args.event_log and app.match: app.match.ledger.write(args.event_log)


