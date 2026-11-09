"""Original shrink/swap/expand approximation of observed DX maze transitions.

Only broad compression and temporary actor enlargement are observed in footage.
The 0.90 scale, 1.35 actor multiplier and short blend window are authored values,
not reverse-engineered timings or a claim of exact commercial wall trajectories.
Call with already rendered backgrounds; no morphology or asset generation runs
per frame. Draw actors and HUD afterwards so they remain independent of walls.
"""
import math
import pygame as pg

MIN_WALL_SCALE = .90
MAX_ACTOR_SCALE = 1.35
BLEND_START = .44
BLEND_END = .56


def _progress(progress):
    value=float(progress)
    if not math.isfinite(value):
        raise ValueError('Transition progress must be finite')
    return max(0.0,min(1.0,value))


def wall_scale(progress):
    pulse=math.sin(math.pi*_progress(progress))**2
    return 1-(1-MIN_WALL_SCALE)*pulse


def actor_scale(progress):
    """Presentation-only multiplier; never change collision radii or powers."""
    pulse=math.sin(math.pi*_progress(progress))**2
    return 1+(MAX_ACTOR_SCALE-1)*pulse


def render_background(old,new,progress):
    """Return a full-size opaque background; never mutate supplied surfaces.

    The old maze contracts, swaps over a short continuous overlap, then the new
    maze expands. The intentional 12%-duration overlap avoids an abrupt swap;
    it is not an inferred component-by-component topology morph. No dark fade
    or blank midpoint is introduced. Root controls duration and gameplay state.
    """
    if old.get_size()!=new.get_size():
        raise ValueError('Transition backgrounds must have matching dimensions')
    p=_progress(progress)
    if p==0:return old.copy()
    if p==1:return new.copy()
    size=old.get_size()
    factor=wall_scale(p)
    scaled_size=tuple(max(1,round(v*factor)) for v in size)
    if p<=BLEND_START:
        walls=pg.transform.smoothscale(old,scaled_size)
    elif p>=BLEND_END:
        walls=pg.transform.smoothscale(new,scaled_size)
    else:
        weight=(p-BLEND_START)/(BLEND_END-BLEND_START)
        weight=weight*weight*(3-2*weight)
        walls=pg.transform.smoothscale(old,scaled_size)
        incoming=pg.transform.smoothscale(new,scaled_size)
        incoming.set_alpha(round(255*weight))
        walls.blit(incoming,(0,0))
    result=pg.Surface(size)
    result.fill((0,0,4))
    result.blit(walls,walls.get_rect(center=result.get_rect().center))
    return result
