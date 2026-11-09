"""Deterministic contact rollback, independently authored (not measured DX physics)."""


from collections import deque

CELL_SIZE = 20
NORMAL_RADIUS = 17
GIANT_RADIUS = 36


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
    if p.pos==q.pos:return True
    if previous and previous[p.idx]==q.pos and previous[q.idx]==p.pos:return True
    giant_p=match.active(p,'Titan');giant_q=match.active(q,'Titan')
    radii=(GIANT_RADIUS if giant_p else NORMAL_RADIUS)+(GIANT_RADIUS if giant_q else NORMAL_RADIUS)
    limit=int(radii//CELL_SIZE)
    current=_corridor_distance(match.arena,p.pos,q.pos,limit)
    if current is None:return False
    if giant_p!=giant_q:return True
    if previous is None:return False
    old=_corridor_distance(match.arena,previous[p.idx],previous[q.idx],limit)
    return old is None or current<old


def resolve_bumps(match, contacts, previous):
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
        if pair in match.bump_cooldowns:
            continue
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
                            response='rollback_then_one_recoil_step')
    for idx, direction in impulses.items():
        p = actors[idx]
        p.direction = direction
        p.recoil = direction
        p.stun = max(p.stun, .12)
        p.clock = 0.
    # Only malformed/explicitly overlapping initial states need this fallback.
    match.separate_overlaps()
