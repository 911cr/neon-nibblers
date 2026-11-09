"""Neon Nibblers — original local arcade maze battle. Python 3.10+."""
import os
import sys
import math
import random
import argparse
import uuid
import time
from collections import deque
from dataclasses import dataclass, field
import pygame as pg
from score_ledger import ScoreLedger, DEFAULT_SCORES
from stations import Phase, phase_for, StationBindings
from map_library import get_map, next_map_index
from arcade_art import maze_background, muncher, foe, power_icon, arcade_digits, dot_sprite, fire_plume,smoke_cloud
from arcade_audio import ArcadeAudio
from cabinet import CabinetStore, spectator_view, atomic_json
from presentation import LifecyclePresentation
from gameplay_tuning import validate_tuning, load_tuning
from arcade_ai import choose_direction
from cabinet_flow import ContinueOffers
from gate_art import draw_station_gate,draw_house,draw_tunnel_neck,gate_geometry,GATE_HATCH
from player_contacts import resolve_bumps,approaching_contact
from maze_transition import render_background,actor_scale
from corridor_motion import CorridorTrack

MAZE_TRANSITION_SECONDS=1.1  # Observed sequence; exact duration remains estimated.

W, H, TILE, TOP = 1280, 720, 20, 50
COLS, ROWS = 59, 31
OX = (W - COLS * TILE) // 2
COLORS = [(255,222,45),(255,108,195),(75,226,245),(255,83,80),
          (111,235,90),(255,155,55),(185,109,255),(90,141,255)]
DIRS = [(1,0),(-1,0),(0,1),(0,-1)]
THEMES = [(get_map(index).name,get_map(index).accent) for index in range(4)]
PALETTES=[theme[1] for theme in THEMES]+[(74,91,255)]
_BAY_CELLS={cell for index in range(4) for cell in get_map(index).spawns}
SPAWN_INTERVAL=3.0  # Custom tuning; commercial cadence is not published.
MAX_ITEMS=12
ITEM_STEP_INTERVAL=.24
ITEMS = {
 'Crown': ('CR','Hunt foes.'),
 'Titan': ('TI','Grow giant and eat smaller rivals.'),
 'Rush': ('RU','Move faster.'),
 'Mist': ('MI','Leave a smoke trail that slows foes.'),
 'Slick': ('SL','Skid uncontrollably.'),
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
    bot: bool = False
    locate_remaining: float = 0.
    recoil: tuple = (0,0)

class Arena:
    def __init__(self, theme):
        spec=get_map(theme)
        self.theme=theme%4
        self.map_id=spec.id; self.map_revision=spec.revision
        self.lanes=set(spec.lanes)
        self.entries=list(spec.entries); self.spawns=list(spec.spawns)
        self.gate_owner={c:i for i,c in enumerate(self.spawns)}
        self.portals=spec.portals; self.den=spec.den
        self.lane_radius=getattr(spec,'lane_radius',32)
        dx,dy,dw,dh=self.den
        self.door=(dx+dw//2,dy)
        self.exit=(self.door[0],dy-2)
        self.homes=tuple((dx+1+i*2,dy+2) for i in range(4))
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
    def __init__(self, count=2, theme=0, seed=None, score_values=None, progression='cycle',rules=None,tuning=None,
                 continue_seconds=0,continue_delay=1):
        if not 0 <= count <= 8: raise ValueError('Player count must be 0..8')
        if progression not in ('cycle', 'repeat', 'random'): raise ValueError('Unknown progression policy')
        self.progression = progression
        self.rules=CabinetStore.validate(rules or {})
        self.tuning=validate_tuning(tuning)
        self.continues=ContinueOffers(continue_seconds,continue_delay)
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
        self.time, self.item_clock, self.foe_clock = float(self.rules['match_seconds']), 0., 0.
        self.item_walk_clock=0.; self.item_directions={}
        self.over, self.paused = False, False
        self.players = [Player(i,(0,0),lives=self.rules['starting_lives']) for i in range(count)]
        self.new_arena(theme)
        self.ledger.append(self, 'match_start', seed=self.seed, count=count,
                           theme=theme, score_values=self.score_values, progression=progression,rules=self.rules,tuning=self.tuning,
                           continue_seconds=continue_seconds,continue_delay=continue_delay)

    def award(self, player, event, **context):
        """One score mutation path, shared by HUD totals, traces and replay checks."""
        rule=({'Crown':'gold_pickup','Titan':'giant_pickup'}.get(context.get('power'),'pickup')
              if event=='pickup' else event)
        delta = self.score_values[rule]
        player.score += delta
        self.ledger.append(self, event, player, delta, position=list(player.pos),score_rule=rule, **context)

    def fill_vacancies(self):
        """Original bot-fill policy; commercial AI difficulty/replacement is unknown.

        Explicit opt-in by the application. Repeated calls preserve eliminated
        actors, human progress, and bot state rather than granting extra lives.
        """
        if self.over or self.paused: return 0
        added = 0
        for idx in range(8):
            if idx < len(self.players):
                old = self.players[idx]
                if old.joined or old.bot: continue
            p = Player(idx, self.arena.spawns[idx], lives=self.rules['starting_lives'],
                       joined=False, bot=True, entry=.8)
            p.direction = (0, 1) if p.pos[1] == 0 else (0, -1)
            if idx < len(self.players): self.players[idx] = p
            else: self.players.append(p)
            self.ledger.append(self, 'bot_join', p, position=list(p.pos), lives=p.lives)
            added += 1
        return added

    def join_station(self, idx):
        """Development free-play policy; commercial joining windows remain unknown."""
        if not 0 <= idx < 8 or self.over or self.paused: return False
        if idx < len(self.players) and getattr(self.players[idx], 'joined', True): return False
        replaced_bot = idx < len(self.players) and self.players[idx].bot
        while len(self.players) < 8:
            p = Player(len(self.players), (0, 0), lives=0)
            p.joined = False
            self.players.append(p)
        p = Player(idx, self.arena.spawns[idx],lives=self.rules['starting_lives'])
        p.joined = True
        p.entry = .8
        p.direction = (0, 1) if p.pos[1] == 0 else (0, -1)
        self.players[idx] = p
        if replaced_bot:
            self.traps = {cell: trap for cell, trap in self.traps.items() if trap[0] != idx}
            self.bump_cooldowns = {pair: timer for pair, timer in self.bump_cooldowns.items() if idx not in pair}
            for ghost, owner in list(self.foe_carriers.items()):
                if owner == idx: self.reset_foe(ghost)
        self.count = sum(getattr(p, 'joined', True) for p in self.players)
        self.ledger.append(self, 'station_join', p, position=list(p.pos), lives=p.lives, replaced_bot=replaced_bot)
        return True

    def rankings(self):
        """Competition ranks preserve ties; station order only stabilizes display."""
        ordered = sorted((p for p in self.players if getattr(p, 'joined', True)),
                         key=lambda p: (-p.score, p.idx))
        return [{'rank': 1 + sum(q.score > p.score for q in ordered),
                 'player_id': p.idx + 1, 'score': p.score, 'lives': p.lives}
                for p in ordered]

    def can_continue_station(self,idx):
        if type(idx) is not int or not 0<=idx<len(self.players) or self.over or self.paused:return False
        if self.rules['match_seconds']>0 and self.time<=0:return False
        p=self.players[idx]
        return p.joined and not p.bot and p.lives<=0 and self.continues.can_accept(idx)

    def continue_station(self,idx):
        """Caller authorizes credit/free-play first; restoration policy is original.

        DX footage establishes a continue prompt, not its score/life policy.
        Retain the score and already-earned bonus flag; restore configured lives.
        """
        if not self.can_continue_station(idx):return False
        old=self.players[idx]
        if not self.continues.accept(idx):return False
        p=Player(idx,self.arena.spawns[idx],lives=self.rules['starting_lives'],
                 score=old.score,bonus_life=old.bonus_life,entry=.8)
        p.direction=(0,1) if p.pos[1]==0 else (0,-1)
        self.players[idx]=p
        self.traps={cell:trap for cell,trap in self.traps.items() if trap[0]!=idx}
        self.bump_cooldowns={pair:t for pair,t in self.bump_cooldowns.items() if idx not in pair}
        for ghost,owner in list(self.foe_carriers.items()):
            if owner==idx:self.reset_foe(ghost)
        self.ledger.append(self,'station_continue',p,lives=p.lives,position=list(p.pos),
                           score_preserved=True,bonus_life_preserved=p.bonus_life)
        return True

    def snapshot(self):
        """JSON-safe complete logic state for deterministic regression comparisons."""
        def freeze(value):
            if isinstance(value, dict):
                return [[freeze(k), freeze(v)] for k, v in sorted(value.items(), key=lambda p: repr(p[0]))]
            if isinstance(value, set): return [freeze(v) for v in sorted(value)]
            if isinstance(value, (list, tuple)): return [freeze(v) for v in value]
            return value
        state = {k: freeze(v) for k, v in vars(self).items()
                 if k not in ('arena', 'players', 'rng', 'ledger','continues')}
        state['continues']=self.continues.snapshot()
        state['arena_theme'] = self.arena.theme
        state['map_id'] = self.arena.map_id
        state['map_revision'] = self.arena.map_revision
        state['players'] = [freeze(vars(p)) for p in self.players]
        state['rng'] = freeze(self.rng.getstate())
        return state

    def new_arena(self, theme):
        self.transition_from=None
        self.transition_age=0.
        self.refill_pending={}
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
            p.entry=.8; p.stun=0.; p.clock=0.; p.recoil=(0,0)
            p.effects.clear()
        self.foes = list(self.arena.homes)
        self.foe_previous=list(self.foes)
        self.foe_modes=['house']*4
        self.foe_release=[.9+i*.6 for i in range(4)]
        self.foe_carriers={}
        self.foe_ticks=[0.]*4
        self.foe_zapped=[0.]*4
        self.foe_stun = 0.
        self.foe_clock=0.
        for c in ((1,1),(COLS-2,1),(1,ROWS-2),(COLS-2,ROWS-2)):
            if c in self.arena.floor and len(self.items)<self.tuning['max_items']: self.items[c]='Crown'
        for anchor in ((COLS//2,9),(COLS//2,21)):
            c=min(self.arena.lanes,key=lambda c:(distance(c,anchor),c))
            if len(self.items)<self.tuning['max_items']:self.items[c]='Titan'
        for name in self.rng.sample([k for k in ITEMS if k not in ('Crown','Titan')],3): self.spawn_item(name)

    def transition_arena(self, theme):
        """Keep the running field across a layout change, as observed in DX.

        Exact commercial relocation, persistence and refill timings are unknown.
        Our deterministic policy preserves legal positions first, then moves
        disappearing cells to the nearest free public lane; no respawn/immunity.
        """
        old=self.arena
        self.arena=Arena(theme%4)
        self.transition_from=old.theme
        self.transition_age=0.
        # Reserve unchanged living positions before assigning displaced actors.
        reserved=set()
        displaced=[]
        for p in self.players:
            if p.lives<=0 or not (p.joined or p.bot):continue
            if self.arena.can_enter(p.pos,p) and p.pos not in reserved:reserved.add(p.pos)
            else:displaced.append(p)
        for p in displaced:
            p.pos=min(self.arena.lanes-reserved,key=lambda c:(distance(c,p.pos),c))
            reserved.add(p.pos)
        for i,mode in enumerate(self.foe_modes):
            if mode in ('roaming','eyes') and self.foes[i] not in self.arena.lanes:
                self.foes[i]=min(self.arena.lanes,key=lambda c:(distance(c,self.foes[i]),c))
            # All catalog layouts share the same house/door. Keep progress on
            # its entry/exit track rather than resetting release/recovery.
            if self.foe_previous[i] not in self.arena.lanes:self.foe_previous[i]=self.foes[i]
        self.sync_carriers()
        occupied={c for c in self.items if c in self.arena.lanes}
        items={};directions={}
        for cell,name in sorted(self.items.items()):
            target=cell if cell in self.arena.lanes else min(
                self.arena.lanes-occupied,key=lambda c:(distance(c,cell),c))
            occupied.add(target);items[target]=name
            directions[target]=self.item_directions.get(cell)
        self.items=items;self.item_directions=directions
        self.traps={c:value for c,value in self.traps.items() if c in self.arena.lanes}
        self.smoke={c:value for c,value in self.smoke.items() if c in self.arena.lanes}
        self.dots=set()
        # Stagger visible/collectible dots together; hidden dots cannot score.
        self.refill_pending={c:.6+((c[0]*37+c[1]*61)%101)/100*.5
                             for c in self.arena.lanes-set(self.arena.entries)}

    def spawn_item(self, name=None):
        if len(self.items)>=self.tuning['max_items']: return
        cells = sorted(self.arena.lanes - set(self.items) - {p.pos for p in self.players})
        if cells: self.items[self.rng.choice(cells)] = name or self.rng.choice(list(ITEMS))

    def reset_foe(self, index, returning=True):
        self.foe_carriers.pop(index,None)
        self.foe_modes[index]='eyes' if returning else 'house'
        self.foe_release[index]=1.2
        if not returning: self.foes[index]=self.arena.homes[index]

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

    def lane_distances(self,goal):
        """Legal graph distances; a wall is never a shortcut for ghost AI."""
        if goal not in self.arena.lanes:return {}
        distances={goal:0};queue=deque([goal])
        while queue:
            cell=queue.popleft()
            for direction in DIRS:
                nxt=self.arena.step(cell,direction)
                if nxt in self.arena.lanes and nxt not in distances:
                    distances[nxt]=distances[cell]+1;queue.append(nxt)
        return distances

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
        interval=self.tuning['ghost_step_seconds']
        if self.foe_clock+1e-10<interval: return
        self.foe_clock=max(0.,self.foe_clock-interval)%interval
        target_distances={}
        for i,f in enumerate(self.foes):
            while len(self.foe_previous)<=i:self.foe_previous.append(f)
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
                if x!=self.arena.door[0]: self.foes[i]=(x+(1 if x<self.arena.door[0] else -1),y)
                elif y>self.arena.exit[1]: self.foes[i]=(x,y-1)
                else: self.foe_modes[i]='roaming'
                continue
            if mode=='entering':
                x,y=f; home,home_y=self.arena.homes[i]
                if y<home_y: self.foes[i]=(x,y+1)
                elif x!=home: self.foes[i]=(x+(1 if x<home else -1),y)
                else:
                    self.foe_modes[i]='house'; self.foe_release[i]=1.2
                continue
            if mode=='eyes':
                if f==self.arena.exit:
                    self.foe_modes[i]='entering'
                else: self.foes[i]=self.next_toward(f,self.arena.exit)
                continue
            slow=self.tuning['quake_multiplier'] if self.quake>0 else 1
            if any(distance(f,c)<=self.tuning['smoke_radius'] for c in self.smoke): slow*=self.tuning['smoke_multiplier']
            if self.foe_stun>0 or self.foe_zapped[i]>0 or self.foe_ticks[i]+1e-10<interval*slow: continue
            self.foe_ticks[i]=max(0.,self.foe_ticks[i]-interval*slow)%(interval*slow)
            targets=[p for p in self.players if p.lives>0 and p.pos in self.arena.lanes
                     and not self.active(p,'Veil')]
            options=[self.arena.step(f,d) for d in DIRS if self.arena.step(f,d) in self.arena.lanes]
            if not options: continue
            forward=[cell for cell in options if cell!=self.foe_previous[i]]
            if forward:options=forward
            if targets and self.rng.random()<.7:
                for target in targets:
                    if target.idx not in target_distances:target_distances[target.idx]=self.lane_distances(target.pos)
                target=min(targets,key=lambda p:target_distances[p.idx].get(f,float('inf')))
                distances=target_distances[target.idx]
                options.sort(key=lambda c:distances.get(c,float('inf')),reverse=self.active(target,'Crown') or self.active(target,'Titan'))
                self.foes[i]=options[0]
            else: self.foes[i]=self.rng.choice(options)
            self.foe_previous[i]=f

    def active(self,p,key): return p.effects.get(key,0)>0

    def player_interval(self,p):
        interval=self.tuning['rush_step_seconds'] if self.active(p,'Rush') else self.tuning['player_step_seconds']
        if self.active(p,'Slick'):interval=self.tuning['slick_step_seconds']
        if self.quake>0:interval*=self.tuning['quake_multiplier']
        return interval

    def hurt(self,p):
        if p.lives<=0 or p.safe>0 or self.active(p,'Titan'): return False
        old_position = list(p.pos)
        p.lives -= 1
        p.pos, p.safe = self.arena.spawns[p.idx], 3.
        p.direction, p.wanted = (0,0),(0,0)
        p.entry=.8; p.stun=0.; p.clock=0.; p.recoil=(0,0)
        p.effects.clear()
        self.ledger.append(self, 'player_hurt', p, position=old_position, lives=p.lives)
        if p.lives==0 and p.joined and not p.bot and not (self.rules['match_seconds']>0 and self.time<=0):
            if self.continues.open(p.idx):
                self.ledger.append(self,'continue_offered',p,duration=self.continues.seconds,
                                   reveal_delay=self.continues.delay)
        return True

    def collect(self,p,name):
        duration=self.tuning['durations'].get(name,0.)
        self.award(p, 'pickup', power=name, duration=duration,
                   expires_at=round(self.elapsed+duration,9) if duration else None)
        p.last = name
        if name == 'Heart':
            old_lives = p.lives
            p.lives = min(5,p.lives+1)
            self.ledger.append(self, 'extra_life', p, lives=p.lives, gained=p.lives-old_lives)
        elif name=='Spark':
            self.zaps.append((p.pos,.5))
            for q in self.players:
                if q is not p and q.lives>0 and distance(q.pos,p.pos)<=self.tuning['spark_radius']: q.stun=duration
            for i,f in enumerate(self.foes):
                if distance(f,p.pos)<=self.tuning['spark_radius']: self.foe_zapped[i]=duration
        elif name=='Quake': self.quake=duration
        elif name=='Mist':
            p.effects[name]=duration
            # The published effect includes a smoke explosion. It must also
            # occur for a stationary collector, before any movement trail.
            self.smoke[p.pos]=self.tuning['smoke_seconds']
        elif name!='Heart': p.effects[name]=duration

    def fire_cells(self, p):
        cells=[]; c=p.pos
        if p.direction==(0,0): return cells
        for _ in range(self.tuning['flame_cells']):
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
        resolve_bumps(self,[(p,q)],previous)

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
            if self.rules['bonus_threshold'] and p.score>=self.rules['bonus_threshold'] and not p.bonus_life:
                p.bonus_life=True
                old_lives = p.lives
                if p.lives>0: p.lives=min(5,p.lives+1)
                self.ledger.append(self, 'score_bonus_life', p, lives=p.lives, gained=p.lives-old_lives)

    def combat(self,previous=None,old_foes=None):
        event_start=len(self.ledger.events)
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
        contacts=[]
        for i,p in enumerate(self.players):
            for q in self.players[i+1:]:
                if min(p.lives,q.lives)<=0: continue
                if not approaching_contact(self,p,q,previous): continue
                a = self.active(p,'Titan')
                b = self.active(q,'Titan')
                if a and not b and self.hurt(q): self.award(p, 'rival_eaten', target_player_id=q.idx+1)
                if b and not a and self.hurt(p): self.award(q, 'rival_eaten', target_player_id=p.idx+1)
                if a==b: contacts.append((p,q))
        harmed={e['player_id']-1 for e in self.ledger.events[event_start:]
                if e['event']=='player_hurt'}
        contacts=[pair for pair in contacts if not any(p.idx in harmed for p in pair)]
        if contacts:resolve_bumps(self,contacts,previous)
        else:self.separate_overlaps()

    def update(self,dt):
        if self.over or self.paused: return []
        if not math.isfinite(dt) or dt < 0: raise ValueError('dt must be finite and non-negative')
        self.elapsed += dt; self.tick += 1
        if self.transition_from is not None:
            self.transition_age+=dt
            ready={c for c,at in self.refill_pending.items() if at<=self.transition_age+1e-10}
            self.dots.update(ready)
            for c in ready:del self.refill_pending[c]
        sounds=[]
        expired_continues=self.continues.advance(dt)
        for idx in expired_continues:
            self.ledger.append(self,'continue_expired',self.players[idx])
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
            # A legal fresh turn can face immediately without granting extra
            # distance. Movement still spends the same cadence budget.
            if p.recoil==(0,0) and not self.active(p,'Slick') and p.wanted!=(0,0):
                if self.arena.can_enter(self.arena.step(p.pos,p.wanted),p):p.direction=p.wanted
            p.clock+=dt
            speed=self.player_interval(p)
            if p.clock+1e-10>=speed:
                p.clock=max(0.,p.clock-speed)%speed
                if p.recoil!=(0,0):
                    # One legal outward step survives held input/autoplay.
                    # It uses normal movement cadence rather than teleporting.
                    p.direction=p.recoil; p.recoil=(0,0)
                elif self.active(p,'Slick'):
                    if not self.arena.can_enter(self.arena.step(p.pos,p.direction),p) or p.direction==(0,0):
                        options=[d for d in DIRS if self.arena.can_enter(self.arena.step(p.pos,d),p)]
                        if options: p.direction=self.rng.choice(options)
                elif self.arena.can_enter(self.arena.step(p.pos,p.wanted),p): p.direction=p.wanted
                if self.active(p,'Mist') and p.pos in self.arena.lanes: self.smoke[p.pos]=self.tuning['smoke_seconds']
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
        spawn_interval=self.tuning['spawn_seconds']
        if self.item_clock+1e-10>=spawn_interval:
            self.item_clock=max(0.,self.item_clock-spawn_interval)%spawn_interval
            if len(self.items)<self.tuning['max_items']: self.spawn_item()
        self.item_walk_clock+=dt
        item_interval=self.tuning['item_step_seconds']
        if self.item_walk_clock+1e-10>=item_interval:
            self.item_walk_clock=max(0.,self.item_walk_clock-item_interval)%item_interval
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
        timed_out=self.rules['match_seconds']>0 and self.time<=0
        if timed_out or not any(p.joined and p.lives>0 for p in self.players) and not self.continues.active:
            self.over=True
            if timed_out:self.continues.clear()
            self.ledger.append(self, 'match_end', reason='time' if timed_out else 'elimination', rankings=self.rankings(),
                               continue_timeout=not timed_out and bool(expired_continues))
        elif not self.dots and not self.refill_pending:
            for p in self.players:
                if p.lives>0: self.award(p, 'stage_clear')
            self.stage+=1
            self.transition_arena(next_map_index(self.arena.theme, self.progression, self.rng))
            self.ledger.append(self, 'stage_start', theme=self.arena.theme,previous_theme=self.transition_from,
                               actors_preserved=True,refill_seconds=MAZE_TRANSITION_SECONDS)
            self.award_score_lives()
            sounds.append('power')
        return sounds

def add(a,b): return a[0]+b[0],a[1]+b[1]
def distance(a,b): return abs(a[0]-b[0])+abs(a[1]-b[1])
def center(c):
    x=OX+c[0]*TILE+TILE//2
    if c in _BAY_CELLS:return x,TOP-20 if c[1]==0 else TOP+ROWS*TILE+20
    return x,TOP+c[1]*TILE+TILE//2

def station_hud(spawn,score=0):
    """Reserve clearance beside each bay for every digit, life and prompt."""
    sx=center(spawn)[0]
    sy=4 if spawn[1]<ROWS//2 else H-45
    label=str(score)
    scale=max(1,min(3,108//(6*len(label))))
    return {'x':sx+50,'y':sy,'label':label,'scale':scale,
            'score':pg.Rect(sx+50,sy,(6*len(label)-1)*scale,7*scale),
            'lives':pg.Rect(sx+50,sy+25,48,7)}

class App:
    def __init__(self, simulate_controllers=False,cabinet=None):
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
        self.count=2; self.theme=3; self.match=None; self.help=False; self.muted=False
        self.simulate_controllers=simulate_controllers
        self.controller_notice_until=0
        self.bindings=StationBindings(); self.pair_station=None
        self.pads={}; self.refresh_pads(); self.sounds={}
        self.fixed_accumulator=0.; self.ledger_cursor=0
        self.locator_seconds=2.0  # Original timing unknown; configurable approximation.
        self.seed=None; self.progression='cycle'; self.pair_error=''
        self.tuning=validate_tuning()
        self.untimed=False
        self.continue_seconds=10.;self.continue_delay=1.
        self.palette_override=None  # Presentation is independent of maze topology.
        self.match_palette=None  # A layout change alone is not a color-change trigger.
        self.cabinet=cabinet if cabinet is not None else CabinetStore()
        self.operator_open=False;self.operator_index=0;self.operator_draft={}
        self.status_notice='';self.scores_open=False;self.idle_time=0.
        self.session_id=str(uuid.uuid4());self.spectator_path=None;self.publish_clock=0.
        self.pending_results=[];self.next_save_retry=0.;self.name_entry=None
        self.presentation=LifecyclePresentation()
        self.demo=False; self.visual_positions={}; self.animation_time=0.
        self.motion_tracks={'players':{},'ghosts':{},'items':{}}
        self.keyboard_pressed={};self.keyboard_serial=0
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
        if not 0<=idx<8:return
        self.save_result()
        if self.phase in (Phase.GUIDE,Phase.PAUSED): return
        if self.match and not self.match.over and idx<len(self.match.players):
            p=self.match.players[idx]
            if p.joined and p.lives<=0:
                if not self.match.can_continue_station(idx):return
                if not self.cabinet.pay(1):
                    self.status_notice=self.cabinet.error or 'Press INSERT for a credit, then this station Start.';return
                self.match.continue_station(idx)
                self.match.players[idx].locate_remaining=self.locator_seconds
                self.presentation.radii.pop(idx,None)
                self.status_notice='';return
        fresh=self.phase in (Phase.ATTRACT,Phase.RESULTS)
        needs_join=fresh or idx>=len(self.match.players) or not self.match.players[idx].joined
        if needs_join and not self.cabinet.pay(1):
            self.status_notice='Insert credit: press C in the lobby.';return
        if self.phase in (Phase.ATTRACT,Phase.RESULTS):
            self.match_palette=self.theme
            self.match=Match(0,self.theme,seed=self.seed,progression=self.progression,rules=self.match_rules(),tuning=self.tuning,
                             continue_seconds=self.continue_seconds,continue_delay=self.continue_delay)
            self.session_id=str(uuid.uuid4())
            self.reset_visuals()
            self.prepare_mazes()
        if idx>=len(self.match.players) or not self.match.players[idx].joined:
            self.match.join_station(idx)
        if self.cabinet.settings['fill_bots']:self.match.fill_vacancies()
        p=self.match.players[idx]
        if p.lives>0:
            p.locate_remaining=self.locator_seconds
            self.match.ledger.append(self.match,'locate',p,duration=self.locator_seconds)

    def events(self):
        self.save_result(False)
        for e in pg.event.get():
            if e.type in (pg.KEYDOWN,pg.JOYBUTTONDOWN,pg.MOUSEBUTTONDOWN):
                self.idle_time=0.;self.attract_page=None
            if e.type==pg.QUIT: self.running=False
            if self.name_entry is not None:
                if e.type==pg.KEYDOWN:self.name_entry_event(e)
                continue
            if self.operator_open:
                if e.type==pg.KEYDOWN:self.operator_event(e.key)
                continue
            if e.type in (pg.JOYDEVICEADDED,pg.JOYDEVICEREMOVED): self.refresh_pads()
            if e.type==pg.KEYUP:self.keyboard_pressed.pop(e.key,None)
            if e.type==pg.KEYDOWN and any(e.key in keys for keys in KEYS):
                if e.key not in self.keyboard_pressed:
                    self.keyboard_serial+=1;self.keyboard_pressed[e.key]=self.keyboard_serial
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
            if e.key==pg.K_n and self.match and self.match.over:
                self.begin_name_entry();continue
            if e.key==pg.K_F11 and (not self.match or self.match.over):
                self.operator_open=True;self.operator_draft=dict(self.cabinet.settings);continue
            if e.key==pg.K_c and not self.match or e.key==pg.K_INSERT and self.match and not self.match.over and self.match.continues.active:
                if self.cabinet.add_credit():self.status_notice=f'{self.cabinet.credits} credits available'
                else:self.status_notice=self.cabinet.error
                continue
            if e.key==pg.K_h and not self.match:
                self.scores_open=not self.scores_open;continue
            if pg.K_F3<=e.key<=pg.K_F10:
                idx=e.key-pg.K_F3
                if getattr(e,'mod',0)&pg.KMOD_SHIFT and self.match is None:
                    self.pair_station=idx; self.pair_error=''
                else: self.station_action(idx)
                continue
            if self.match and not self.match.over:
                for p in self.match.players:
                    if p.bot:continue
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
                current=self.wall_palette()
                self.palette_override=(current+1)%len(PALETTES)
            elif e.key==pg.K_RETURN and (not self.match or self.match.over): self.start()
            elif e.key==pg.K_p and self.match: self.match.paused=not self.match.paused
            elif not self.match:
                if pg.K_1<=e.key<=pg.K_8: self.count=e.key-pg.K_0
                if e.key==pg.K_TAB: self.theme=(self.theme+1)%4

    def start(self):
        self.save_result()
        if not self.cabinet.pay(self.count):
            self.status_notice=f'{self.count} credits needed. Press C in the lobby.';return False
        self.match_palette=self.theme
        self.match=Match(self.count,self.theme,seed=self.seed,progression=self.progression,rules=self.match_rules(),tuning=self.tuning,
                         continue_seconds=self.continue_seconds,continue_delay=self.continue_delay); self.help=False
        if self.cabinet.settings['fill_bots']:self.match.fill_vacancies()
        self.session_id=str(uuid.uuid4());self.scores_open=False;self.status_notice='';self.name_entry=None
        self.reset_visuals()
        self.prepare_mazes()
        return True

    def prepare_mazes(self):
        """Build costly wall geometry before play, avoiding a first-clear hitch."""
        palette,accent=self.wall_style()
        missing=[Arena(theme) for theme in range(4)
                 if (get_map(theme).id,get_map(theme).revision,palette) not in self.backgrounds]
        if not missing:return
        self.canvas.fill((0,0,4))
        self.text('Preparing mazes...',W//2-105,H//2-20,(220,230,255),self.font)
        self.screen.blit(pg.transform.smoothscale(self.canvas,self.screen.get_size()),(0,0))
        pg.display.flip();pg.event.pump()
        for arena in missing:
            key=(arena.map_id,arena.map_revision,palette)
            if len(self.backgrounds)>=24:self.backgrounds.pop(next(iter(self.backgrounds)))
            self.backgrounds[key]=maze_background(arena.space,COLS,ROWS,TILE,accent,arena.lane_radius)

    def wall_palette(self):
        if self.palette_override is not None:return self.palette_override
        if self.match is None:return self.theme
        return self.match.arena.theme if self.match_palette is None else self.match_palette

    def wall_style(self):
        """DX footage shows hue following and cycling among active giants.

        Exact period/order are not recovered: this presentation uses a documented
        1.25-second station-order cycle. It never changes collision or scoring.
        """
        if self.match:
            giants=sorted(p.idx for p in self.match.players
                          if p.lives>0 and self.match.active(p,'Titan'))
            if giants:
                idx=giants[int(self.match.elapsed/1.25)%len(giants)]
                return ('giant',idx),COLORS[idx]
        palette=self.wall_palette()
        return palette,PALETTES[palette]

    def match_rules(self):
        rules=dict(self.cabinet.settings)
        if self.untimed:rules['match_seconds']=0
        return rules

    def save_result(self,force=True):
        queued={token for rows,token in self.pending_results}
        if self.match is not None and self.match.over and self.session_id not in self.cabinet.recorded and self.session_id not in queued:
            self.pending_results.append((self.match.rankings(),self.session_id))
        if not force and time.monotonic()<self.next_save_retry:return
        while self.pending_results:
            rows,token=self.pending_results[0]
            if token in self.cabinet.recorded or self.cabinet.record_rows(rows,token):self.pending_results.pop(0)
            else:
                self.status_notice=self.cabinet.error;self.next_save_retry=time.monotonic()+1;break

    def begin_name_entry(self):
        self.save_result()
        self.help=False
        if self.session_id not in self.cabinet.recorded:
            self.status_notice='Scores are not saved yet. Check storage, then press N to retry.';return
        rows=[row for row in self.cabinet.high_scores if row.get('session')==self.session_id]
        if not rows:
            self.status_notice='No score from this match qualified for the saved top 20.';return
        self.name_entry={'rows':rows,'index':0,'letters':list('AAA'),'cursor':0,'error':''}
        self.status_notice=''

    def name_entry_event(self,event):
        entry=self.name_entry
        if event.key==pg.K_ESCAPE:
            self.name_entry=None;self.status_notice='Initials entry closed. Saved scores are retained.';return
        if event.key==pg.K_RETURN:
            row=entry['rows'][entry['index']]
            if not self.cabinet.rename_score(self.session_id,row['player_id'],''.join(entry['letters'])):
                entry['error']=self.cabinet.error;return
            entry['index']+=1
            if entry['index']==len(entry['rows']):
                self.name_entry=None;self.status_notice='Initials saved.';return
            entry.update(letters=list('AAA'),cursor=0,error='');return
        if event.key in (pg.K_LEFT,pg.K_RIGHT):
            entry['cursor']=(entry['cursor']+(1 if event.key==pg.K_RIGHT else -1))%3
        elif event.key in (pg.K_UP,pg.K_DOWN):
            i=entry['cursor'];entry['letters'][i]=chr(65+(ord(entry['letters'][i])-65+(1 if event.key==pg.K_UP else -1))%26)
        elif event.key==pg.K_BACKSPACE:
            entry['cursor']=max(0,entry['cursor']-1);entry['letters'][entry['cursor']]='A'
        else:
            char=getattr(event,'unicode','').upper()
            if len(char)==1 and char in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                entry['letters'][entry['cursor']]=char;entry['cursor']=min(2,entry['cursor']+1)

    def draw_name_entry(self):
        entry=self.name_entry;row=entry['rows'][entry['index']]
        panel=pg.Surface((900,410));panel.fill((9,18,32));self.canvas.blit(panel,(190,155))
        self.text('NEON NIBBLERS | INITIALS',270,185,(104,242,209),self.big)
        self.text(f"P{row['player_id']}   {row['score']:06}   Entry {entry['index']+1}/{len(entry['rows'])}",390,260,COLORS[row['player_id']-1])
        for i,char in enumerate(entry['letters']):
            self.text(char,510+i*90,315,(255,225,90),self.big)
            if i==entry['cursor']:pg.draw.line(self.canvas,(104,242,209),(508+i*90,377),(553+i*90,377),3)
        self.text('Type A-Z | arrows select/change | Backspace corrects',340,420,font=self.small)
        self.text('ENTER saves this name | ESC closes without saving this draft',300,455,font=self.small)
        if entry['error']:self.text(entry['error'],245,505,(255,155,110),self.small)

    def operator_event(self,key):
        fields=list(self.cabinet.settings)
        choices={'starting_lives':[1,2,3,4,5],'bonus_threshold':[0,5000,10000,20000,50000],
                 'match_seconds':[0,60,90,120,180,300,600],
                 'free_play':[False,True],'attract_sound':[False,True],'fill_bots':[False,True]}
        if key==pg.K_ESCAPE:self.operator_open=False
        elif key in (pg.K_UP,pg.K_DOWN):self.operator_index=(self.operator_index+(1 if key==pg.K_DOWN else -1))%len(fields)
        elif key in (pg.K_LEFT,pg.K_RIGHT):
            name=fields[self.operator_index];values=choices[name];old=self.operator_draft[name]
            index=values.index(old) if old in values else 0
            self.operator_draft[name]=values[(index+(1 if key==pg.K_RIGHT else -1))%len(values)]
        elif key==pg.K_RETURN:
            if self.cabinet.configure(self.operator_draft):
                self.operator_open=False;self.status_notice='Operator settings saved.'
            else:self.status_notice=self.cabinet.error

    def draw_operator(self):
        panel=pg.Rect(260,130,760,470)
        pg.draw.rect(self.canvas,(8,15,28),panel,border_radius=14)
        pg.draw.rect(self.canvas,(80,210,230),panel,2,border_radius=14)
        self.text('OPERATOR SETTINGS',310,155,(255,225,90),self.big)
        names={'starting_lives':'Starting lives','bonus_threshold':'Bonus life score (0 disables)',
               'match_seconds':'Time limit (0 = no limit)','free_play':'Free play','attract_sound':'Attract sound','fill_bots':'AI in vacant stations'}
        for index,(name,value) in enumerate(self.operator_draft.items()):
            color=(255,230,100) if index==self.operator_index else (220,230,245)
            display=('ON' if value else 'OFF') if type(value) is bool else value
            self.text(('> ' if index==self.operator_index else '  ')+names[name],310,250+index*45,color)
            self.text(display,870,250+index*45,color)
        self.text('Up / Down select   Left / Right change   Enter save   Esc cancel',300,520,font=self.small)
        self.text(self.status_notice or 'Changes apply to the next match. Timings are adaptation settings.',300,556,font=self.small)

    def draw_high_scores(self):
        panel=pg.Rect(300,120,680,480);pg.draw.rect(self.canvas,(8,15,28),panel,border_radius=12)
        self.text('LOCAL HIGH SCORES',345,145,(255,225,90),self.big)
        rows=self.cabinet.high_scores[:10]
        if not rows:self.text('Complete a match to set the first score.',365,250)
        for index,row in enumerate(rows):
            self.text(f"{index+1:2}   {row['name']}",350,225+index*30)
            self.text(row['score'],790,225+index*30,(255,225,90))
        self.text('H closes   |   Scores are stored on this computer',370,560,font=self.small)

    def draw_attract(self):
        page=int((self.idle_time-12)//4)%12
        if page==11:
            self.draw_high_scores();return
        name=list(ITEMS)[page]
        pg.draw.rect(self.canvas,(6,12,23),(270,265,740,340),border_radius=15)
        self.text('POWER-UP SPOTLIGHT',390,285,(255,225,90),self.big)
        power_icon(self.canvas,(640,405),name,self.animation_time,96)
        label=DISPLAY_NAMES[name];self.text(label,640-self.big.size(label)[0]//2,465,(110,240,220),self.big)
        desc=self.power_description(name);self.text(desc,640-self.font.size(desc)[0]//2,530)
        self.text('Press a station Start or Enter to play',480,575,(255,225,90),self.small)

    def power_description(self,name):
        tuning=self.match.tuning if self.match else self.tuning
        duration=tuning['durations'].get(name)
        return ITEMS[name][1]+(f' ({duration:g}s)' if duration is not None else '')

    def reset_visuals(self):
        self.fixed_accumulator=0.; self.ledger_cursor=0
        self.visual_positions={}; self.visual_foes={}; self.score_memory={}; self.popups=[]; self.visual_items={}
        self.presentation.reset()
        self.motion_tracks={'players':{},'ghosts':{},'items':{}}

    def corridor_position(self,kind,key,old,target,dt,interval,wrap):
        """Render logical waypoint motion without exponential corner cutting."""
        local=(old[0]-OX,old[1]-TOP)
        track=self.motion_tracks[kind].get(key)
        if track is None:
            track=CorridorTrack(local);self.motion_tracks[kind][key]=track
        elif distance(track.position,local)>1e-5:track.reset(local)
        point=track.sample((target[0]-OX,target[1]-TOP),dt,TILE/interval,
                           (COLS*TILE,None) if wrap else None)
        return point[0]+OX,point[1]+TOP

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
        # Most recently pressed direction wins when two keys overlap. Fixed
        # iteration priority used to overwrite fresh RIGHT turns with held UP.
        for key in tuple(self.keyboard_pressed):
            if not keys[key]:self.keyboard_pressed.pop(key,None)
        for group in KEYS:
            for key in group:
                if keys[key] and key not in self.keyboard_pressed:
                    self.keyboard_serial+=1;self.keyboard_pressed[key]=self.keyboard_serial
        self.bindings.sync(self.pads)
        for p in self.match.players:
            if p.bot:continue
            wanted=None
            held=[key for key in KEYS[p.idx] if keys[key]]
            if held:
                latest=max(held,key=lambda key:self.keyboard_pressed[key])
                wanted=DIRS[KEYS[p.idx].index(latest)]
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

    def transition_geometry(self,arena,palette,accent):
        """Geometry-only frame; station text and actors never get rescaled."""
        frame=pg.Surface((W,H));frame.fill((0,0,4))
        key=(arena.map_id,arena.map_revision,palette)
        if key not in self.backgrounds:
            if len(self.backgrounds)>=24:self.backgrounds.pop(next(iter(self.backgrounds)))
            self.backgrounds[key]=maze_background(arena.space,COLS,ROWS,TILE,accent,arena.lane_radius)
        frame.blit(self.backgrounds[key],(OX,TOP))
        dx,dy,dw,dh=arena.den
        draw_house(frame,pg.Rect(OX+dx*TILE+5,TOP+dy*TILE+5,dw*TILE-10,dh*TILE-10),accent,center(arena.door)[0])
        for idx,spawn in enumerate(arena.spawns):
            p=self.match.players[idx] if idx<len(self.match.players) else None
            opening=p and p.lives>0 and (p.entry>0 or p.pos==spawn)
            draw_station_gate(frame,center(spawn)[0],TOP+4 if spawn[1]==0 else TOP+ROWS*TILE-4,
                              spawn[1]==0,accent,opening)
        for row in arena.portals:
            for side in (-1,1):
                draw_tunnel_neck(frame,OX if side<0 else OX+COLS*TILE,center((0,row))[1],side,accent)
        return frame

    def draw(self,dt=1/60):
        self.canvas.fill((0,0,4))
        if self.match and self.phase not in (Phase.PLAYING,Phase.CONTINUE):dt=0.
        self.animation_time+=dt
        if not self.match:
            palette=self.theme if self.palette_override is None else self.palette_override
            lobby_key=('lobby',self.theme,palette)
            if lobby_key not in self.backgrounds:
                arena=Arena(self.theme)
                self.backgrounds[lobby_key]=maze_background(arena.space,COLS,ROWS,TILE,PALETTES[palette],arena.lane_radius)
            self.canvas.blit(self.backgrounds[lobby_key],(OX,TOP))
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
            self.text(f"Collect dots. Claim powers. Outscore friends in {self.cabinet.settings['match_seconds']} seconds.",W//2-265,408)
            for i in range(8):
                self.text(f'P{i+1}  F{i+3} START   {KEYLABELS[i]}',W//2-270+(i//4)*360,462+(i%4)*33,COLORS[i])
            pairing=f'PAIR P{self.pair_station+1}: press controller button 1' if self.pair_station is not None else 'SHIFT + F3-F10: pair a controller to a station'
            self.text(pairing,(W-self.font.size(pairing)[0])//2,620,(255,222,72))
            if self.pair_error: self.text(self.pair_error,360,647,(255,155,110),self.small)
            self.text('TAB arena  |  F1 guide  |  F2 sound  |  ESC quit',W//2-190,667)
            credit='FREE PLAY' if self.cabinet.settings['free_play'] else f'CREDITS {self.cabinet.credits}   C inserts a credit'
            self.text(credit+'   |   H scores   F11 operator',W//2-210,700,font=self.small)
            if self.status_notice:self.text(self.status_notice,360,645,(255,200,100),self.small)
            if self.idle_time>=12 and not self.scores_open and not self.operator_open:self.draw_attract()
            if self.scores_open:self.draw_high_scores()
        else:
            g=self.match
            self.presentation.update(g,dt)
            for event in g.ledger.events[self.ledger_cursor:]:
                if event['event'] in ('player_hurt','station_join') and event['player_id'] is not None:
                    self.visual_positions.pop(event['player_id']-1,None)
                elif event['event']=='stage_start' and not event['context'].get('actors_preserved'):
                    self.visual_positions.clear();self.visual_foes.clear();self.visual_items.clear()
            palette,accent=self.wall_style()
            morph=g.transition_from is not None and g.transition_age<MAZE_TRANSITION_SECONDS
            progress=g.transition_age/MAZE_TRANSITION_SECONDS if morph else 1.
            pulse=actor_scale(progress) if morph else 1.
            background_key=(g.arena.map_id,g.arena.map_revision,palette)
            if background_key not in self.backgrounds:
                if len(self.backgrounds)>=24:self.backgrounds.pop(next(iter(self.backgrounds)))
                self.backgrounds[background_key]=maze_background(g.arena.space,COLS,ROWS,TILE,accent,g.arena.lane_radius)
            if morph:
                before=self.transition_geometry(Arena(g.transition_from),palette,accent)
                after=self.transition_geometry(g.arena,palette,accent)
                self.canvas.blit(render_background(before,after,progress),(0,0))
            else:self.canvas.blit(self.backgrounds[background_key],(OX,TOP))
            # Thin enclosure and colored border stations, leaving the maze dominant.
            dx,dy,dw,dh=g.arena.den
            gate=pg.Rect(OX+dx*TILE+5,TOP+dy*TILE+5,dw*TILE-10,dh*TILE-10)
            door_x=center(g.arena.door)[0]
            if not morph:draw_house(self.canvas,gate,accent,door_x)
            for idx,spawn in enumerate(g.arena.spawns):
                sx=center(spawn)[0]
                upper=spawn[1]<ROWS//2
                mouth_y=TOP+4 if upper else TOP+ROWS*TILE-4
                active=idx<len(g.players) and g.players[idx].joined
                color=COLORS[idx] if active else tuple(max(85,c//2) for c in COLORS[idx])
                occupant=g.players[idx] if idx<len(g.players) and (active or g.players[idx].bot) else None
                inward=(0,-1) if upper else (0,1)
                visual=self.visual_positions.get(idx,center(spawn))
                crossing=occupant and abs(visual[0]-sx)<24 and (
                    visual[1]<mouth_y+22 if upper else visual[1]>mouth_y-22)
                opening=occupant and occupant.lives>0 and (occupant.entry>0 or occupant.pos==spawn
                    or (occupant.pos==g.arena.entries[idx] and occupant.wanted==inward) or crossing)
                if not morph:draw_station_gate(self.canvas,sx,mouth_y,upper,accent,opening)
                hud=station_hud(spawn,g.players[idx].score if active else 0)
                sx_text,sy=hud['x'],hud['y']
                if active:
                    p=g.players[idx]
                    arcade_digits(self.canvas,hud['label'],sx_text,sy,color,hud['scale'])
                    for life in range(p.lives): pg.draw.circle(self.canvas,color,(sx_text+3+life*9,sy+28),2)
                    if p.lives<=0:
                        remaining=g.continues.remaining(idx)
                        if remaining and not g.continues.pending(idx):
                            prompt=(f'CONTINUE {math.ceil(remaining-1e-10):02}' if int(self.animation_time*2)%2==0 else
                                    f'F{idx+3} START' if self.cabinet.settings['free_play'] or self.cabinet.credits else 'INSERT COIN')
                            self.text(prompt,sx_text,sy+(24 if upper else 21),color,self.micro)
                        elif not remaining:self.text('OUT',sx_text,sy+(24 if upper else 21),color,self.micro)
                else: self.text(f'F{idx+3} / START',sx_text,sy+1,color,self.small)
            top_bays=sorted(c[0] for c in g.arena.spawns if c[1]==0)
            status_center=round((center((top_bays[1],0))[0]+158+center((top_bays[2],0))[0]-28)/2)
            if g.rules['match_seconds']:
                timer=f'{int(g.time)//60}:{int(g.time)%60:02}'
                arcade_digits(self.canvas,timer,status_center-len(timer)*9,1,(250,250,235),3)
            else:self.text('LIFE SURVIVAL',status_center-self.micro.size('LIFE SURVIVAL')[0]//2,8,(250,250,235),self.micro)
            stage_label=f'S{g.stage} | {THEMES[g.arena.theme][0]}'
            self.text(stage_label,status_center-self.micro.size(stage_label)[0]//2,27,accent,self.micro)
            # Tunnel necks project beyond the board, as in the cabinet footage.
            for row in g.arena.portals:
                cy=center((0,row))[1]
                for side in (-1,1):
                    edge=OX if side<0 else OX+COLS*TILE
                    if not morph:draw_tunnel_neck(self.canvas,edge,cy,side,accent)
            self.canvas.set_clip(pg.Rect(OX-28,TOP-32,COLS*TILE+56,ROWS*TILE+64))
            self.canvas.set_clip(pg.Rect(OX,TOP,COLS*TILE,ROWS*TILE))
            for c,life in g.smoke.items():
                cx,cy=center(c)
                smoke_cloud(self.canvas,(cx,cy),self.animation_time,
                            radius=27,opacity=round(150*min(1,life)))
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
            self.motion_tracks['items']={key:value for key,value in self.motion_tracks['items'].items() if key in tracks.values()}
            for c,name in sorted(g.items.items()):
                key=tracks[c]
                target=center(c); old=self.visual_items.get(key,target)
                wrap=c[1] in g.arena.portals
                if distance(old,target)>TILE*3 and not (wrap and abs(target[0]-old[0])>COLS*TILE/2):old=target
                smooth=self.corridor_position('items',key,old,target,dt,g.tuning['item_step_seconds'],wrap)
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
                wrap=c[1] in g.arena.portals
                if distance(old,target)>TILE*3 and not (wrap and abs(target[0]-old[0])>COLS*TILE/2):old=target
                interval=g.tuning['ghost_step_seconds']
                if g.foe_modes[i]=='carried' and i in g.foe_carriers:
                    interval=g.player_interval(g.players[g.foe_carriers[i]])
                elif g.foe_modes[i]=='roaming':
                    if g.quake>0:interval*=g.tuning['quake_multiplier']
                    if any(distance(c,cloud)<=g.tuning['smoke_radius'] for cloud in g.smoke):interval*=g.tuning['smoke_multiplier']
                smooth=self.corridor_position('ghosts',i,old,target,dt,interval,wrap)
                if c[1] in g.arena.portals:
                    if smooth[0]<OX: smooth=(smooth[0]+COLS*TILE,smooth[1])
                    elif smooth[0]>OX+COLS*TILE: smooth=(smooth[0]-COLS*TILE,smooth[1])
                self.visual_foes[i]=smooth
                look=(1 if target[0]>old[0] else -1 if target[0]<old[0] else 0,
                      1 if target[1]>old[1] else -1 if target[1]<old[1] else 0)
                edible=any(g.active(p,'Crown') or g.active(p,'Titan') for p in g.players if p.lives>0)
                stunned=g.foe_stun>0 or (i<len(g.foe_zapped) and g.foe_zapped[i]>0)
                foe(self.canvas,tuple(map(round,smooth)),COLORS[(3,1,2,5)[i%4]],self.animation_time,stunned,look,edible and g.foe_modes[i]=='roaming',g.foe_modes[i] in ('eyes','entering'),pulse)
                if c[1] in g.arena.portals and (smooth[0]<OX+30 or smooth[0]>OX+COLS*TILE-30):
                    twin=smooth[0]+COLS*TILE if smooth[0]<OX+30 else smooth[0]-COLS*TILE
                    foe(self.canvas,(round(twin),round(smooth[1])),COLORS[(3,1,2,5)[i%4]],self.animation_time,
                        stunned,look,edible and g.foe_modes[i]=='roaming',g.foe_modes[i] in ('eyes','entering'),pulse)
            for p in g.players:
                if p.lives<=0: continue
                target=center(p.pos)
                old=self.visual_positions.get(p.idx,target)
                wrap=p.pos[1] in g.arena.portals and abs(target[0]-old[0])>COLS*TILE/2
                if not wrap and distance(old,target)>TILE*3:old=target
                interval=g.player_interval(p)
                spawn=g.arena.spawns[p.idx];entry=g.arena.entries[p.idx]
                outside=old[1]<center(entry)[1] if spawn[1]==0 else old[1]>center(entry)[1]
                if p.pos==spawn or p.pos==entry and outside:
                    # Gate centers are50px apart, unlike20px public lanes.
                    # Cover that visual distance in one movement interval.
                    interval*=TILE/abs(center(spawn)[1]-center(entry)[1])
                smooth=self.corridor_position('players',p.idx,old,target,dt,interval,p.pos[1] in g.arena.portals)
                if p.pos[1] in g.arena.portals:
                    if smooth[0]<OX: smooth=(smooth[0]+COLS*TILE,smooth[1])
                    elif smooth[0]>OX+COLS*TILE: smooth=(smooth[0]-COLS*TILE,smooth[1])
                self.visual_positions[p.idx]=smooth
                cx,cy=map(round,smooth); r=round(self.presentation.radius(p.idx)*pulse)
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
                spawn=g.arena.spawns[p.idx];sx=center(spawn)[0];upper=spawn[1]==0
                mouth=TOP+4 if upper else TOP+ROWS*TILE-4
                if abs(cx-sx)<32+r and (cy<TOP+40 if upper else cy>TOP+ROWS*TILE-40):
                    # The public-maze clip must not hide a body inside its own
                    # outside pocket. A separate bounded pass protects the HUD.
                    pocket=gate_geometry(sx,mouth,upper)['outer'].inflate(-3,-3)
                    self.canvas.set_clip(pocket)
                    muncher(self.canvas,(cx,cy),COLORS[p.idx],p.direction,self.animation_time+p.idx,r,
                            g.active(p,'Crown') or g.active(p,'Titan'),p.safe>0,150 if g.active(p,'Veil') else 255)
                    self.canvas.set_clip(pg.Rect(OX,TOP,COLS*TILE,ROWS*TILE))
                if p.pos[1] in g.arena.portals and (cx<=OX+r+9 or cx>=OX+COLS*TILE-r-9):
                    twin=cx+COLS*TILE if cx<OX+COLS*TILE/2 else cx-COLS*TILE
                    muncher(self.canvas,(twin,cy),COLORS[p.idx],p.direction,self.animation_time+p.idx,r,
                            g.active(p,'Crown') or g.active(p,'Titan'),p.safe>0,150 if g.active(p,'Veil') else 255)
                self.score_memory[p.idx]=p.score
                if p.stun>0:
                    self.text('* *',cx-12,cy-r-14,(255,255,230),self.small)
                if p.bot and p.pos in g.arena.lanes:
                    ai_y=cy+r+3
                    if ai_y+12>TOP+ROWS*TILE:ai_y=cy-r-14
                    ai_y=max(TOP,ai_y)
                    self.text('AI',max(OX,min(OX+COLS*TILE-16,cx-7)),ai_y,COLORS[p.idx],self.micro)
                if g.active(p,'Lure'): power_icon(self.canvas,(cx,cy-r-12),'Lure',self.animation_time,22)
            self.presentation.draw_effects(self.canvas,center,COLORS,
                pg.Rect(OX,TOP,COLS*TILE,ROWS*TILE),g.arena.portals)
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
            status=self.controller_status()
            color=(255,188,87) if status['missing'] or status['disconnected'] else (127,168,198)
            if status['simulated']:message=f"SIMULATED {status['effective']}"
            elif status['disconnected']:message='PAD DISCONNECTED'
            elif status['missing']:message=f"MISSING {status['missing']}/{status['expected']}"
            else:message=f"PADS {status['actual']}/{status['expected']}"
            if self.status_notice.startswith('CONTROLLED TEST'):message='TEST | '+message
            bottom=sorted(c[0] for c in g.arena.spawns if c[1]==ROWS-1)
            left=center((bottom[1],ROWS-1))[0]+164
            right=center((bottom[2],ROWS-1))[0]-39
            label=self.micro.render(message,True,color)
            if label.get_width()>right-left:
                label=pg.transform.smoothscale(label,(right-left,label.get_height()))
            self.canvas.blit(label,(left+(right-left-label.get_width())//2,H-12))
            if self.status_notice and not self.status_notice.startswith('CONTROLLED TEST'):
                notice=pg.Rect(180,H//2+70,920,34)
                pg.draw.rect(self.canvas,(8,15,28),notice,border_radius=6)
                self.text(self.status_notice,notice.x+12,notice.y+7,(255,200,110),self.small)
            if g.paused: self.overlay('PAUSED','Press P to continue')
            if g.over and self.name_entry is None:
                self.draw_results()
        if self.help:
            panel=pg.Surface((1160,650)); panel.fill((12,18,31)); self.canvas.blit(panel,(60,35))
            self.text('POWER FIELD GUIDE',105,55,(104,242,209),self.big)
            for i,(name,(code,desc)) in enumerate(ITEMS.items()):
                power_icon(self.canvas,(125,140+i*43),name,self.animation_time,42)
                self.text(f'{DISPLAY_NAMES[name]}: {self.power_description(name)}',165,130+i*43)
            self.text('F1 closes. Guide pauses play. Titans bite rivals; equal powers are safe.',105,617)
            rules=self.match.rules if self.match else self.cabinet.settings
            mode=f"Time {rules['match_seconds']}s" if rules['match_seconds'] else 'No time limit'
            self.text(f"Lives {rules['starting_lives']} | {mode} | Dot clearance advances the selected map policy.",105,653)
        if self.operator_open:self.draw_operator()
        if self.name_entry is not None:self.draw_name_entry()
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
        if self.phase not in (Phase.PLAYING,Phase.CONTINUE):
            self.fixed_accumulator=0.; return []
        self.fixed_accumulator+=max(0,dt)
        sounds=[]
        while self.fixed_accumulator+1e-10>=1/60:
            steer_demo(self.match,only_bots=not self.demo)
            for p in self.match.players:
                p.locate_remaining=self.match.countdown(p.locate_remaining,1/60)
            sounds.extend(self.match.update(1/60))
            self.fixed_accumulator-=1/60
            if self.match.over:
                self.fixed_accumulator=0.
                ended=self.match.ledger.events[-1]
                if ended['event']=='match_end' and ended['context'].get('continue_timeout'):
                    self.save_result()
                    self.begin_name_entry()
                break
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
        self.text('ENTER replay preset | F3-F10 new station | N initials | ESC lobby',300,575,font=self.small)
        if self.status_notice:self.text(self.status_notice,250,610,(255,200,110),self.small)

    def run(self,frames=0):
        n=0
        while self.running:
            dt=min(.25,self.clock.tick(60)/1000)
            self.events()
            if self.match is None:
                self.idle_time+=dt
                if self.idle_time>=12 and self.cabinet.settings['attract_sound'] and not self.muted and not (self.operator_open or self.scores_open or self.help):
                    page=int((self.idle_time-12)//4)
                    if page!=getattr(self,'attract_page',None):
                        self.attract_page=page
                        if 'power' in self.sounds and pg.mixer.get_init():
                            try:pg.mixer.Channel(1).play(self.sounds['power'])
                            except pg.error:pass
            if self.match:
                if not self.demo: self.inputs()
                sounds=self.advance(dt)
                self.audio.consume(self.match.ledger,self.muted)
                if self.match.over:self.save_result(False)
            elif self.pending_results:self.save_result(False)
            self.publish_clock+=dt
            publish_due=self.spectator_path and self.publish_clock>=.1
            self.draw(dt);n+=1
            if publish_due:
                self.publish_clock=0.
                try:
                    from pathlib import Path
                    feed_path=Path(self.spectator_path);feed_path.parent.mkdir(parents=True,exist_ok=True)
                    frame=feed_path.with_suffix('.frame.jpg');temporary=frame.with_name(frame.stem+'.tmp.jpg')
                    pg.image.save(self.canvas,str(temporary));temporary.replace(frame)
                    atomic_json(feed_path,spectator_view(self.match,self.phase.value,
                        THEMES[self.match.arena.theme][0] if self.match else ''))
                except (OSError,pg.error):self.status_notice='Spectator feed could not be saved.'
            if frames and n>=frames: break
        pg.quit()

def steer_demo(g,only_bots=False):
    """Original deterministic navigation for bots and the reproducible demo."""
    for p in g.players:
        if only_bots and not p.bot:continue
        if p.lives<=0: continue
        directions=DIRS[p.idx%4:]+DIRS[:p.idx%4]
        p.wanted=choose_direction(g,p,directions)

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
    parser.add_argument('--palette',type=int,choices=range(5),help='Independent wall color; palette4 is luminous blue. F12 cycles all five.')
    parser.add_argument('--spectator-state',help='Publish an optional local spectator feed JSON file.')
    parser.add_argument('--data-dir',help='Directory for local operator settings, credits and high scores.')
    parser.add_argument('--arena',type=int,choices=range(4),default=3,help='Starting visual profile; four independently reconstructed observed layouts.')
    parser.add_argument('--tuning',help='JSON overrides for explicitly approximate power timings, speeds, ranges and item cadence.')
    parser.add_argument('--untimed',action='store_true',help='Play until all humans lose their lives; optional inferred DX-style survival mode.')
    parser.add_argument('--continue-seconds',type=float,default=10.,help='Continue window (0 disables, maximum60);10s is a footage-derived estimate.')
    parser.add_argument('--continue-delay',type=float,default=1.,help='Custom final-death reveal delay,0..5seconds.')
    args=parser.parse_args()
    if not math.isfinite(args.locator_seconds) or not 0<args.locator_seconds<=10: parser.error('Locator duration must be in (0,10].')
    try:ContinueOffers(args.continue_seconds,args.continue_delay)
    except ValueError as error:parser.error(str(error))
    app=App(simulate_controllers=args.simulate_controllers,cabinet=CabinetStore(args.data_dir))
    app.untimed=args.untimed
    app.continue_seconds=args.continue_seconds;app.continue_delay=args.continue_delay
    if args.tuning:
        try:app.tuning=load_tuning(args.tuning)
        except (OSError,ValueError,TypeError) as error:parser.error(str(error))
    app.spectator_path=args.spectator_state
    app.theme=args.arena
    app.seed=args.seed; app.progression=args.progression; app.locator_seconds=args.locator_seconds
    app.palette_override=args.palette
    app.demo=args.demo
    if args.demo and not args.players: args.players=8
    if args.players: app.count=args.players; app.start()
    app.run(args.frames)
    if args.event_log and app.match: app.match.ledger.write(args.event_log)


