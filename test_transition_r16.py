"""Continuous stage transitions: preserved progress, legal deterministic relocation."""
import copy
import os
os.environ['SDL_VIDEODRIVER']='dummy'
os.environ['SDL_AUDIODRIVER']='dummy'
import unittest
from unittest.mock import patch
import game
from replay import digest


class TransitionQA(unittest.TestCase):
    def test_displaced_moving_item_does_not_move_legal_static_pellet(self):
        g=game.Match(1,0,seed=4)
        g.items={(0,17):'Heart',(1,17):'Crown'}
        g.item_directions={(0,17):(1,0),(1,17):None}
        self.assertTrue(set(g.items)<=g.arena.lanes)
        self.assertIn((1,17),game.Arena(2).lanes)
        g.transition_arena(2)
        self.assertEqual(g.items.get((1,17)),'Crown')
        self.assertCountEqual(g.items.values(),['Heart','Crown'])
        self.assertTrue(set(g.items)<=g.arena.lanes)
        heart=next(c for c,n in g.items.items() if n=='Heart')
        self.assertEqual(g.item_directions[heart],(1,0))

    def test_all_sixteen_pairs_preserve_valid_actors_and_progress(self):
        for old in range(4):
            for new in range(4):
                g=game.Match(8,old,seed=91,continue_seconds=10)
                common=sorted(g.arena.lanes & game.Arena(new).lanes)
                for i,p in enumerate(g.players):
                    p.pos=common[i*7];p.entry=0;p.score=1000+i;p.lives=2
                    p.effects={'Titan':2.3,'Lure':4.2};p.safe=.4;p.stun=.2
                    p.wanted=(1,0);p.direction=(0,1);p.bonus_life=True
                before=[copy.deepcopy(vars(p)) for p in g.players]
                g.transition_arena(new)
                self.assertEqual([vars(p) for p in g.players],before,(old,new))
                self.assertEqual(g.arena.theme,new)
                self.assertEqual(g.dots,set())
                self.assertEqual(set(g.refill_pending),g.arena.lanes-set(g.arena.entries))

    def test_displaced_actor_cannot_steal_valid_later_actor_cell(self):
        exercised=0
        for old in range(4):
            for new in range(4):
                g=game.Match(8,old,seed=23)
                target=game.Arena(new)
                removed=sorted(g.arena.lanes-target.lanes)
                if not removed:continue
                invalid=removed[0]
                valid=min(g.arena.lanes & target.lanes,key=lambda c:(game.distance(c,invalid),c))
                others=sorted((g.arena.lanes & target.lanes)-{valid})
                for p,c in zip(g.players,others):p.pos=c;p.entry=0
                g.players[0].pos=invalid;g.players[7].pos=valid
                before=[p.pos for p in g.players]
                clone=copy.deepcopy(g)
                g.transition_arena(new);clone.transition_arena(new)
                after=[p.pos for p in g.players]
                self.assertEqual(after,[p.pos for p in clone.players])
                self.assertEqual(after[1:],before[1:])
                self.assertEqual(len(set(after)),8)
                self.assertTrue(all(c in target.lanes for c in after))
                exercised+=1
        self.assertGreater(exercised,0)

    def test_bays_dead_slots_and_continue_timers_survive(self):
        for old in range(4):
            for new in range(4):
                g=game.Match(2,old,seed=19,continue_seconds=10,continue_delay=1)
                g.join_station(7)
                g.players[0].entry=.35
                p=g.players[1];p.lives=1;p.safe=0;g.hurt(p)
                g.continues.advance(.4)
                before=copy.deepcopy(g.continues.snapshot())
                g.transition_arena(new)
                self.assertEqual(g.continues.snapshot(),before)
                self.assertEqual(g.players[0].pos,g.arena.spawns[0])
                self.assertEqual(g.players[0].entry,.35)
                self.assertEqual(g.players[1].lives,0)
                self.assertEqual(g.players[1].pos,g.arena.spawns[1])
                self.assertTrue(all(p.lives==0 and not p.joined for p in g.players[2:7]))

    def test_carried_ghost_owner_and_timers_survive_all_pairs(self):
        for old in range(4):
            for new in range(4):
                g=game.Match(1,old,seed=11)
                p=g.players[0];p.pos=next(iter(sorted(g.arena.lanes)));p.entry=0
                p.effects={'Lure':5};p.direction=(1,0)
                g.foe_modes[0]='carried';g.foe_carriers[0]=0
                g.foe_zapped[0]=.75;g.sync_carriers()
                g.transition_arena(new)
                self.assertEqual(g.foe_modes[0],'carried')
                self.assertEqual(g.foe_carriers,{0:0})
                self.assertEqual(g.foe_zapped[0],.75)
                expected=g.arena.step(p.pos,p.direction)
                if expected not in g.arena.lanes:expected=p.pos
                self.assertEqual(g.foes[0],expected)

    def test_ghost_house_return_and_release_progress_remain_reachable(self):
        for old in range(4):
            for new in range(4):
                g=game.Match(0,old,seed=31)
                g.foe_modes=['house','leaving','entering','eyes']
                g.foes=[g.arena.homes[0],g.arena.homes[1],g.arena.exit,g.arena.exit]
                g.foe_release=[.2,.3,.4,.5]
                before=list(g.foe_modes)
                g.transition_arena(new)
                self.assertEqual(g.foe_modes,before)
                self.assertEqual(g.foe_release,[.2,.3,.4,.5])
                for _ in range(150):g.update_foes(.16)
                self.assertEqual(g.foe_modes,['roaming']*4,(old,new,g.foes))
                self.assertTrue(all(c in g.arena.lanes for c in g.foes))

    def test_stage_clear_uses_continuous_transition_without_bonus_reset(self):
        g=game.Match(1,0,seed=9,progression='cycle')
        p=g.players[0];p.pos=(1,1);p.entry=0;p.safe=.7;p.score=800
        p.effects={'Rush':2.,'Veil':3.};p.bonus_life=True
        g.foe_release=[100.]*4;g.items={};g.dots.clear()
        before=copy.deepcopy(vars(p));g.update(0)
        self.assertEqual(g.stage,2)
        self.assertEqual(g.arena.theme,1)
        self.assertEqual(p.pos,before['pos'])
        self.assertEqual(p.effects,before['effects'])
        self.assertEqual(p.safe,before['safe'])
        self.assertEqual(p.score,800+g.score_values['stage_clear'])
        self.assertTrue(p.bonus_life)
        event=next(e for e in reversed(g.ledger.events) if e['event']=='stage_start')
        self.assertTrue(event['context']['actors_preserved'])
        self.assertTrue(g.refill_pending)
        g.update(.01)
        self.assertEqual(g.stage,2)

    def test_refill_is_visible_collectible_together_and_pause_freezes(self):
        g=game.Match(1,0,seed=19)
        g.transition_arena(1);g.foe_release=[100.]*4
        p=g.players[0];p.entry=2.;score=p.score
        pending=copy.deepcopy(g.refill_pending)
        g.paused=True;before=g.snapshot();g.update(.4)
        self.assertEqual(g.snapshot(),before)
        g.paused=False
        for _ in range(55):g.update(.01)
        self.assertFalse(g.dots)
        self.assertEqual(p.score,score)
        for _ in range(55):g.update(.01)
        self.assertFalse(g.refill_pending)
        self.assertEqual(g.dots,set(pending))
        self.assertEqual(g.stage,1)

    def test_actual_transition_render_preserves_logic_hud_and_pause(self):
        app=game.App(simulate_controllers=True)
        try:
            app.count=1;app.theme=0;app.start();g=app.match;p=g.players[0]
            p.pos=(1,1);p.entry=0;p.effects={'Titan':5};p.score=12345
            app.draw(.3)
            g.items={};g.dots.clear();g.foe_release=[100.]*4
            g.update(0)
            old=game.center(p.pos);old=(old[0]-5,old[1])
            app.visual_positions[0]=old
            app.draw(0)
            self.assertEqual(app.visual_positions[0],old)
            locations=[]
            for age in (0.,game.MAZE_TRANSITION_SECONDS/2,game.MAZE_TRANSITION_SECONDS):
                g.transition_age=age
                logic=digest(g)
                with patch.object(game,'arcade_digits',wraps=game.arcade_digits) as digits,patch.object(game,'muncher',wraps=game.muncher) as actor:
                    app.draw(.01)
                self.assertEqual(digest(g),logic)
                calls=[c.args[2:4] for c in digits.call_args_list if c.args[1]==str(p.score)]
                self.assertTrue(calls);locations.append(calls)
                if age==game.MAZE_TRANSITION_SECONDS/2:
                    self.assertTrue(any(c.args[5]>36 for c in actor.call_args_list))
            self.assertTrue(all(x==locations[0] for x in locations))
            g.transition_age=game.MAZE_TRANSITION_SECONDS/2
            for state in ('paused','guide','results'):
                g.paused=state=='paused';app.help=state=='guide';g.over=state=='results'
                app.draw(0)
                pixels=game.pg.image.tobytes(app.canvas,'RGB')
                snapshot=digest(g);animation=app.animation_time
                app.draw(.5)
                self.assertEqual(digest(g),snapshot)
                self.assertEqual(app.animation_time,animation)
                self.assertEqual(game.pg.image.tobytes(app.canvas,'RGB'),pixels,state)
        finally:game.pg.quit()


if __name__=='__main__':unittest.main(verbosity=2)
