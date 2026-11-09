"""Deterministic original navigation, not a recovered commercial AI algorithm."""
from collections import deque
import heapq

DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def threat_distances(arena, threats):
    """Shortest legal corridor distance, including side tunnels and walls."""
    distances = {cell: 0 for cell in threats if cell in arena.lanes}
    queue = deque(sorted(distances))
    while queue:
        cell = queue.popleft()
        if distances[cell] >= 3: continue
        for direction in DIRECTIONS:
            nxt = arena.step(cell, direction)
            if nxt in arena.lanes and nxt not in distances:
                distances[nxt] = distances[cell] + 1
                queue.append(nxt)
    return distances


def choose_direction(match, player, directions):
    """Choose a legal low-risk route; active hunters seek edible targets.

    Risk costs improve the adaptation's bots. No exact DX difficulty, target
    algorithm, or reaction time is asserted by these implementation choices.
    """
    arena = match.arena
    giant = match.active(player, 'Titan')
    edible = giant or match.active(player, 'Crown') or match.active(player, 'Lure')
    roaming = {cell for i, cell in enumerate(match.foes)
               if i < len(match.foe_modes) and match.foe_modes[i] == 'roaming'}
    # Local means corridor distance, including wrap tunnels, not screen distance.
    local={player.pos:0}; frontier=deque([player.pos])
    while frontier:
        cell=frontier.popleft()
        if local[cell]>=14:continue
        for direction in directions:
            nxt=arena.step(cell,direction)
            if nxt not in local and arena.can_enter(nxt,player):
                local[nxt]=local[cell]+1;frontier.append(nxt)
    nearby=set(match.items)&local.keys()
    hunt=set(roaming) if edible else set()
    if giant:
        hunt.update(other.pos for other in match.players if other is not player
                    and other.lives>0 and other.safe<=0 and other.pos in arena.lanes
                    and not match.active(other,'Titan'))
    # A giant's rival target must not lose priority merely because ghosts are
    # currently inside their house. Protected/private-bay rivals are not goals.
    goals=(hunt or nearby or set(match.dots))-{player.pos}
    fallback_goals=set(match.dots)-{player.pos}
    threats = set()
    if player.safe <= 0 and not giant:
        if not edible: threats.update(roaming)
        threats.update(other.pos for other in match.players if other is not player
                       and other.lives > 0 and match.active(other, 'Titan'))
        for i, owner in match.foe_carriers.items():
            if owner != player.idx and match.players[owner].lives > 0 and match.active(match.players[owner], 'Lure'):
                threats.add(match.foes[i])
    danger = threat_distances(arena, threats)
    risk_cost = {0:100,1:30,2:7,3:2}
    def fallback_direction():
        legal=[d for d in directions if arena.can_enter(arena.step(player.pos,d),player)]
        if not legal:return (0,0)
        return min(legal,key=lambda d:(risk_cost.get(danger.get(arena.step(player.pos,d)),0),
                                      d!=player.wanted,d!=player.direction,directions.index(d)))
    if not goals:return fallback_direction()
    fallback=None
    costs = {player.pos: 0}
    queue = [(0, 0, player.pos, None)]
    serial = 0
    while queue:
        cost, _, cell, first = heapq.heappop(queue)
        if cost != costs.get(cell): continue
        if cell in goals:return first
        if fallback is None and cell in fallback_goals:fallback=first
        for direction in directions:
            nxt = arena.step(cell, direction)
            if not arena.can_enter(nxt, player): continue
            risk = risk_cost.get(danger.get(nxt), 0)
            next_cost = cost + 1 + risk
            if next_cost < costs.get(nxt, float('inf')):
                costs[nxt] = next_cost
                serial += 1
                heapq.heappush(queue, (next_cost, serial, nxt, first or direction))
    return fallback or fallback_direction()
