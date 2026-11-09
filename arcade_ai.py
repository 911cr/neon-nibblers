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
    nearby = {cell for cell in match.items
              if abs(cell[0]-player.pos[0]) + abs(cell[1]-player.pos[1]) <= 14}
    goals = nearby or set(match.dots)
    if edible and roaming: goals = set(roaming)
    if giant:
        goals.update(other.pos for other in match.players if other is not player
                     and other.lives > 0 and other.safe <= 0
                     and not match.active(other, 'Titan'))
    goals.discard(player.pos)
    if not goals: return player.wanted
    threats = set()
    if player.safe <= 0 and not giant:
        if not edible: threats.update(roaming)
        threats.update(other.pos for other in match.players if other is not player
                       and other.lives > 0 and match.active(other, 'Titan'))
        for i, owner in match.foe_carriers.items():
            if owner != player.idx and match.players[owner].lives > 0 and match.active(match.players[owner], 'Lure'):
                threats.add(match.foes[i])
    danger = threat_distances(arena, threats)
    costs = {player.pos: 0}
    queue = [(0, 0, player.pos, None)]
    serial = 0
    while queue:
        cost, _, cell, first = heapq.heappop(queue)
        if cost != costs.get(cell): continue
        if cell in goals: return first
        for direction in directions:
            nxt = arena.step(cell, direction)
            if not arena.can_enter(nxt, player): continue
            risk = {0: 100, 1: 30, 2: 7, 3: 2}.get(danger.get(nxt), 0)
            next_cost = cost + 1 + risk
            if next_cost < costs.get(nxt, float('inf')):
                costs[nxt] = next_cost
                serial += 1
                heapq.heappush(queue, (next_cost, serial, nxt, first or direction))
    return player.wanted
