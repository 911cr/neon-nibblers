"""Adversarial event/account and power timing checks; tuning is original."""
import os
os.environ['SDL_VIDEODRIVER']='dummy'
os.environ['SDL_AUDIODRIVER']='dummy'
import unittest
from unittest.mock import patch
import game
from cabinet import spectator_view
from replay import FixedStepper,digest

class Interactions(unittest.TestCase):
    def test_takeover_resets_current_ledger_account_but_retains_history(self):
        g=game.Match(1,seed=123);g.fill_vacancies()
        g.collect(g.players[7],'Rush')
        old_event=g.ledger.events[-1].copy()
        self.assertEqual(g.ledger.totals()[8],75)
        self.assertTrue(g.join_station(7))
        self.assertEqual(g.ledger.totals()[8],0)
        g.award(g.players[7],'dot')
        self.assertEqual(g.ledger.totals()[8],g.players[7].score)
        self.assertIn(old_event,g.ledger.events)
        self.assertTrue(all(event['delta']>=0 for event in g.ledger.events))
        self.assertEqual(next(row['score'] for row in spectator_view(g,'playing')['ranking'] if row['player_id']==8),10)

    def test_same_tick_dot_power_ghost_rival_and_bonus_count_once(self):
        for theme in range(4):
            g=game.Match(2,theme,seed=91,rules={'bonus_threshold':500})
            start=next(c for c in sorted(g.arena.lanes) if g.arena.step(c,(1,0)) in g.arena.lanes)
            target=g.arena.step(start,(1,0));p,q=g.players
            p.pos=start;p.entry=p.safe=0;p.direction=p.wanted=(1,0);p.clock=g.tuning['player_step_seconds']-1/60
            q.pos=target;q.entry=q.safe=0;q.stun=10
            g.items={target:'Titan'};g.dots={target,max(g.arena.lanes)}
            g.foes=[target];g.foe_modes=['roaming'];g.foe_release=[0];g.foe_ticks=[0];g.foe_zapped=[0]
            g.update(1/60)
            events=[e for e in g.ledger.events if e['tick']==1]
            for name in ('dot','pickup','ghost_eaten','rival_eaten','score_bonus_life'):
                self.assertEqual(sum(e['event']==name for e in events),1,(theme,name,events))
            self.assertEqual(p.score,1510)
            self.assertEqual((p.lives,q.lives),(4,2))
            self.assertEqual(g.ledger.totals()[1],p.score)
            for _ in range(3):g.update(1/60)
            self.assertEqual(sum(e['event']=='ghost_eaten' for e in g.ledger.events),1)
            self.assertEqual(sum(e['event']=='rival_eaten' for e in g.ledger.events),1)

    def test_all_timed_personal_effects_expire_at_same_logic_tick_30_60(self):
        for power in ('Rush','Slick','Flare','Crown','Titan','Veil','Mist','Lure'):
            runs=[]
            for hz in (30,60):
                g=game.Match(1,seed=7);g.items={};g.foes=[]
                p=g.players[0];p.stun=100
                g.collect(p,power);duration=p.effects[power]
                stepper=FixedStepper(g)
                for _ in range(round(duration*hz)):stepper.advance(1/hz)
                self.assertNotIn(power,p.effects)
                self.assertEqual(g.tick,round(duration*60))
                runs.append(digest(g))
            self.assertEqual(*runs,power)

    def test_no_duplicate_fire_credit_for_multiple_attackers(self):
        for theme in range(4):
            g=game.Match(3,theme,seed=8);p,q,r=g.players
            c=next(c for c in sorted(g.arena.lanes) if all(g.arena.step(c,(d,0)) in g.arena.lanes for d in (-1,1)))
            p.pos=g.arena.step(c,(-1,0));q.pos=g.arena.step(c,(1,0));r.pos=c
            p.direction=(1,0);q.direction=(-1,0)
            p.effects=q.effects={'Flare':3};p.safe=q.safe=3;r.safe=0
            g.foes=[c];g.foe_modes=['roaming'];g.foe_release=[0]
            g.apply_fire()
            self.assertEqual(r.lives,2)
            self.assertEqual(sum(e['event']=='rival_burned' for e in g.ledger.events),1)
            self.assertEqual(sum(e['event']=='ghost_burned' for e in g.ledger.events),1)

    def test_lure_expiry_releases_weapon_before_same_tick_contact(self):
        g=game.Match(2,seed=4);p,q=g.players
        cell=next(iter(g.arena.lanes));p.effects={'Lure':1/60}
        q.pos=cell;q.safe=q.entry=0;q.stun=10
        g.foes=[cell];g.foe_modes=['carried'];g.foe_carriers={0:0}
        g.foe_release=[0];g.foe_ticks=[0];g.foe_zapped=[0];g.items={}
        g.update(1/60)
        self.assertEqual(g.foe_modes[0],'eyes')
        self.assertEqual(g.foe_carriers,{})
        self.assertEqual(q.lives,3)
        self.assertFalse(any(e['event']=='carried_ghost_hit' for e in g.ledger.events))

    def test_crown_expiry_and_damage_produce_one_death_event(self):
        g=game.Match(1,seed=4);p=g.players[0]
        cell=next(iter(g.arena.lanes));p.pos=cell;p.safe=p.entry=0;p.stun=10
        p.effects={'Crown':1/60};g.items={}
        g.foes=[cell,cell];g.foe_modes=['roaming']*2
        g.foe_release=[0]*2;g.foe_ticks=[0]*2;g.foe_zapped=[0]*2
        sounds=g.update(1/60)
        self.assertEqual(p.lives,2)
        deaths=[e for e in g.ledger.events if e['event']=='player_hurt']
        self.assertEqual(len(deaths),1)
        self.assertEqual(deaths[0]['context']['position'],list(cell))
        self.assertEqual(sounds.count('hurt'),1)
        self.assertEqual(p.score,0)

    def test_hud_and_spectator_show_new_human_account_after_bot_takeover(self):
        app=game.App(simulate_controllers=True)
        try:
            app.cabinet.settings.update(fill_bots=True,free_play=True)
            app.count=1;app.start();g=app.match
            g.collect(g.players[7],'Rush');app.draw(0)
            app.station_action(7);g.award(g.players[7],'dot')
            calls=[];original=game.arcade_digits
            def capture(surface,label,x,y,color,scale=3):
                calls.append((str(label),x,y));return original(surface,label,x,y,color,scale)
            with patch.object(game,'arcade_digits',capture):app.draw(0)
            hud=game.station_hud(g.arena.spawns[7],10)
            self.assertIn(('10',hud['x'],hud['y']),calls)
            row=next(r for r in spectator_view(g,'playing')['ranking'] if r['player_id']==8)
            self.assertEqual(row['score'],g.ledger.totals()[8])
        finally:game.pg.quit()

class NavigationQA(unittest.TestCase):
    def test_threat_distances_follow_tunnels_and_do_not_cross_walls(self):
        from arcade_ai import threat_distances
        for theme in range(4):
            arena=game.Arena(theme)
            for row in arena.portals:
                distances=threat_distances(arena,{(0,row)})
                self.assertEqual(distances[(game.COLS-1,row)],1)
        # A U corridor isolates graph distance from visual/Manhattan proximity.
        # Endpoints are two cells apart but six legal steps apart; the middle
        # cell is a wall. This avoids assuming a specific decorative map gap.
        from types import SimpleNamespace
        lanes={(0,0),(0,1),(0,2),(1,2),(2,2),(2,1),(2,0)}
        arena=SimpleNamespace(lanes=lanes,step=game.add)
        distances=threat_distances(arena,{(0,0)})
        self.assertEqual(distances[(1,2)],3)
        self.assertNotIn((2,0),distances)
        self.assertNotIn((1,0),distances)

    def test_ai_avoids_ghost_and_crown_does_not_ignore_giant_rival(self):
        from arcade_ai import choose_direction,DIRECTIONS
        for theme in range(4):
            for threat in ('ghost','giant'):
                g=game.Match(2,theme,seed=1);p,q=g.players
                c=next(c for c in sorted(g.arena.lanes) if all(g.arena.step(c,(d,0)) in g.arena.lanes for d in (-1,1)))
                left=g.arena.step(c,(-1,0));right=g.arena.step(c,(1,0))
                p.pos=c;p.safe=0;g.items={};g.dots={left,right}
                if threat=='ghost':
                    g.foes=[left];g.foe_modes=['roaming'];q.lives=0
                else:
                    g.foes=[];g.foe_modes=[];q.pos=left;q.effects={'Titan':5};p.effects={'Crown':5}
                self.assertEqual(choose_direction(g,p,DIRECTIONS),(1,0))

    def test_bot_only_choices_legal_and_deterministic_all_maps(self):
        for theme in range(4):
            outcomes=[]
            for _ in range(2):
                g=game.Match(1,theme,seed=234);g.fill_vacancies()
                human=g.players[0];human.wanted=(0,1)
                for frame in range(60):
                    before=human.wanted
                    game.steer_demo(g,only_bots=True)
                    self.assertEqual(human.wanted,before)
                    for p in g.players:
                        if p.bot and p.lives>0:
                            self.assertTrue(g.arena.can_enter(g.arena.step(p.pos,p.wanted),p),(theme,frame,p))
                    g.update(1/60)
                outcomes.append(digest(g))
            self.assertEqual(*outcomes)

    def test_station_start_honors_same_tuning_as_quick_start(self):
        from gameplay_tuning import validate_tuning
        app=game.App(simulate_controllers=True)
        try:
            app.cabinet.settings.update(fill_bots=False,free_play=True)
            app.tuning=validate_tuning({'durations':{'Rush':11},'spawn_seconds':9})
            app.station_action(7)
            self.assertEqual(app.match.tuning,app.tuning)
            app.match.collect(app.match.players[7],'Rush')
            self.assertEqual(app.match.players[7].effects['Rush'],11)
        finally:game.pg.quit()

class FinalIntegrationQA(unittest.TestCase):
    def test_tuning_malformed_types_and_rule_zero_are_not_coerced(self):
        from gameplay_tuning import validate_tuning
        from cabinet import CabinetStore
        import math
        for value in (True,False,'0',0.,-1,1,29,None,math.inf):
            with self.subTest(value=value),self.assertRaises(ValueError):
                CabinetStore.validate({'match_seconds':value})
        self.assertEqual(CabinetStore.validate({'match_seconds':0})['match_seconds'],0)
        for key in ('spawn_seconds','quake_multiplier','spark_radius','max_items'):
            for value in (True,False,'1',None,math.inf,math.nan):
                with self.subTest(key=key,value=value),self.assertRaises(ValueError):
                    validate_tuning({key:value})
        for value in (None,[],True,'7'):
            with self.subTest(duration=value),self.assertRaises(ValueError):
                validate_tuning({'durations':value})

    def test_carried_ghost_risk_requires_live_other_owner_with_lure(self):
        from arcade_ai import choose_direction
        directions=((-1,0),(1,0),(0,1),(0,-1))
        for theme in range(4):
            for state in ('own','rival','dead','expired'):
                g=game.Match(2,theme,seed=11);p,q=g.players
                c=next(c for c in sorted(g.arena.lanes) if all(g.arena.step(c,(d,0)) in g.arena.lanes for d in (-1,1)))
                left=g.arena.step(c,(-1,0));right=g.arena.step(c,(1,0))
                p.pos=c;p.safe=0;g.items={};g.dots={left,right}
                g.foes=[left];g.foe_modes=['carried'];g.foe_carriers={0:0 if state=='own' else 1}
                owner=p if state=='own' else q;owner.effects={'Lure':2}
                if state=='dead':owner.lives=0
                if state=='expired':owner.effects={}
                self.assertEqual(choose_direction(g,p,directions),(1,0) if state=='rival' else (-1,0),(theme,state))

    def test_untimed_pause_guide_and_end_do_not_age_tuned_effects(self):
        from gameplay_tuning import validate_tuning
        app=game.App(simulate_controllers=True)
        try:
            app.cabinet.settings.update(fill_bots=False,free_play=True)
            app.untimed=True;app.tuning=validate_tuning({'durations':{'Rush':.5}})
            app.count=1;app.start();g=app.match;p=g.players[0]
            g.collect(p,'Rush')
            for state in ('pause','guide'):
                g.paused=state=='pause';app.help=state=='guide'
                before=digest(g);app.advance(4);app.draw(.5)
                self.assertEqual(digest(g),before)
                self.assertEqual(app.fixed_accumulator,0)
            g.paused=False;app.help=False
            for _ in range(30):app.advance(1/60)
            self.assertNotIn('Rush',p.effects)
            self.assertEqual(g.time,0);self.assertFalse(g.over)
            p.lives=0;app.advance(1/60);self.assertTrue(g.over)
            before=digest(g);app.advance(10);app.draw(.5)
            self.assertEqual(digest(g),before)
            self.assertEqual(g.ledger.events[-1]['context']['reason'],'elimination')
        finally:game.pg.quit()

if __name__=='__main__':unittest.main(verbosity=2)
