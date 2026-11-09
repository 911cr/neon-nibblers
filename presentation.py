"""Original lifecycle feedback. Timings are configurable approximations, not DX measurements.

This module reads simulation state/events and never changes collision, powers,
scores, safety or respawn timing. Call update once per presented frame with the
effective world delta (zero during pause, guide and results).
"""
from dataclasses import dataclass
import math
import pygame as pg


@dataclass
class RadiusTween:
    start: float
    target: int
    began: float


@dataclass
class Burst:
    player_id: int
    position: tuple
    began: float


class LifecyclePresentation:
    def __init__(self, growth_seconds=.25, death_seconds=.45, arrival_seconds=.45):
        for value in (growth_seconds, death_seconds, arrival_seconds):
            if not math.isfinite(value) or value <= 0:
                raise ValueError('Animation durations must be positive and finite')
        self.growth_seconds=growth_seconds
        self.death_seconds=death_seconds
        self.arrival_seconds=arrival_seconds
        self.reset()

    def reset(self):
        self.ledger=None
        self.cursor=0
        self.time=0.
        self.radii={}
        self.deaths=[]
        self.arrivals=[]

    def _radius_float(self,idx):
        tween=self.radii.get(idx)
        if tween is None:return 17.
        progress=max(0.,min(1.,(self.time-tween.began)/self.growth_seconds))
        eased=progress*progress*(3-2*progress)
        return tween.start+(tween.target-tween.start)*eased

    def radius(self,idx):
        """At most twenty integer sizes: bounded procedural-art cache keys."""
        return max(17,min(36,round(self._radius_float(idx))))

    def update(self,match,dt):
        if not math.isfinite(dt) or dt < 0:raise ValueError('Animation dt must be finite and non-negative')
        if self.ledger is not match.ledger or self.cursor>len(match.ledger.events):
            self.reset()
            self.ledger=match.ledger
        for event in match.ledger.events[self.cursor:]:
            kind=event['event']
            if kind=='stage_start':
                self.deaths.clear();self.arrivals.clear();self.radii.clear()
            elif kind=='player_hurt' and event['player_id'] is not None:
                idx=event['player_id']-1
                position=event['context'].get('position')
                if position is not None:
                    self.deaths.append(Burst(idx,tuple(position),self.time))
                if event['context'].get('lives',0)>0 and 0<=idx<len(match.players):
                    self.arrivals.append(Burst(idx,tuple(match.arena.spawns[idx]),self.time))
            elif kind=='station_join' and event['player_id'] is not None:
                idx=event['player_id']-1
                self.radii.pop(idx,None)
                if 0<=idx<len(match.players):
                    self.arrivals.append(Burst(idx,tuple(match.arena.spawns[idx]),self.time))
        self.cursor=len(match.ledger.events)
        for player in match.players:
            if not getattr(player,'joined',True) and not getattr(player,'bot',False):continue
            desired=36 if match.active(player,'Titan') else 17
            tween=self.radii.get(player.idx)
            if tween is None:
                self.radii[player.idx]=RadiusTween(17.,desired,self.time)
            elif tween.target!=desired:
                self.radii[player.idx]=RadiusTween(self._radius_float(player.idx),desired,self.time)
        self.time+=dt
        self.deaths=[b for b in self.deaths if self.time-b.began<self.death_seconds-1e-10]
        self.arrivals=[b for b in self.arrivals if self.time-b.began<self.arrival_seconds-1e-10]

    def draw_effects(self,surface,center_fn,colors,playfield_rect,portals):
        """Draw bounded original shards and bay pulses; restore caller clipping.

        Deaths are clipped to the maze and duplicated periodically only at a
        declared tunnel. Arrival pulses are clipped to their own narrow bay,
        keeping neighboring station scores and the footer untouched.
        """
        board=pg.Rect(playfield_rect)
        prior=surface.get_clip()
        surface.set_clip(board.clip(prior))
        for burst in self.deaths:
            progress=max(0.,min(1.,(self.time-burst.began)/self.death_seconds))
            color=colors[burst.player_id]
            tile=pg.Surface((96,96),pg.SRCALPHA)
            alpha=round(230*(1-progress))
            # A dissolving core and outward chips are independently drawn,
            # rather than a copied commercial death sprite sequence.
            core=max(1,round(17*(1-progress)**2))
            pg.draw.circle(tile,(*color,round(alpha*.65)),(48,48),core)
            for n in range(12):
                angle=n*math.tau/12+burst.player_id*.23
                distance=7+31*progress
                x=48+math.cos(angle)*distance;y=48+math.sin(angle)*distance
                radius=max(1,round(3*(1-progress)))
                pg.draw.polygon(tile,(*color,alpha),
                                [(x-radius,y),(x,y-radius),(x+radius,y),(x,y+radius)])
            x,y=center_fn(burst.position)
            centers=[(x,y)]
            if burst.position[1] in portals:
                if x-board.left<48:centers.append((x+board.width,y))
                if board.right-x<48:centers.append((x-board.width,y))
            for point in centers:surface.blit(tile,tile.get_rect(center=point))
        for burst in self.arrivals:
            progress=max(0.,min(1.,(self.time-burst.began)/self.arrival_seconds))
            x,_=center_fn(burst.position)
            upper=burst.position[1]==0
            y=board.top-5 if upper else board.bottom+5
            pocket=pg.Rect(x-28,board.top-32 if upper else board.bottom-12,56,44)
            surface.set_clip(pocket.clip(prior))
            tile=pg.Surface((64,64),pg.SRCALPHA)
            radius=round(24-7*progress)
            alpha=round(200*math.sin(math.pi*(.15+.85*progress)))
            pg.draw.circle(tile,(*colors[burst.player_id],max(0,alpha)),(32,32),radius,2)
            surface.blit(tile,tile.get_rect(center=(x,y)))
        surface.set_clip(prior)
