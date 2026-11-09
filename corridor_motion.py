"""Original constant-speed presentation along ordered corridor waypoints.

This module changes no simulation state and does not infer routes through walls.
Callers reset tracks when externally replacing their published visual position.
"""
from collections import deque
import math

_EPS = 1e-7


def _delta(start, end, period):
    result = []
    for index in range(2):
        value = end[index] - start[index]
        wrap = period[index] if period else None
        if wrap:
            value = (value + wrap / 2) % wrap - wrap / 2
        result.append(value)
    return tuple(result)


def _axis(delta):
    return abs(delta[0]) <= _EPS or abs(delta[1]) <= _EPS


class CorridorTrack:
    """Follow logical targets with bounded, axis-aligned visual motion.

    ``period=(width, None)`` enables horizontal tunnel wrapping. Axis-aligned
    logical jumps up to ``max_jump`` are permitted (including gate entries);
    diagonal or larger jumps reset immediately. A paused sample queues nothing.
    """

    def __init__(self, position, cell_size=20, max_jump=None):
        self.max_jump = 3 * cell_size if max_jump is None else max_jump
        self.reset(position)

    def reset(self, position):
        self.position = tuple(map(float, position))
        self.direction = (0, 0)
        self._last_target = self.position
        self._last_direction = (0., 0.)
        self._waypoints = deque()

    @property
    def remaining_path(self):
        """Read-only presentation route; never grants additional hit range."""
        return (self.position, *self._waypoints)

    def sample(self, target, dt, speed, period=None):
        if dt <= 0:
            return self.position
        target = tuple(map(float, target))
        change = _delta(self._last_target, target, period)
        if math.hypot(*change) > _EPS:
            if not _axis(change) or math.hypot(*change) > self.max_jump + _EPS:
                self.reset(target)
                return self.position
            # A logical reversal can cancel future waypoints before reaching
            # them. Keep any earlier corner needed to reach the new endpoint.
            matched = next((i for i, point in enumerate(self._waypoints)
                            if math.hypot(*_delta(point, target, period)) <= _EPS), None)
            reverse = sum(a*b for a,b in zip(change, self._last_direction)) < -_EPS
            if matched is not None:
                self._waypoints = deque(list(self._waypoints)[:matched+1])
            elif reverse and _axis(_delta(self.position, target, period)):
                self._waypoints = deque([target])
            else:
                self._waypoints.append(target)
            self._last_target = target
            self._last_direction = change

        budget = max(0., speed) * dt
        while self._waypoints:
            point = self._waypoints[0]
            delta = _delta(self.position, point, period)
            distance = math.hypot(*delta)
            if distance <= _EPS:
                self.position = point
                self._waypoints.popleft()
                continue
            if budget <= _EPS:
                break
            travel = min(budget, distance)
            self.direction = tuple(0 if abs(value) <= _EPS else
                                   (1 if value > 0 else -1) for value in delta)
            position = [self.position[i] + delta[i] * travel / distance for i in range(2)]
            for i in range(2):
                if period and period[i]:
                    position[i] %= period[i]
            self.position = tuple(position)
            budget -= travel
            if travel >= distance - _EPS:
                self.position = point
                self._waypoints.popleft()
        return self.position
