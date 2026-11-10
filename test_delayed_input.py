import os,unittest
from collections import defaultdict
from unittest.mock import patch
os.environ['SDL_VIDEODRIVER']='dummy';os.environ['SDL_AUDIODRIVER']='dummy'
import game

class DelayedInput(unittest.TestCase):
    def setUp(self):
        self.app=game.App(simulate_controllers=True)
        self.app.cabinet.settings.update(fill_bots=False,free_play=True)
        self.app.count=2;self.app.start();self.g=self.app.match
        self.g.foes=[];self.g.items={}
        self.held=defaultdict(bool)
        self.junctions=[x for x in range(3,55) if (x,2) in self.g.arena.lanes]
        for p,x in zip(self.g.players,(self.junctions[0],self.junctions[-1])):
            p.pos=(x,1);p.entry=0;p.clock=0;p.wanted=p.direction=(1,0)
            self.held[game.KEYS[p.idx][0]]=True
    def tearDown(self):game.pg.quit()
    def batch(self,events,dt):
        for kind,key in events:
            game.pg.event.post(game.pg.event.Event(kind,key=key,mod=0))
        self.app.events()
        with patch.object(game.pg.key,'get_pressed',return_value=self.held):self.app.inputs()
        self.app.advance(dt)
    def test_two_same_frame_taps_survive_an_older_held_key(self):
        origins=[p.pos for p in self.g.players];events=[]
        for p in self.g.players:
            key=game.KEYS[p.idx][2]
            events.extend([(game.pg.KEYDOWN,key),(game.pg.KEYUP,key)])
        self.batch(events,.1) # Six ticks elapse but no movement step is due yet.
        self.batch([], .1)
        self.assertEqual([p.pos for p in self.g.players],[(x,y+1) for x,y in origins])
    def test_tap_before_blocked_junction_persists_until_legal(self):
        p=self.g.players[0];x=next(x for x in self.junctions if (x-1,2) not in self.g.arena.lanes)
        p.pos=(x-1,1);k=game.KEYS[0][2]
        self.batch([(game.pg.KEYDOWN,k),(game.pg.KEYUP,k)],.2)
        self.assertEqual(p.pos,(x,1))
        self.batch([],.15)
        self.assertEqual(p.pos,(x,2))

    def test_real_event_loop_with_a_delayed_render(self):
        # Hold the original key while a complete tap waits in the SDL queue.
        origins=[p.pos for p in self.g.players]
        draw=self.app.draw
        frames=[]
        def slow_first_frame(dt):
            draw(dt)
            frames.append(dt)
            if len(frames)==1:
                for p,origin in zip(self.g.players,origins):
                    p.pos=origin;p.clock=0
                    key=game.KEYS[p.idx][2]
                    for kind in (game.pg.KEYDOWN,game.pg.KEYUP):
                        game.pg.event.post(game.pg.event.Event(kind,key=key,mod=0))
                game.pg.time.wait(185)
        with patch.object(self.app,'draw',side_effect=slow_first_frame), \
             patch.object(game.pg.key,'get_pressed',return_value=self.held):
            self.app.run(frames=2)
        self.assertGreaterEqual(frames[1],.18)
        self.assertEqual([p.pos for p in self.g.players],[(x,y+1) for x,y in origins])

    def test_newer_press_can_cancel_an_unconsumed_turn(self):
        p=self.g.players[0];x,y=p.pos
        down,left=game.KEYS[0][2],game.KEYS[0][1]
        self.batch([(game.pg.KEYDOWN,down),(game.pg.KEYUP,down)],.05)
        self.batch([(game.pg.KEYDOWN,left),(game.pg.KEYUP,left)],.12)
        self.assertEqual(p.pos,(x-1,y))
