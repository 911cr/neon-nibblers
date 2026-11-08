"""Original procedural arcade art. No commercial sprites, logos or traced maps."""
import math
from functools import lru_cache
import pygame as pg

def maze_background(floor, cols, rows, tile, accent):
    size=(cols*tile,rows*tile)
    raw=pg.Surface(size,pg.SRCALPHA)
    # Carve a constant-width tube around the SAME graph used by movement.
    # A free-looking gap can no longer disagree with the collision map.
    raw.fill((255,255,255))
    radius=32
    raw.set_clip(pg.Rect(6,6,size[0]-12,size[1]-12))
    for x,y in floor:
        cx,cy=x*tile+tile//2,y*tile+tile//2
        pg.draw.circle(raw,(0,0,0,0),(cx,cy),radius)
        for dx,dy in ((1,0),(0,1)):
            if (x+dx,y+dy) in floor:
                if dx: rect=(cx,cy-radius,tile,radius*2)
                else: rect=(cx-radius,cy,radius*2,tile)
                pg.draw.rect(raw,(0,0,0,0),rect)
    raw.set_clip(None)
    # The main board stays framed despite wider corridors. Carve only the real
    # tunnel mouths and player thresholds through that frame.
    for x,y in floor:
        cx,cy=x*tile+tile//2,y*tile+tile//2
        if x in (0,cols-1): pg.draw.rect(raw,(0,0,0,0),(x*tile,cy-26,tile,52))
        if y in (0,rows-1): pg.draw.rect(raw,(0,0,0,0),(cx-20,y*tile,40,tile))
    mask=pg.mask.from_surface(raw)
    # Round exposed wall corners without changing the corridor center-lines.
    offsets=[(x,y) for x in range(-5,6) for y in range(-5,6) if x*x+y*y<=25]
    core=mask.copy()
    for offset in ((5,0),(-5,0),(0,5),(0,-5),(4,3),(-4,3),(4,-3),(-4,-3)):
        shifted=pg.mask.Mask(size); shifted.draw(mask,offset)
        core=core.overlap_mask(shifted,(0,0))
    rounded=pg.mask.Mask(size)
    for offset in offsets: rounded.draw(core,offset)
    # Retain the thin outer frame; openings remain carved at tunnels and bays.
    for y in range(rows):
        for x in range(cols):
            if x in (0,cols-1) or y in (0,rows-1):
                for yy in range(y*tile,(y+1)*tile):
                    for xx in range(x*tile,(x+1)*tile):
                        if mask.get_at((xx,yy)): rounded.set_at((xx,yy))
    mask=rounded
    inner=mask.copy()
    for offset in ((2,0),(-2,0),(0,2),(0,-2)):
        shifted=pg.mask.Mask(size); shifted.draw(mask,offset)
        inner=inner.overlap_mask(shifted,(0,0))
    edge=mask.copy(); edge.erase(inner,(0,0))
    result=pg.Surface(size); result.fill((0,0,4))
    glow=edge.to_surface(setcolor=tuple(int(c*.16) for c in accent),unsetcolor=(0,0,0,0))
    for offset in ((-3,0),(3,0),(0,-3),(0,3),(-2,-2),(2,2)):
        result.blit(glow,offset,special_flags=pg.BLEND_RGB_ADD)
    result.blit(mask.to_surface(setcolor=(1,2,8),unsetcolor=(0,0,0,0)),(0,0))
    result.blit(edge.to_surface(setcolor=accent,unsetcolor=(0,0,0,0)),(0,0))
    return result

@lru_cache(maxsize=64)
def sphere(color,radius):
    """Newly computed sphere lighting, supersampled for smooth silhouettes."""
    scale=3; r=radius*scale; mid=(radius+9)*scale
    s=pg.Surface((mid*2,mid*2),pg.SRCALPHA)
    for yy in range(-r,r+1):
        for xx in range(-r,r+1):
            nx,ny=xx/r,yy/r
            square=nx*nx+ny*ny
            if square>1: continue
            nz=math.sqrt(1-square)
            lit=.25+.8*max(0,-.36*nx-.48*ny+.8*nz)
            gloss=max(0,-.28*nx-.4*ny+.87*nz)**35*.75
            rgb=tuple(min(255,int(v*lit+255*gloss)) for v in color)
            s.set_at((mid+xx,mid+yy),(*rgb,255))
    return s

def muncher(target, pos, color, direction, time, radius=15, powered=False, safe=False,opacity=255):
    scale=3; r=radius*scale; mid=(radius+9)*scale
    s=sphere(tuple(color),radius).copy()
    if powered or safe:
        pg.draw.circle(s,(*color,55),(mid,mid),r+5*scale,2*scale)
    angle=.035+.77*(.5+.5*math.sin(time*22))
    mouth=[(mid,mid),(mid+int(r*1.3),mid-int(math.tan(angle)*r*1.3)),
           (mid+int(r*1.3),mid+int(math.tan(angle)*r*1.3))]
    pg.draw.polygon(s,(0,0,0,0),mouth)
    pg.draw.ellipse(s,(12,14,24),(mid-r*.04,mid-r*.64,r*.14,r*.26))
    angle_deg=math.degrees(math.atan2(-direction[1],direction[0])) if direction!=(0,0) else 0
    s=pg.transform.rotate(s,angle_deg)
    s=pg.transform.smoothscale(s,(s.get_width()//scale,s.get_height()//scale))
    if opacity<255: s.set_alpha(opacity)
    target.blit(s,s.get_rect(center=pos))

def foe(target,pos,color,time,stunned=False,direction=(0,0),edible=False,eyes_only=False):
    x,y=pos; scale=3; mid=24*scale
    s=pg.Surface((48*scale,48*scale),pg.SRCALPHA)
    c=color
    if edible: c=(53,72,236)
    shape=pg.Surface(s.get_size(),pg.SRCALPHA)
    pg.draw.circle(shape,(255,255,255),(mid,21*scale),15*scale)
    pg.draw.rect(shape,(255,255,255),(9*scale,21*scale,30*scale,13*scale))
    for i in range(4):
        xx=(12+i*8)*scale
        pg.draw.circle(shape,(255,255,255),(xx,int((33+math.sin(time*8+i))*scale)),4*scale)
    mask=pg.mask.from_surface(shape)
    # Light the domed body across its width, with a soft upper-left highlight.
    for xx in range(9*scale,40*scale):
        nx=(xx-mid)/(16*scale)
        intensity=.5+.5*math.sqrt(max(0,1-nx*nx))-.15*nx
        cc=tuple(min(255,int(v*intensity)) for v in c)
        pg.draw.line(s,cc,(xx,6*scale),(xx,39*scale))
    s.blit(mask.to_surface(setcolor=(255,255,255,255),unsetcolor=(0,0,0,0)),(0,0),special_flags=pg.BLEND_RGBA_MULT)
    if eyes_only: s.fill((0,0,0,0))
    for ex in (18,30):
        pg.draw.ellipse(s,(248,251,255),((ex-5)*scale,17*scale,10*scale,13*scale))
        dx=direction[0]*2; dy=direction[1]*2
        pg.draw.ellipse(s,(35,58,146),((ex-2+dx)*scale,(22+dy)*scale,5*scale,7*scale))
    s=pg.transform.smoothscale(s,(58,58))
    target.blit(s,(round(x)-29,round(y)-29))

_DIGITS=(
 '01110' '11011' '11011' '11011' '11011' '11011' '01110',
 '00110' '01110' '00110' '00110' '00110' '00110' '11111',
 '01110' '11011' '00011' '00110' '01100' '11000' '11111',
 '11110' '00011' '00011' '01110' '00011' '00011' '11110',
 '00011' '00111' '01111' '11011' '11111' '00011' '00011',
 '11111' '11000' '11000' '11110' '00011' '00011' '11110',
 '01110' '11000' '11000' '11110' '11011' '11011' '01110',
 '11111' '00011' '00110' '00110' '01100' '01100' '01100',
 '01110' '11011' '11011' '01110' '11011' '11011' '01110',
 '01110' '11011' '11011' '01111' '00011' '00011' '01110')

def arcade_digits(target,text,x,y,color,scale=3):
    for ch in str(text):
        if ch.isdigit():
            pattern=_DIGITS[int(ch)]
            for i,bit in enumerate(pattern):
                if bit=='1': pg.draw.rect(target,color,(x+(i%5)*scale,y+(i//5)*scale,scale,scale))
        elif ch==':':
            for row in (2,5): pg.draw.rect(target,color,(x+scale*2,y+row*scale,scale,scale))
        x+=6*scale

@lru_cache(maxsize=1)
def dot_sprite():
    s=pg.Surface((28,28),pg.SRCALPHA)
    pg.draw.circle(s,(135,145,166,35),(14,14),12)
    pg.draw.circle(s,(249,248,235),(14,14),8)
    return pg.transform.smoothscale(s,(7,7))

def power_icon(target,pos,name,time,size=32):
    x,y=pos; y+=round(math.sin(time*3+x)*2)
    s=pg.Surface((42,42),pg.SRCALPHA); c=(255,240,190)
    if name in ('Crown','Titan'):
        color=(255,222,76) if name=='Crown' else (114,255,98)
        pg.draw.circle(s,(*color,40),(21,21),16)
        orb=pg.transform.smoothscale(sphere(tuple(color),11),(40,40))
        s.blit(orb,(1,1))
    elif name=='Rush':
        # Independently drawn handled coffee mug from the observed object type.
        pg.draw.ellipse(s,(145,156,181),(27,14,13,20),5)
        pg.draw.rect(s,(167,180,204),(9,11,22,24),border_radius=5)
        pg.draw.rect(s,(215,222,232),(10,12,6,20),border_radius=3)
        pg.draw.ellipse(s,(236,239,245),(9,7,22,10))
        pg.draw.ellipse(s,(103,65,32),(12,9,16,6))
        pg.draw.polygon(s,(255,205,75),[(23,16),(17,24),(22,24),(19,31),(27,21),(22,21)])
    elif name=='Mist':
        pg.draw.circle(s,(129,124,106),(21,25),12)
        pg.draw.circle(s,(176,171,146),(18,21),8)
        pg.draw.arc(s,(98,96,82),(10,14,23,23),.7,2.6,2)
        pg.draw.line(s,(112,108,91),(12,29),(27,16),2)
        pg.draw.line(s,(112,108,91),(19,36),(31,24),2)
        pg.draw.circle(s,(209,208,180),(16,19),3)
        pg.draw.lines(s,(210,180,100),False,[(23,14),(26,9),(23,5)],2)
        pg.draw.circle(s,(255,200,85),(23,5),3)
    elif name=='Veil':
        pg.draw.circle(s,(239,244,255),(21,18),13)
        pg.draw.polygon(s,(239,244,255),[(8,18),(34,18),(36,35),(28,31),(23,36),(17,32),(9,36)])
        pg.draw.ellipse(s,(41,51,89),(13,16,6,9)); pg.draw.ellipse(s,(41,51,89),(24,16,6,9))
    elif name=='Slick':
        pg.draw.polygon(s,(255,218,61),[(22,11),(23,24),(36,32),(27,32),(20,27),(10,35),(5,33),(16,23)])
        pg.draw.polygon(s,(255,245,157),[(22,11),(18,22),(19,28),(23,24)])
        pg.draw.polygon(s,(230,174,36),[(23,24),(31,29),(36,32),(27,32)])
        pg.draw.line(s,(130,103,40),(22,11),(24,7),3)
    elif name=='Spark':
        pg.draw.polygon(s,(123,230,255),[(23,3),(9,24),(20,23),(16,39),(34,16),(23,18)])
    elif name=='Flare':
        pg.draw.polygon(s,(255,91,27),[(10,27),(5,18),(9,9),(12,17),(16,4),(20,16),(17,24)])
        pg.draw.polygon(s,(255,222,73),[(11,25),(9,18),(14,12),(15,20),(17,18),(16,25)])
        pg.draw.polygon(s,(243,64,54),[(28,18),(33,21),(29,28),(20,33),(6,35),(15,30),(22,25)])
        pg.draw.line(s,(255,159,110),(27,22),(20,28),3)
        pg.draw.lines(s,(99,215,73),False,[(28,18),(28,13),(33,12)],3)
    elif name=='Quake':
        pg.draw.rect(s,(141,35,39),(10,19,24,19),border_radius=2)
        pg.draw.rect(s,(225,57,54),(9,17,23,19),border_radius=2)
        pg.draw.rect(s,(252,115,92),(10,18,5,17))
        pg.draw.rect(s,(155,164,178),(19,6,5,13))
        pg.draw.rect(s,(196,204,213),(10,4,24,6),border_radius=3)
        pg.draw.lines(s,(255,234,211),False,[(17,22),(24,22),(19,26),(25,31),(18,31)],2)
    elif name=='Heart':
        # Original block lettering, no commercial logo asset.
        white=(249,250,255)
        pg.draw.polygon(s,white,[(6,12),(14,7),(19,7),(19,31),(23,31),(23,36),(8,36),(8,31),(13,31),(13,15),(6,18)])
        label=pg.font.Font(None,19).render('UP',True,white)
        s.blit(label,(20,9))
    else:
        pg.draw.arc(s,(40,121,194),(6,7,29,29),math.pi/2,math.pi*1.5,9)
        pg.draw.rect(s,(40,121,194),(20,7,12,9))
        pg.draw.rect(s,(40,121,194),(20,27,12,9))
        pg.draw.rect(s,(224,230,239),(28,7,6,9))
        pg.draw.rect(s,(224,230,239),(28,27,6,9))
    if size!=42: s=pg.transform.smoothscale(s,(size,size))
    target.blit(s,(x-size//2,y-size//2))
