"""Explicit simulation estimates; these are not measured DX timings.

Use --tuning PATH to load partial overrides. Each Match owns a validated copy;
the complete effective configuration is included in event logs and replays.
"""
import copy
import json
import math
from pathlib import Path

DEFAULT_TUNING = {
    'durations': {'Crown': 7., 'Titan': 7., 'Rush': 7., 'Mist': 7.,
                  'Slick': 2., 'Spark': 2., 'Veil': 7., 'Flare': 3.,
                  'Quake': 5., 'Lure': 7.},
    'spawn_seconds': 3., 'item_step_seconds': .60,
    # Two DX actor tracks suggest roughly2.4–5 dots/sec. Use4 as a
    # provisional reference pace; relative boost/foe ratios remain authored.
    'player_step_seconds': .25, 'rush_step_seconds': .1625,
    'slick_step_seconds': .1375, 'ghost_step_seconds': .40,
    'spark_radius': 8, 'flame_cells': 5, 'smoke_seconds': 2.5,
    'smoke_radius': 2, 'quake_multiplier': 2., 'smoke_multiplier': 2.,
    'max_items': 12,
}


def validate_tuning(overrides=None):
    if overrides is None: overrides = {}
    if not isinstance(overrides, dict): raise ValueError('Tuning must be an object')
    if set(overrides) - set(DEFAULT_TUNING): raise ValueError('Unknown tuning setting')
    result = copy.deepcopy(DEFAULT_TUNING)
    for key, value in overrides.items():
        if key == 'durations':
            if not isinstance(value, dict) or set(value) - set(result[key]):
                raise ValueError('Unknown power duration')
            result[key].update(value)
        else: result[key] = value
    for name, value in result['durations'].items():
        _number(name + ' duration', value, 1 / 60, 120)
    for key in ('spawn_seconds', 'item_step_seconds', 'player_step_seconds',
                'rush_step_seconds', 'slick_step_seconds', 'ghost_step_seconds'):
        _number(key, result[key], 1 / 60, 120)
    _number('smoke_seconds', result['smoke_seconds'], 1 / 60, 120)
    for key in ('quake_multiplier', 'smoke_multiplier'):
        _number(key, result[key], 1, 10)
    for key, low, high in [('spark_radius', 0, 60), ('flame_cells', 1, 59),
                           ('smoke_radius', 0, 30), ('max_items', 1, 64)]:
        if type(result[key]) is not int or not low <= result[key] <= high:
            raise ValueError('Invalid ' + key)
    return result


def _number(name, value, low, high):
    if type(value) not in (int, float) or not math.isfinite(value) or not low <= value <= high:
        raise ValueError('Invalid ' + name)


def load_tuning(path):
    return validate_tuning(json.loads(Path(path).read_text(encoding='utf-8')))
