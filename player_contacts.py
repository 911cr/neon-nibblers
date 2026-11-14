"""Deterministic contact rollback, independently authored (not measured DX physics)."""


from collections import deque
import math

CELL_SIZE = 20
NORMAL_RADIUS = 17
GIANT_RADIUS = 36


def giant_contact(match,p,q):
    """Test solid body discs at the fixed-tick poses, through a clear corridor."""
    if p.pos not in match.arena.lanes or q.pos not in match.arena.lanes:
        return False
    first,ra=match.body_circle(p)
    second,rb=match.body_circle(q)
    ax,ay=first
    dx,dy=second[0]-ax,second[1]-ay
    width=match.arena.width*CELL_SIZE
    seam=abs(dx)>width/2
    if seam:
        if p.pos[1]!=q.pos[1] or p.pos[1] not in match.arena.portals:return False
        dx=(dx+width/2)%width-width/2
    if dx*dx+dy*dy>(ra+rb)**2:return False
    # Centers are in board-local pixels. Sample the same solid-wall mask that
    # the renderer uses, including thin islands and rounded junction corners.
    steps=max(1,math.ceil(max(abs(dx),abs(dy))))
    mask=match.arena.wall_mask()
    for i in range(steps+1):
        x=round(ax+dx*i/steps)%width
        y=round(ay+dy*i/steps)
        if not 0<=y<mask.get_size()[1] or mask.get_at((x,y)):return False
    return True


def _touch_offsets(match, p, q, attempted):
    """Follow the two actual attempted edges until the circular bodies touch."""
    arena = match.arena
    moves = []
    for actor in (p, q):
        step = actor.direction
        moved = (actor.pos != attempted[actor.idx] and
                 arena.step(actor.pos,step) == attempted[actor.idx])
        moves.append(step if moved else (0,0))
    dx = q.pos[0]-p.pos[0]
    if p.pos[1] == q.pos[1] and p.pos[1] in arena.portals:
        width = max(x for x,y in arena.lanes if y == p.pos[1])+1
        dx = (dx+width//2)%width-width//2
    dy = q.pos[1]-p.pos[1]
    radius = 2*(GIANT_RADIUS if match.active(p,'Titan') else NORMAL_RADIUS)/CELL_SIZE
    # Grid and render use the same centerline. Only advance along a real edge.
    lo, hi = 0., 1.
    if dx*dx+dy*dy <= radius*radius:
        return [(0.,0.),(0.,0.)]
    for _ in range(10):
        t = (lo+hi)/2
        x = dx+t*(moves[1][0]-moves[0][0])
        y = dy+t*(moves[1][1]-moves[0][1])
        if x*x+y*y > radius*radius: lo=t
        else: hi=t
    return [(x*lo*CELL_SIZE,y*lo*CELL_SIZE) for x,y in moves]


def _corridor_distance(arena, start, goal, limit):
    """Bounded graph distance; walls and private bay endpoints are excluded."""
    if start not in arena.lanes or goal not in arena.lanes:return None
    queue=deque([(start,0)]);seen={start}
    while queue:
        cell,steps=queue.popleft()
        if cell==goal:return steps
        if steps==limit:continue
        for direction in ((1,0),(-1,0),(0,1),(0,-1)):
            nxt=arena.step(cell,direction)
            if nxt in arena.lanes and nxt not in seen:
                seen.add(nxt);queue.append((nxt,steps+1))
    return None


def approaching_contact(match, p, q, previous=None):
    """Radius-aware grid contact, not continuous rendered-disc collision.

    Use legal corridor distance (including tunnels), so nearby parallel lanes
    do not collide through a wall. Equal bodies must be approaching; unchanged
    following separation is not repeatedly blocked. A newly grown giant can
    threaten a smaller body already nearby without either one moving.
    """
    if min(p.lives,q.lives)<=0:return False
    giant_p=match.active(p,'Titan');giant_q=match.active(q,'Titan')
    if giant_p!=giant_q:return giant_contact(match,p,q)
    if p.pos==q.pos:return True
    if previous and previous[p.idx]==q.pos and previous[q.idx]==p.pos:return True
    radii=(GIANT_RADIUS if giant_p else NORMAL_RADIUS)+(GIANT_RADIUS if giant_q else NORMAL_RADIUS)
    limit=int(radii//CELL_SIZE)
    current=_corridor_distance(match.arena,p.pos,q.pos,limit)
    if current is None:return False
    if previous is None:return False
    old=_corridor_distance(match.arena,previous[p.idx],previous[q.idx],limit)
    return old is None or current<old


def resolve_bumps(match, contacts, previous, separate=True):
    """Resolve a whole contact group before moving any participant.

    Rolling back a contact can occupy a following player's destination. Include
    those followers in the rollback until reservations are consistent. Valid
    unique starting positions never need an arbitrary multi-cell crowd shove.
    """
    actors = {p.idx: p for p in match.players if p.lives > 0}
    origins = {idx: p.pos for idx, p in actors.items()}
    rollback = {p.idx for pair in contacts for p in pair}
    if previous:
        while True:
            reserved = {previous[idx] for idx in rollback}
            followers = {idx for idx, p in actors.items() if idx not in rollback
                         and p.pos in reserved and previous[idx] != p.pos
                         and p.pos in match.arena.lanes}
            if not followers:
                break
            rollback.update(followers)
        for idx in rollback:
            if match.arena.can_enter(previous[idx], actors[idx]):
                actors[idx].pos = previous[idx]
    impulses = {}
    for p, q in contacts:
        pair = tuple(sorted((p.idx, q.idx)))
        for actor, offset in zip((p,q),_touch_offsets(match,p,q,origins)):
            if actor.pos in match.arena.lanes:
                match.contact_offsets.setdefault(actor.idx, (actor.pos,offset))
        if pair in match.bump_cooldowns or pair in match.contact_origins:
            continue
        match.contact_origins[pair] = tuple(actors[idx].pos for idx in pair)
        match.bump_cooldowns[pair] = .28
        for actor, other in ((p, q), (q, p)):
            reverse = (-actor.direction[0], -actor.direction[1])
            # Stationary bodies recoil away from the incoming participant.
            stationary = reverse == (0, 0) or (previous and previous[actor.idx] == origins[actor.idx])
            if stationary:
                if other.direction != (0, 0):
                    reverse = other.direction
                else:
                    dx = actor.pos[0] - origins[other.idx][0]
                    dy = actor.pos[1] - origins[other.idx][1]
                    reverse = ((1 if dx > 0 else -1), 0) if abs(dx) > abs(dy) else (0, 1 if dy > 0 else -1)
            impulses.setdefault(actor.idx, reverse)
        match.ledger.append(match, 'player_bump', p, other_player_id=q.idx + 1,
                            positions=[list(p.pos), list(q.pos)],
                            response='touch_then_separate')
    for idx, direction in impulses.items():
        p = actors[idx]
        p.recoil = direction
        # Keep the incoming face during the shove. The body slides backward.
        # Reserve a short contact beat within the usual movement cadence.
        p.clock = max(0., match.player_interval(p)-.09)
    # Only malformed/explicitly overlapping initial states need this fallback.
    if separate:match.separate_overlaps()
