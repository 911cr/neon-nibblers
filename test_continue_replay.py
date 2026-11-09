"""Replay genuine simulated death/continue inputs, not synthetic device proof."""
import json
import unittest
from replay import record,replay,digest


class ContinueReplay(unittest.TestCase):
    def test_natural_death_and_continue_roundtrip_1_2_8(self):
        for count in (1,2,8):
            # Seed1 includes natural final-life losses with R18's longer
            # Giant timing; seed0's one-human station now survives this window.
            document=record(count,3,1,3600,fill_bots=True,
                rules={'starting_lives':1,'match_seconds':0,'bonus_threshold':0},
                continue_seconds=10,continue_delay=.2,auto_continue=True)
            restored=replay(json.loads(json.dumps(document)))
            self.assertEqual(digest(restored),document['final_digest'])
            continued=[event for event in restored.ledger.events if event['event']=='station_continue']
            self.assertTrue(continued,count)
            self.assertTrue(any(command.get('continue_stations') for command in document['commands']))
            self.assertEqual(restored.count,count)
            totals=restored.ledger.totals()
            self.assertTrue(all(player.score==totals.get(player.idx+1,0) for player in restored.players))
            self.assertTrue(all(event['context']['score_preserved'] for event in continued))

    def test_invalid_early_continue_command_rejected(self):
        document=record(1,3,42,60,continue_seconds=10)
        document['commands'][0]['continue_stations']=[0]
        with self.assertRaisesRegex(ValueError,'Invalid station continue'):replay(document)


if __name__=='__main__':unittest.main(verbosity=2)
