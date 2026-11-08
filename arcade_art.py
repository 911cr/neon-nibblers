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
    radius=26
    for x,y in floor:
        cx,cy=x*tile+tile//2,y*tile+tile//2
        pg.draw.circle(raw,(0,0,0,0),(cx,cy),radius)
        for dx,dy in ((1,0),(0,1)):
            if (x+dx,y+dy) in floor:
                if dx: rect=(cx,cy-radius,tile,radius*2)
                else: rect=(cx-radius,cy,radius*2,tile)
                pg.draw.rect(raw,(0,0,0,0),rect)
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

def foe(target,pos,color,time,stunned=False,direction=(0,0),edible=False):
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
    pg.draw.circle(s,(120,180,255,22),(21,21),19)
    if name in ('Crown','Titan'):
        color=(255,222,76) if name=='Crown' else (114,255,98)
        pg.draw.circle(s,(*color,40),(21,21),16)
        pg.draw.circle(s,color,(21,21),11)
        pg.draw.circle(s,tuple(v//2 for v in color),(23,24),7)
        pg.draw.circle(s,(255,255,225),(17,17),4)
        if name=='Titan': pg.draw.lines(s,(255,255,255),False,[(12,8),(21,3),(30,8)],2)
    elif name=='Rush':
        pg.draw.rect(s,(192,206,235),(12,8,20,28),border_radius=5)
        pg.draw.rect(s,(107,78,183),(14,13,16,19),border_radius=3)
        pg.draw.ellipse(s,(239,244,255),(13,7,18,6))
        pg.draw.polygon(s,(255,239,80),[(22,13),(17,23),(23,23),(19,31),(28,20),(23,20)])
        for yy in (16,23,30): pg.draw.line(s,c,(4,yy),(10,yy),2)
    elif name=='Mist':
        pg.draw.circle(s,(46,54,67),(21,25),12)
        pg.draw.circle(s,(91,101,120),(18,21),8)
        pg.draw.circle(s,(192,205,219),(16,19),3)
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
        pg.draw.polygon(s,(243,64,54),[(25,11),(32,16),(30,26),(22,33),(10,35),(16,29),(21,21)])
        pg.draw.line(s,(255,159,110),(25,16),(23,24),3)
        pg.draw.lines(s,(99,215,73),False,[(24,12),(24,8),(31,6)],3)
    elif name=='Quake':
        for r in (7,12,17): pg.draw.ellipse(s,(255,170,100),(21-r,24-r//2,r*2,r),2)
        pg.draw.lines(s,c,False,[(6,15),(14,15),(18,5),(23,24),(27,15),(36,15)],2)
    elif name=='Heart':
        label=pg.font.Font(None,24).render('1UP',True,(134,255,101))
        pg.draw.rect(s,(28,61,34),(3,10,36,23),border_radius=5)
        pg.draw.rect(s,(134,255,101),(3,10,36,23),1,border_radius=5)
        s.blit(label,label.get_rect(center=(21,22)))
    else:
        pg.draw.arc(s,(255,109,130),(8,8,27,28),0,math.pi,8)
        pg.draw.rect(s,(255,109,130),(8,20,8,13)); pg.draw.rect(s,(92,193,255),(27,20,8,13))
        pg.draw.rect(s,c,(8,28,8,6)); pg.draw.rect(s,c,(27,28,8,6))
    if size!=42: s=pg.transform.smoothscale(s,(size,size))
    target.blit(s,(x-size//2,y-size//2))
