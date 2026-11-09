"""Pure cosmetic corridor paths; never supplies damage or collision geometry."""
import math

_EPS=1e-6


def corridor_segments(arena, points, origin=(50,50), tile=20, columns=59):
    """Return wall-safe screen-space ``(start, end, direction)`` segments.

    Only public lane centerlines are accepted. Invalid links break continuity;
    they are never repaired by finding a speculative route. Portal crossings
    split at the two board edges rather than drawing across the entire maze.
    """
    if tile<=0 or columns<=0:
        raise ValueError('tile and columns must be positive')
    width=tile*columns
    lanes=arena.lanes
    out=[]
    join=False

    def center_index(value):
        index=round(value/tile-.5)
        return index if abs(value-(index+.5)*tile)<_EPS else None

    def valid(a,b):
        dx,dy=b[0]-a[0],b[1]-a[1]
        if abs(dx)>_EPS and abs(dy)>_EPS:return False
        if abs(dx)<=_EPS and abs(dy)<=_EPS:return False
        axis=0 if abs(dx)>_EPS else 1
        fixed=center_index(a[1-axis])
        if fixed is None:return False
        lo,hi=sorted((a[axis],b[axis]))
        # Edges are accepted only as the boundary of the adjacent public cell.
        start=math.floor((lo+_EPS)/tile)
        stop=math.floor((hi-_EPS)/tile)
        for moving in range(start,stop+1):
            cell=(moving,fixed) if axis==0 else (fixed,moving)
            if cell not in lanes:return False
        return start<=stop

    def add(a,b,allow_join):
        if not valid(a,b):return False
        # Remove harmless floating-point drift rather than emitting a nominally
        # diagonal segment with a two-axis direction.
        if abs(b[0]-a[0])<=_EPS:b=(a[0],b[1])
        else:b=(b[0],a[1])
        direction=(int(b[0]>a[0])-int(b[0]<a[0]),int(b[1]>a[1])-int(b[1]<a[1]))
        a=(a[0]+origin[0],a[1]+origin[1]);b=(b[0]+origin[0],b[1]+origin[1])
        if allow_join and out and out[-1][2]==direction and all(abs(x-y)<_EPS for x,y in zip(out[-1][1],a)):
            out[-1]=(out[-1][0],b,direction)
        else:out.append((a,b,direction))
        return True

    local=[]
    for point in points:
        try:
            p=(float(point[0])-origin[0],float(point[1])-origin[1])
            local.append(p if all(math.isfinite(v) for v in p) else None)
        except (TypeError,ValueError,IndexError):local.append(None)
    for a,b in zip(local,local[1:]):
        if a is None or b is None:join=False;continue
        dx,dy=b[0]-a[0],b[1]-a[1]
        if abs(dx)<_EPS and abs(dy)<_EPS:continue
        row=center_index(a[1])
        if abs(dy)<_EPS and abs(dx)>width/2 and row in arena.portals and 0<=a[0]<=width and 0<=b[0]<=width:
            first_edge=0 if dx>0 else width
            second_edge=width-first_edge
            left=(first_edge,a[1]);right=(second_edge,b[1])
            # Validate both halves before emitting either one.
            first_empty=math.dist(a,left)<_EPS
            second_empty=math.dist(right,b)<_EPS
            if (first_empty or valid(a,left)) and (second_empty or valid(right,b)):
                if not first_empty:add(a,left,join)
                if not second_empty:add(right,b,False)
                join=True
            else:join=False
        else:join=add(a,b,join)
    return out
