"""Original procedural arcade art. No commercial sprites, logos or source code."""
import math
from functools import lru_cache
import pygame as pg

def maze_background(floor, cols, rows, tile, accent,radius=32):
    size=(cols*tile,rows*tile)
    raw=pg.Surface(size,pg.SRCALPHA)
    # Carve a constant-width tube around the SAME graph used by movement.
    # A free-looking gap can no longer disagree with the collision map.
    raw.fill((255,255,255))
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
    corner=2 if radius<30 else 5
    offsets=[(x,y) for x in range(-corner,corner+1) for y in range(-corner,corner+1) if x*x+y*y<=corner*corner]
    core=mask.copy()
    erosion=((2,0),(-2,0),(0,2),(0,-2),(1,1),(-1,1),(1,-1),(-1,-1)) if corner==2 else ((5,0),(-5,0),(0,5),(0,-5),(4,3),(-4,3),(4,-3),(-4,-3))
    for offset in erosion:
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
    if radius < 30:
        # Larger convex corners are visible on the observed connected branches.
        # Opening them alone would erase narrow stems, so restore only long
        # removed features; small corner chips stay removed and rounded.
        smooth_core = rounded.copy()
        for offset in ((12,0),(-12,0),(0,12),(0,-12),(8,8),(-8,8),(8,-8),(-8,-8)):
            shifted = pg.mask.Mask(size); shifted.draw(rounded, offset)
            smooth_core = smooth_core.overlap_mask(shifted, (0,0))
        smooth = pg.mask.Mask(size)
        for xx in range(-12,13):
            for yy in range(-12,13):
                if xx*xx+yy*yy <= 144:
                    smooth.draw(smooth_core, (xx,yy))
        smooth = smooth.overlap_mask(rounded, (0,0))
        removed = rounded.copy(); removed.erase(smooth, (0,0))
        for component in removed.connected_components():
            box = component.get_bounding_rects()[0]
            if max(box.size) > 28:
                smooth.draw(component, (0,0))
        rounded = smooth
    # Observed A/B isolated bars have capsule ends, rather than square tips.
    # Restrict this to straight narrow islands: connected hooks, the frame and
    # house footprint keep their collision-derived contours and thin stems.
    if radius < 30:
        for component in rounded.connected_components(20):
            bounds = component.get_bounding_rects()[0]
            short, long = min(bounds.size), max(bounds.size)
            if (bounds.left <= tile or bounds.top <= tile or
                    bounds.right >= size[0]-tile or bounds.bottom >= size[1]-tile):
                continue
            if not (4 <= short <= 40 and long >= short*2 and
                    component.count() >= bounds.width*bounds.height*.90):
                continue
            capsule = pg.Surface(size, pg.SRCALPHA)
            pg.draw.rect(capsule, (255,255,255), bounds, border_radius=short//2)
            rounded.erase(component, (0,0))
            rounded.draw(pg.mask.from_surface(capsule).overlap_mask(component, (0,0)), (0,0))
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
    # The reconstructed A/B layouts use ordinary single-contour capsules.
    # Preserve their two outer edges; do not add an inner rectangle merely
    # because a long narrow wall happens to exceed the old area threshold.
    if radius<30:return result
    # Broad wall islands have a second inset contour, as visible on the
    # rectangular DX island in the retained 1:15 reference. Erosion removes
    # thin capsules and the frame from this pass, preserving their silhouette.
    broad=mask.copy()
    for offset in ((12,0),(-12,0),(0,12),(0,-12),(9,9),(-9,9),(9,-9),(-9,-9)):
        shifted=pg.mask.Mask(size);shifted.draw(mask,offset)
        broad=broad.overlap_mask(shifted,(0,0))
    filtered=pg.mask.Mask(size)
    for component in broad.connected_components(500):filtered.draw(component,(0,0))
    broad=filtered
    core=broad.copy()
    for offset in ((1,0),(-1,0),(0,1),(0,-1)):
        shifted=pg.mask.Mask(size);shifted.draw(broad,offset)
        core=core.overlap_mask(shifted,(0,0))
    inset=broad.copy();inset.erase(core,(0,0))
    result.blit(inset.to_surface(setcolor=accent,unsetcolor=(0,0,0,0)),(0,0))
    return result

@lru_cache(maxsize=32)
def _sphere_template(color):
    """One high-resolution lighting calculation per original character color."""
    r=108;mid=r
    s=pg.Surface((r*2+1,r*2+1),pg.SRCALPHA)
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

@lru_cache(maxsize=256)
def sphere(color,radius):
    scale=3;r=radius*scale;mid=(radius+9)*scale
    s=pg.Surface((mid*2,mid*2),pg.SRCALPHA)
    body=pg.transform.smoothscale(_sphere_template(color),(r*2+1,r*2+1))
    s.blit(body,(mid-r,mid-r))
    return s

def muncher(target, pos, color, direction, time, radius=15, powered=False, safe=False,opacity=255):
    scale=3; r=radius*scale; mid=(radius+9)*scale
    s=sphere(tuple(color),radius).copy()
    if powered or safe:
        pg.draw.circle(s,(*color,55),(mid,mid),r+5*scale,2*scale)
    angle=.035+.77*(.5+.5*math.sin(time*22))
    # Move facial geometry, not the lighting. Left-facing sprites mirror their
    # face rather than rotating their eye underneath the mouth.
    def face_point(x,y):
        if direction==(-1,0): x=-x
        elif direction==(0,-1): x,y=y,-x
        elif direction==(0,1): x,y=-y,x
        return round(mid+x),round(mid+y)
    mouth=[face_point(0,0),face_point(r*1.3,-math.tan(angle)*r*1.3),
           face_point(r*1.3,math.tan(angle)*r*1.3)]
    pg.draw.polygon(s,(0,0,0,0),mouth)
    eye=face_point(r*.03,-r*.51)
    ew,eh=(r*.26,r*.14) if direction[1] else (r*.14,r*.26)
    pg.draw.ellipse(s,(12,14,24),(eye[0]-ew/2,eye[1]-eh/2,ew,eh))
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
    if stunned and not eyes_only:
        # New, original readable feedback for a state that previously had none.
        units=s.get_width()/58
        for index in range(3):
            angle=time*5+index*math.tau/3
            sx=29+math.cos(angle)*19; sy=29-19+math.sin(angle)*4
            points=[(sx,sy-3),(sx+1,sy-1),(sx+4,sy),(sx+1,sy+1),
                    (sx,sy+3),(sx-1,sy+1),(sx-4,sy),(sx-1,sy-1)]
            pg.draw.polygon(s,(255,236,133),[(round(px*units),round(py*units)) for px,py in points])
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

class _IconDraw:
    """Draw the original 42-unit icon vectors at 3x before downsampling."""
    def __init__(self, surface): self.surface=surface
    def point(self, p): return tuple(round(v*3) for v in p)
    def rect(self, color, rect, width=0, border_radius=0):
        pg.draw.rect(self.surface,color,self.point(rect),width*3,border_radius=border_radius*3)
    def ellipse(self, color, rect, width=0):
        pg.draw.ellipse(self.surface,color,self.point(rect),width*3)
    def circle(self, color, center, radius, width=0):
        pg.draw.circle(self.surface,color,self.point(center),round(radius*3),width*3)
    def polygon(self, color, points, width=0):
        pg.draw.polygon(self.surface,color,[self.point(p) for p in points],width*3)
    def line(self, color, start, end, width=1):
        pg.draw.line(self.surface,color,self.point(start),self.point(end),width*3)
    def lines(self, color, closed, points, width=1):
        pg.draw.lines(self.surface,color,closed,[self.point(p) for p in points],width*3)
    def arc(self, color, rect, start, stop, width=1):
        pg.draw.arc(self.surface,color,self.point(rect),start,stop,width*3)


@lru_cache(maxsize=128)
def _power_sprite(name,size):
    if type(size) is not int or size < 1: raise ValueError("Icon size must be a positive integer")
    s=pg.Surface((126,126),pg.SRCALPHA)
    draw=_IconDraw(s)
    if name in ('Crown','Titan'):
        color=(255,222,76) if name=='Crown' else (114,255,98)
        draw.circle((*color,40),(21,21),16)
        orb=pg.transform.smoothscale(sphere(tuple(color),11),(120,120))
        s.blit(orb,(3,3))
    elif name=='Rush':
        # Independently drawn handled coffee mug from the observed object type.
        draw.ellipse((145,156,181),(27,14,13,20),5)
        draw.rect((167,180,204),(9,11,22,24),border_radius=5)
        draw.rect((215,222,232),(10,12,6,20),border_radius=3)
        draw.ellipse((236,239,245),(9,7,22,10))
        draw.ellipse((103,65,32),(12,9,16,6))
        draw.polygon((255,205,75),[(23,16),(17,24),(22,24),(19,31),(27,21),(22,21)])
    elif name=='Mist':
        draw.circle((129,124,106),(21,25),12)
        draw.circle((176,171,146),(18,21),8)
        draw.arc((98,96,82),(10,14,23,23),.7,2.6,2)
        draw.line((112,108,91),(12,29),(27,16),2)
        draw.line((112,108,91),(19,36),(31,24),2)
        draw.circle((209,208,180),(16,19),3)
        draw.lines((210,180,100),False,[(23,14),(26,9),(23,5)],2)
        draw.circle((255,200,85),(23,5),3)
    elif name=='Veil':
        draw.circle((239,244,255),(21,18),13)
        draw.polygon((239,244,255),[(8,18),(34,18),(36,35),(28,31),(23,36),(17,32),(9,36)])
        draw.ellipse((41,51,89),(13,16,6,9)); draw.ellipse((41,51,89),(24,16,6,9))
    elif name=='Slick':
        draw.polygon((255,218,61),[(22,11),(23,24),(36,32),(27,32),(20,27),(10,35),(5,33),(16,23)])
        draw.polygon((255,245,157),[(22,11),(18,22),(19,28),(23,24)])
        draw.polygon((230,174,36),[(23,24),(31,29),(36,32),(27,32)])
        draw.line((130,103,40),(22,11),(24,7),3)
    elif name=='Spark':
        draw.polygon((123,230,255),[(23,3),(9,24),(20,23),(16,39),(34,16),(23,18)])
    elif name=='Flare':
        draw.polygon((255,91,27),[(10,27),(5,18),(9,9),(12,17),(16,4),(20,16),(17,24)])
        draw.polygon((255,222,73),[(11,25),(9,18),(14,12),(15,20),(17,18),(16,25)])
        draw.polygon((243,64,54),[(28,18),(33,21),(29,28),(20,33),(6,35),(15,30),(22,25)])
        draw.line((255,159,110),(27,22),(20,28),3)
        draw.lines((99,215,73),False,[(28,18),(28,13),(33,12)],3)
    elif name=='Quake':
        draw.rect((141,35,39),(10,19,24,19),border_radius=2)
        draw.rect((225,57,54),(9,17,23,19),border_radius=2)
        draw.rect((252,115,92),(10,18,5,17))
        draw.rect((155,164,178),(19,6,5,13))
        draw.rect((196,204,213),(10,4,24,6),border_radius=3)
        draw.lines((255,234,211),False,[(17,22),(24,22),(19,26),(25,31),(18,31)],2)
    elif name=='Heart':
        # Original block lettering, no commercial logo asset.
        white=(249,250,255)
        draw.polygon(white,[(6,12),(14,7),(19,7),(19,31),(23,31),(23,36),(8,36),(8,31),(13,31),(13,15),(6,18)])
        label=pg.font.Font(None,57).render('UP',True,white)
        s.blit(label,(60,27))
    else:
        draw.arc((40,121,194),(6,7,29,29),math.pi/2,math.pi*1.5,9)
        draw.rect((40,121,194),(20,7,12,9))
        draw.rect((40,121,194),(20,27,12,9))
        draw.rect((224,230,239),(28,7,6,9))
        draw.rect((224,230,239),(28,27,6,9))
    return pg.transform.smoothscale(s,(size,size))


def power_icon(target,pos,name,time,size=32):
    # Position-independent phase prevents roaming items from jumping vertically
    # whenever they move one grid cell. Same category keeps a stable phase.
    phase=sum(ord(ch) for ch in name)*.13
    x,y=pos
    y+=round(math.sin(time*3+phase)*size/16)
    target.blit(_power_sprite(name,size),(round(x)-size//2,round(y)-size//2))


def fire_plume(target,origin,end,direction,time):
    """Original animated flame contained within a legal straight corridor run.

    The caller splits wrapping paths into contiguous runs. A backwards endpoint
    is rejected so a tunnel wrap cannot accidentally paint across the board.
    Longitudinal extent never exceeds origin/end; transverse radius stays <=16.
    """
    if direction not in ((1,0),(-1,0),(0,1),(0,-1)): return
    dx,dy=direction
    vx,vy=end[0]-origin[0],end[1]-origin[1]
    distance=vx*dx+vy*dy
    if distance<=0 or abs(vx*dy-vy*dx)>.5: return
    length=max(1,round(distance)); scale=3; mid=16
    flame=pg.Surface(((length+1)*scale,33*scale),pg.SRCALPHA)
    def layer(extent,factor,color):
        steps=max(3,math.ceil(extent/4))
        top=[];bottom=[]
        for i in range(steps+1):
            fraction=i/steps; x=fraction*extent
            envelope=min(15,2+12*math.sin(math.pi*(.12+.88*fraction)))
            ripple=math.sin(time*19-fraction*14)*1.2*math.sin(math.pi*fraction)
            half=max(.3,min(15,(envelope+ripple)*factor))
            sway=math.sin(time*23-fraction*19)*min(1.4,15-half)*math.sin(math.pi*fraction)
            # Taper to a definite endpoint rather than a circular cap beyond it.
            if i==steps: half=.3
            top.append((round(x*scale),round((mid+sway-half)*scale)))
            bottom.append((round(x*scale),round((mid+sway+half)*scale)))
        pg.draw.polygon(flame,color,top+bottom[::-1])
    layer(length,1,(255,70,21,190))
    layer(length*.88,.68,(255,178,39,235))
    layer(min(length*.58,40),.37,(255,251,202,250))
    fade=pg.Surface(flame.get_size(),pg.SRCALPHA)
    for x in range(flame.get_width()):
        alpha=round(255*(1-.8*(x/max(1,flame.get_width()-1))**2))
        pg.draw.line(fade,(255,255,255,alpha),(x,0),(x,flame.get_height()))
    flame.blit(fade,(0,0),special_flags=pg.BLEND_RGBA_MULT)
    flame=pg.transform.smoothscale(flame,(length+1,33))
    angle=180 if dx<0 else 90 if dy<0 else -90 if dy>0 else 0
    if angle: flame=pg.transform.rotate(flame,angle)
    if dx: position=(round(min(origin[0],end[0])),round(origin[1])-mid)
    else: position=(round(origin[0])-mid,round(min(origin[1],end[1])))
    target.blit(flame,position)
