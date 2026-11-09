"""Versioned, JSON-safe simulation events; values are adaptation tuning, not DX facts."""
import copy
import json
from pathlib import Path

DEFAULT_SCORES = {'dot': 10, 'pickup': 75, 'ghost_eaten': 200,
                  'ghost_burned': 200, 'rival_eaten': 300, 'rival_burned': 300,
                  'carried_ghost_hit': 300, 'stage_clear': 500}


class ScoreLedger:
    def __init__(self):
        self.events = []

    def append(self, match, event, player=None, delta=0, **context):
        record = {'sequence': len(self.events), 'timestamp': round(match.elapsed, 9),
                  'tick': match.tick, 'event': event,
                  'player_id': player.idx + 1 if player is not None else None,
                  'stage': match.stage, 'delta': delta,
                  'score': player.score if player is not None else None,
                  'context': copy.deepcopy(context)}
        self.events.append(record)
        return record

    def write(self, path):
        Path(path).write_text(json.dumps({'schema_version': 1, 'events': self.events},
                                      indent=2), encoding='utf-8')

    def totals(self):
        """Current station accounts; joining starts a fresh human score account.

        Preserve prior bot awards in history without carrying their points into
        the replacement human account or emitting fictitious negative awards.
        """
        totals = {}
        for event in self.events:
            if event['player_id'] is not None:
                idx = event['player_id']
                if event['event'] == 'station_join':
                    totals[idx] = event['score']
                else:
                    totals[idx] = totals.get(idx, 0) + event['delta']
        return totals
