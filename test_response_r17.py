"""Input intent and crowd recovery checks; no physical-device timing claim."""
import os
os.environ['SDL_VIDEODRIVER']='dummy'
os.environ['SDL_AUDIODRIVER']='dummy'
from collections import defaultdict
import unittest
from unittest.mock import patch
import game


class KeyboardResponse(unittest.TestCase):
    def setUp(self):
        self.app=game.App(simulate_controllers=True)
        self.app.cabinet.settings['free_play']=True
        self.app.count=8;self.app.start();self.held=defaultdict(bool)

    def tearDown(self):game.pg.quit()

    def key(self,key,down):
        self.held[key]=down
        event=game.pg.event.Event(game.pg.KEYDOWN if down else game.pg.KEYUP,key=key,mod=0)
        with patch.object(game.pg.event,'get',return_value=[event]):self.app.events()
        with patch.object(game.pg.key,'get_pressed',return_value=self.held):self.app.inputs()

    def test_new_turn_wins_over_older_held_direction_all_eight_stations(self):
        for p in self.app.match.players:
            right,left,down,up=game.KEYS[p.idx]
            self.key(up,True);self.key(right,True)
            self.assertEqual(p.wanted,(1,0),p.idx)
            self.key(left,True)
            self.assertEqual(p.wanted,(-1,0),p.idx)

    def test_release_falls_back_to_remaining_held_then_retains_buffer(self):
        for p in self.app.match.players:
            right,left,down,up=game.KEYS[p.idx]
            self.key(up,True);self.key(right,True);self.key(right,False)
            self.assertEqual(p.wanted,(0,-1),p.idx)
            self.key(up,False)
            self.assertEqual(p.wanted,(0,-1),p.idx)

    def test_keyboard_does_not_steer_bot(self):
        bot=self.app.match.players[7];bot.bot=True;bot.joined=False;bot.wanted=(-1,0)
        self.key(game.KEYS[7][3],True);self.key(game.KEYS[7][0],True)
        self.assertEqual(bot.wanted,(-1,0))

    def test_key_repeat_cannot_steal_newer_held_turn(self):
        p=self.app.match.players[0]
        up=game.KEYS[0][3];right=game.KEYS[0][0]
        self.key(up,True);self.key(right,True)
        self.key(up,True)  # A repeated KEYDOWN is not a new physical press.
        self.assertEqual(p.wanted,(1,0))

    def test_fresh_turn_reaches_simulation_at_next_step_all_maps(self):
        for theme in range(4):
            self.app.theme=theme;self.app.start();p=self.app.match.players[0]
            for q in self.app.match.players[1:]:q.lives=0
            self.app.match.foes=[];self.app.match.items={}
            p.pos=(10,1);p.entry=0
            p.clock=self.app.match.tuning['player_step_seconds']-1/120
            p.direction=(-1,0)
            self.held.clear()
            self.key(game.KEYS[0][3],True);self.key(game.KEYS[0][0],True)
            self.app.match.update(1/60)
            self.assertEqual(p.pos,(11,1),theme)


class ContactResponse(unittest.TestCase):
    def test_illegal_turn_stays_buffered_until_junction_all_maps(self):
        for theme in range(4):
            g=game.Match(1,theme,seed=7);g.foes=[];g.items={}
            x=next(x for x in range(3,55) if (x,2) in g.arena.lanes and
                   (x-1,2) not in g.arena.lanes and (x-1,1) in g.arena.lanes)
            p=g.players[0];p.pos=(x-1,1);p.entry=0
            p.clock=g.tuning['player_step_seconds']-1/60
            p.direction=(1,0);p.wanted=(0,1)
            g.update(1/60)
            self.assertEqual(p.pos,(x,1));self.assertEqual(p.wanted,(0,1))
            g.update(1/60)
            self.assertEqual(p.direction,(0,1));self.assertEqual(p.pos,(x,1))

    def test_immediate_facing_does_not_override_slick_or_recoil(self):
        for mode in ('Slick','recoil'):
            g=game.Match(1,0,seed=7);g.foes=[];g.items={}
            p=g.players[0];p.pos=(20,1);p.entry=p.clock=0
            p.direction=(1,0);p.wanted=(-1,0)
            if mode=='Slick':p.effects['Slick']=1
            else:p.recoil=(1,0)
            g.update(1/60)
            self.assertEqual(p.direction,(1,0),mode)
            self.assertEqual(p.pos,(20,1))

    def test_legal_reversal_faces_immediately_without_free_step(self):
        g=game.Match(1,0,seed=7);g.foes=[];g.items={}
        p=g.players[0];p.pos=(20,1);p.entry=p.clock=0
        p.direction=(1,0);p.wanted=(-1,0)
        g.update(1/60)
        self.assertEqual(p.direction,(-1,0))
        self.assertEqual(p.pos,(20,1))
        self.assertAlmostEqual(p.clock,1/60)

    def test_turn_position_response_respects_remaining_cadence(self):
        for fraction in (0.,.2,.8,.99):
            g=game.Match(1,0,seed=7);g.foes=[];g.items={}
            p=g.players[0];p.pos=(20,1);p.entry=0
            interval=g.tuning['player_step_seconds']
            p.clock=interval*fraction;p.direction=(1,0);p.wanted=(-1,0)
            elapsed=0.
            while p.pos==(20,1) and elapsed<interval+1/60:
                g.update(1/60);elapsed+=1/60
            self.assertEqual(p.pos,(19,1))
            self.assertGreaterEqual(elapsed+1e-9,interval*(1-fraction))
            self.assertLessEqual(elapsed,interval*(1-fraction)+1/60+1e-9)

    def test_repeated_reversals_cannot_grant_extra_movement_steps(self):
        g=game.Match(1,0,seed=7);g.foes=[];g.items={}
        p=g.players[0];p.pos=(20,1);p.entry=p.clock=0
        moved=0
        for tick in range(120):
            p.wanted=(1 if tick%2 else -1,0)
            before=p.pos;g.update(1/60);moved+=game.distance(before,p.pos)
        self.assertEqual(moved,int((2.+1e-9)/g.tuning['player_step_seconds']))

    def test_cadence_and_buffered_controls_match_30_60_144_frame_rates(self):
        app=game.App(simulate_controllers=True)
        try:
            app.cabinet.settings.update(free_play=True,fill_bots=False)
            for count in (1,2,8):
                for theme in range(4):
                    outcomes=[]
                    for rate in (30,60,144):
                        app.count=count;app.theme=theme;app.start();g=app.match
                        g.foes=[];g.items={}
                        for i,p in enumerate(g.players):
                            p.pos=(4+i*5,1);p.entry=p.clock=0;p.direction=p.wanted=(1,0)
                        for _ in range(rate):app.advance(1/rate)
                        outcomes.append([(p.pos,p.score,p.wanted) for p in g.players])
                    self.assertEqual(outcomes[0],outcomes[1],(count,theme))
                    self.assertEqual(outcomes[1],outcomes[2],(count,theme))
                    steps=int((1.+1e-9)/g.tuning['player_step_seconds'])
                    self.assertEqual(outcomes[0][0][0],(4+steps,1))
        finally:game.pg.quit()

    def test_all_maps_one_two_eight_recover_when_controls_turn_same_way(self):
        for theme in range(4):
            for count in (1,2,8):
                g=game.Match(count,theme,seed=6,tuning={'spawn_seconds':120})
                g.foes=[];g.items={}
                for i,p in enumerate(g.players):
                    p.pos=(7+i*3,1);p.entry=p.safe=p.clock=0
                    p.direction=p.wanted=(1 if i<count/2 else -1,0)
                for _ in range(round(10*g.tuning['player_step_seconds']*60)):g.update(1/60)
                before=[p.pos for p in g.players]
                for p in g.players:p.wanted=(1,0)
                for _ in range(round(20*g.tuning['player_step_seconds']*60)):
                    previous=[p.pos for p in g.players];g.update(1/60)
                    self.assertEqual(len({p.pos for p in g.players}),count)
                    self.assertTrue(all(game.distance(p.pos,old)<=1 for p,old in zip(g.players,previous)))
                self.assertTrue(all(p.pos[0]>old[0] for p,old in zip(g.players,before)),(theme,count))
                self.assertTrue(all(p.lives==3 for p in g.players))


if __name__=='__main__':unittest.main(verbosity=2)
