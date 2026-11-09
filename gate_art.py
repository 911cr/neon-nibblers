"""Original luminous station pockets and striped thresholds, drawn as vectors."""
from functools import lru_cache
import math
import pygame as pg
from arcade_art import wall_highlight,neon_sprite,NEON_SCALE,NEON_STROKE,NEON_CORE

GATE_HATCH=(228,238,82)
GATE_LIP=(250,255,146)  # Continuous yellow upper edge seen in the reference photo.
GATE_WIDTH=64
GATE_DEPTH=48


@lru_cache(maxsize=24)
def _tunnel_sprite(accent):
    scale=NEON_SCALE
    ink=pg.Surface((64*scale,112*scale),pg.SRCALPHA)
    # Left-hand frame cores are 1/4px inside the board. Replace its old
    # closed cap with two continuous corners, rather than dangling rails.
    for x,top,bottom in ((1,-28,27),(4,-24,23)):
        for y,end in ((top,-56),(bottom,56)):
            points=[(-36,y),(x,y),(x,end)]
            points=[(round((px+36+.5)*scale),round((py+56+.5)*scale)) for px,py in points]
            pg.draw.lines(ink,accent,False,points,round(NEON_STROKE*scale))
            pg.draw.lines(ink,wall_highlight(accent),False,points,round(NEON_CORE*scale))
    return neon_sprite(ink,(64,112))


def draw_tunnel_neck(target,edge,cy,side,accent):
    """Replace only the portal seam, joining necks to the existing frame."""
    old_clip=target.get_clip()
    target.set_clip(pg.Rect(edge-28 if side<0 else edge-14,cy-40,42,80).clip(old_clip))
    target.fill((0,0,4),target.get_clip())
    sprite=_tunnel_sprite(tuple(accent))
    if side>0:sprite=pg.transform.flip(sprite,True,False)
    target.blit(sprite,(edge-36 if side<0 else edge-28,cy-56),
                special_flags=pg.BLEND_PREMULTIPLIED)
    target.set_clip(old_clip)


def gate_geometry(sx,mouth_y,upper):
    return {'outer':pg.Rect(sx-32,mouth_y-48 if upper else mouth_y,64,48),
            'hatch':pg.Rect(sx-24,mouth_y-5,48,10),
            'clear':pg.Rect(sx-44,mouth_y-56 if upper else mouth_y-8,88,64)}


def _u_points(half,depth,radius,lip):
    points=[(-44,lip),(-half,lip),(-half,depth-radius)]
    for angle in range(180,89,-10):
        radians=math.radians(angle)
        points.append((-half+radius+math.cos(radians)*radius,depth-radius+math.sin(radians)*radius))
    points.append((half-radius,depth))
    for angle in range(90,-1,-10):
        radians=math.radians(angle)
        points.append((half-radius+math.cos(radians)*radius,depth-radius+math.sin(radians)*radius))
    points.extend(((half,lip),(44,lip)))
    return points


@lru_cache(maxsize=40)
def _gate_sprite(accent,upper,opening):
    scale=NEON_SCALE;size=(96,80);anchor=(48,12)
    ink=pg.Surface((size[0]*scale,size[1]*scale),pg.SRCALPHA)
    high=wall_highlight(accent)
    for half,depth,radius,lip in ((32,48,10,3),(26,42,6,-2)):
        points=[(round((x+anchor[0])*scale),round((y+anchor[1])*scale))
                for x,y in _u_points(half,depth,radius,lip)]
        pg.draw.lines(ink,accent,False,points,round(NEON_STROKE*scale))
        pg.draw.lines(ink,high,False,points,round(NEON_CORE*scale))
    sprite=neon_sprite(ink,size)
    if upper:sprite=pg.transform.flip(sprite,False,True)
    if not opening:
        band=pg.Surface((48,10));band.fill(GATE_HATCH)
        for x in range(-6,58,8):pg.draw.line(band,(17,23,9),(x,10),(x+10,0),3)
        # Keep the bright lip continuous: the dark cuts begin beneath it.
        # The static reference does not establish a persistent open-gate line.
        pg.draw.line(band,GATE_LIP,(0,0),(47,0),1)
        band_y=(sprite.get_height()-1-anchor[1] if upper else anchor[1])-5
        sprite.blit(band,(anchor[0]-24,band_y))
    return sprite


def draw_station_gate(target,sx,mouth_y,upper,accent,opening):
    geometry=gate_geometry(sx,mouth_y,upper)
    pg.draw.rect(target,(0,0,4),geometry['clear'])
    sprite=_gate_sprite(tuple(accent),bool(upper),bool(opening))
    anchor_y=sprite.get_height()-1-12 if upper else 12
    target.blit(sprite,(sx-48,mouth_y-anchor_y),special_flags=pg.BLEND_PREMULTIPLIED)
    return geometry


@lru_cache(maxsize=20)
def _house_sprite(size,accent):
    width,height=size;pad=14;scale=NEON_SCALE
    output_size=(width+pad*2,height+pad*2)
    ink=pg.Surface((output_size[0]*scale,output_size[1]*scale),pg.SRCALPHA)
    outer=pg.Rect(pad,pad,width,height)
    core_inset=round((NEON_STROKE-NEON_CORE)*scale/2)
    for rect,radius in ((outer,4),(outer.inflate(-20,-20),3)):
        scaled=pg.Rect(rect.x*scale,rect.y*scale,rect.w*scale,rect.h*scale)
        pg.draw.rect(ink,accent,scaled,round(NEON_STROKE*scale),border_radius=radius*scale)
        pg.draw.rect(ink,wall_highlight(accent),scaled.inflate(-2*core_inset,-2*core_inset),
                     round(NEON_CORE*scale),border_radius=max(0,radius*scale-core_inset))
    return neon_sprite(ink,output_size)


def draw_house(target,rect,accent,door_x):
    pg.draw.rect(target,(0,0,4),rect.inflate(54,54))
    target.blit(_house_sprite(rect.size,tuple(accent)),(rect.x-14,rect.y-14),special_flags=pg.BLEND_PREMULTIPLIED)
    pg.draw.rect(target,(0,0,4),(door_x-20,rect.top-14,40,33))
    pg.draw.line(target,(224,211,255),(door_x-19,rect.top),(door_x+19,rect.top),2)
