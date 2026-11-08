"""Record/replay real logic inputs at a fixed 60 Hz, independent of rendering.

python replay.py record replay.json --players 8 --seconds 20 --seed 42
python replay.py verify replay.json
Only independently authored simulation data is stored, never commercial media.
"""
import argparse
import hashlib
import json
import math
import os
from pathlib import Path

os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
from game import Match, DIRS, steer_demo

STEP = 1 / 60


def digest(match):
    payload = {'state': match.snapshot(), 'events': match.ledger.events}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def movement_sample(match):
    return {'tick': match.tick,
            'players': [{'player_id': p.idx+1, 'position': list(p.pos),
                         'direction': list(p.direction), 'lives': p.lives}
                        for p in match.players if getattr(p, 'joined', True)],
            'ghosts': [{'ghost_id': i, 'position': list(c), 'mode': match.foe_modes[i]}
                       for i, c in enumerate(match.foes)]}


class FixedStepper:
    """Accumulate render elapsed time without dropping logic time or overshoot."""
    def __init__(self, match, before_step=None):
        self.match = match
        self.before_step = before_step
        self.pending = 0.
        self.steps = 0

    def advance(self, elapsed):
        if not math.isfinite(elapsed) or elapsed < 0:
            raise ValueError('Elapsed time must be finite and non-negative')
        self.pending += elapsed
        sounds = []
        while self.pending + 1e-12 >= STEP:
            if self.before_step: self.before_step(self.match, self.steps)
            sounds.extend(self.match.update(STEP))
            self.pending -= STEP
            if abs(self.pending) < 1e-12: self.pending = 0.
            self.steps += 1
        return sounds


def record(count=8, theme=0, seed=42, frames=1200, progression='cycle'):
    match = Match(count, theme, seed, progression=progression)
    commands = []
    checkpoints = []
    movement = []
    for frame in range(frames):
        steer_demo(match)
        commands.append({'directions': [list(p.wanted) for p in match.players]})
        match.update(STEP)
        if (frame + 1) % 60 == 0 or frame + 1 == frames:
            checkpoints.append({'frame': frame + 1, 'digest': digest(match)})
        if (frame + 1) % 6 == 0 or frame + 1 == frames:
            movement.append(movement_sample(match))
    return {'schema_version': 1, 'step': STEP,
            'initial': {'count': count, 'theme': theme, 'seed': seed,
                        'score_values': match.score_values, 'progression': progression},
            'commands': commands, 'checkpoints': checkpoints, 'movement_trace': movement,
            'events': match.ledger.events, 'final_digest': digest(match)}


def replay(document):
    if document.get('schema_version') != 1 or document.get('step') != STEP:
        raise ValueError('Unsupported replay schema or simulation step')
    match = Match(**document['initial'])
    checkpoints = {item['frame']: item['digest'] for item in document.get('checkpoints', [])}
    movement = {item['tick']: item for item in document.get('movement_trace', [])}
    for frame, command in enumerate(document['commands'], 1):
        for idx in command.get('join_stations', []):
            match.join_station(idx)
        directions = command['directions']
        if len(directions) != len(match.players): raise ValueError('Replay roster does not match')
        for player, direction in zip(match.players, directions):
            direction = tuple(direction)
            if direction not in DIRS + [(0, 0)]: raise ValueError('Invalid direction')
            player.wanted = direction
        match.update(STEP)
        if frame in checkpoints and digest(match) != checkpoints[frame]:
            raise ValueError(f'Replay diverged at frame {frame}')
        if match.tick in movement and movement_sample(match) != movement[match.tick]:
            raise ValueError(f'Replay movement differs at tick {match.tick}')
    if digest(match) != document['final_digest']:
        raise ValueError('Replay final state/event digest differs')
    if match.ledger.events != document['events']:
        # JSON serializes context tuples as lists: compare normalized structures.
        if json.loads(json.dumps(match.ledger.events)) != document['events']:
            raise ValueError('Replay score/event trace differs')
    return match


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('record', 'verify'))
    parser.add_argument('path', type=Path)
    parser.add_argument('--players', type=int, choices=range(1, 9), default=8)
    parser.add_argument('--theme', type=int, choices=range(4), default=0)
    parser.add_argument('--seconds', type=float, default=20)
    parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args()
    if args.action == 'record':
        if not 0 < args.seconds <= 180: parser.error('Seconds must be in (0, 180]')
        data = record(args.players, args.theme, args.seed, round(args.seconds * 60))
        args.path.write_text(json.dumps(data, indent=2), encoding='utf-8')
    else:
        data = json.loads(args.path.read_text(encoding='utf-8'))
    match = replay(data)
    print(json.dumps({'verified': True, 'frames': len(data['commands']),
                      'events': len(match.ledger.events), 'digest': digest(match),
                      'rankings': match.rankings()}))


if __name__ == '__main__':
    main()
