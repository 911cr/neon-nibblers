"""Original luminous station pockets and striped thresholds, drawn as vectors."""
from functools import lru_cache
import math
import pygame as pg
from arcade_art import wall_highlight

GATE_HATCH=(228,238,82)
GATE_WIDTH=64
GATE_DEPTH=48


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
    scale=3;size=(96,80);anchor=(48,12)
    ink=pg.Surface((size[0]*scale,size[1]*scale),pg.SRCALPHA)
    high=wall_highlight(accent)
    for half,depth,radius,lip in ((32,48,10,3),(26,42,6,-2)):
        points=[(round((x+anchor[0])*scale),round((y+anchor[1])*scale))
                for x,y in _u_points(half,depth,radius,lip)]
        pg.draw.lines(ink,accent,False,points,3*scale)
        pg.draw.lines(ink,high,False,points,scale)
    ink=pg.transform.smoothscale(ink,size)
    sprite=pg.Surface(size,pg.SRCALPHA)
    for radius,mult in ((6,160),(3,210)):
        halo=pg.transform.gaussian_blur(ink,radius)
        halo.fill((mult,mult,mult,255),special_flags=pg.BLEND_RGBA_MULT)
        sprite.blit(halo,(0,0),special_flags=pg.BLEND_RGBA_ADD)
    sprite.blit(ink,(0,0))
    if upper:sprite=pg.transform.flip(sprite,False,True)
    if not opening:
        band=pg.Surface((48,10));band.fill(GATE_HATCH)
        for x in range(-6,58,8):pg.draw.line(band,(17,23,9),(x,10),(x+10,0),3)
        band_y=(sprite.get_height()-1-anchor[1] if upper else anchor[1])-5
        sprite.blit(band,(anchor[0]-24,band_y))
    return sprite


def draw_station_gate(target,sx,mouth_y,upper,accent,opening):
    geometry=gate_geometry(sx,mouth_y,upper)
    pg.draw.rect(target,(0,0,4),geometry['clear'])
    sprite=_gate_sprite(tuple(accent),bool(upper),bool(opening))
    anchor_y=sprite.get_height()-1-12 if upper else 12
    target.blit(sprite,(sx-48,mouth_y-anchor_y))
    return geometry


@lru_cache(maxsize=20)
def _house_sprite(size,accent):
    width,height=size;pad=14
    ink=pg.Surface((width+pad*2,height+pad*2),pg.SRCALPHA)
    outer=pg.Rect(pad,pad,width,height)
    for rect,radius in ((outer,4),(outer.inflate(-20,-20),3)):
        pg.draw.rect(ink,accent,rect,3,border_radius=radius)
        pg.draw.rect(ink,wall_highlight(accent),rect.inflate(-2,-2),1,border_radius=radius)
    result=pg.Surface(ink.get_size(),pg.SRCALPHA)
    for blur,mult in ((6,160),(3,210)):
        halo=pg.transform.gaussian_blur(ink,blur)
        halo.fill((mult,mult,mult,255),special_flags=pg.BLEND_RGBA_MULT)
        result.blit(halo,(0,0),special_flags=pg.BLEND_RGBA_ADD)
    result.blit(ink,(0,0));return result


def draw_house(target,rect,accent,door_x):
    pg.draw.rect(target,(0,0,4),rect.inflate(54,54))
    target.blit(_house_sprite(rect.size,tuple(accent)),(rect.x-14,rect.y-14))
    pg.draw.rect(target,(0,0,4),(door_x-20,rect.top-14,40,33))
    pg.draw.line(target,(224,211,255),(door_x-19,rect.top),(door_x+19,rect.top),2)
