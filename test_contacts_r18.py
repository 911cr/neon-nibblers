"""Power/contact boundary and actual rendered-response regressions."""
import os
os.environ['SDL_VIDEODRIVER']='dummy'
os.environ['SDL_AUDIODRIVER']='dummy'
import unittest
from unittest.mock import patch
import game
from replay import digest
from gate_art import gate_geometry


def carried_fixture(holder=1,lives=1):
    g=game.Match(2,0,seed=18);burner=g.players[1-holder];owner=g.players[holder]
    g.items={}
    for p in g.players:
        p.entry=p.safe=p.clock=0;p.direction=p.wanted=(1,0)
    burner.pos=(10,1);owner.pos=(12,1)
    burner.effects={'Flare':2};owner.effects={'Lure':2};owner.lives=lives
    g.foes=[(13,1)];g.foe_modes=['carried'];g.foe_carriers={0:holder}
    g.foe_previous=list(g.foes);g.foe_release=[0];g.foe_zapped=[0];g.foe_ticks=[0]
    return g,burner,owner


class PowerContactQA(unittest.TestCase):
    def test_fire_stops_at_actual_walls_all_maps(self):
        for theme in range(4):
            g=game.Match(2,theme,seed=18);p,q=g.players
            start,target=next((c,(c[0]+offset,c[1])) for c in sorted(g.arena.lanes)
                if g.arena.step(c,(1,0)) not in g.arena.lanes
                for offset in range(2,6) if (c[0]+offset,c[1]) in g.arena.lanes)
            p.pos=start;q.pos=target;p.direction=(1,0);p.effects={'Flare':2}
            p.safe=q.safe=0
            self.assertEqual(g.fire_cells(p),[])
            g.apply_fire()
            self.assertEqual(q.lives,3);self.assertEqual(p.score,0)

    def test_two_emitters_cannot_damage_shared_victim_twice(self):
        g=game.Match(3,0,seed=18);g.foes=[];g.items={}
        for i,p in enumerate(g.players):
            p.pos=((10,14,12)[i],1);p.entry=p.safe=p.clock=0
            p.direction=p.wanted=(1 if i==0 else -1,0)
            p.effects={'Flare':2} if i<2 else {}
        g.apply_fire()
        self.assertEqual([p.lives for p in g.players],[2,2,2])
        self.assertEqual(sum(e['event']=='player_hurt' and e['player_id']==3 for e in g.ledger.events),1)
        self.assertEqual(sum(p.score for p in g.players),3*g.score_values['rival_burned'])

    def test_mutual_flames_trade_damage_without_station_order_bias(self):
        for theme in range(4):
            for reverse in (False,True):
                for lives in (1,3):
                    g=game.Match(2,theme,seed=18);g.foes=[];g.items={}
                    for i,p in enumerate(g.players):
                        left=(i==0)!=reverse
                        p.pos=(10 if left else 14,1)
                        p.direction=p.wanted=(1 if left else -1,0)
                        p.entry=p.safe=p.clock=0;p.effects={'Flare':2};p.lives=lives
                    origins={p.idx+1:list(p.pos) for p in g.players}
                    g.update(1/60)
                    self.assertEqual([p.lives for p in g.players],[lives-1]*2,(theme,reverse,lives))
                    self.assertEqual([p.score for p in g.players],[g.score_values['rival_burned']]*2)
                    self.assertEqual(sum(e['event']=='player_hurt' for e in g.ledger.events),2)
                    self.assertEqual(sum(e['event']=='rival_burned' for e in g.ledger.events),2)
                    for event in g.ledger.events:
                        if event['event']=='rival_burned':
                            self.assertEqual(event['context']['position'],origins[event['player_id']])

    def test_fire_keeps_immunity_and_ghost_house_exclusions(self):
        for protection in ('safe','Titan'):
            g,burner,owner=carried_fixture()
            g.foe_carriers={};g.foe_modes=['house'];g.foes=[(11,1)]
            owner.effects={};owner.lives=3
            if protection=='safe':owner.safe=1
            else:owner.effects={'Titan':1}
            g.apply_fire()
            self.assertEqual(owner.lives,3)
            self.assertEqual(g.foe_modes,['house'])
            self.assertEqual(burner.score,0)

    def test_direct_hurt_releases_all_owned_ghosts_immediately(self):
        for lives in (1,3):
            g,_,owner=carried_fixture(lives=lives)
            g.foes=[(13,1),(14,1),(15,1)];g.foe_modes=['carried']*3
            g.foe_carriers={i:owner.idx for i in range(3)}
            g.foe_release=[0]*3
            self.assertTrue(g.hurt(owner))
            self.assertEqual(g.foe_carriers,{})
            self.assertEqual(g.foe_modes,['eyes']*3)
            self.assertEqual(owner.lives,lives-1)

    def test_fire_releases_holder_ghosts_in_same_tick_both_player_orders(self):
        for holder in (0,1):
            g,burner,owner=carried_fixture(holder)
            g.update(1/60)
            self.assertEqual(owner.lives,0)
            self.assertEqual(g.foe_carriers,{})
            self.assertEqual(g.foe_modes,['eyes'])
            self.assertEqual(burner.score,g.score_values['rival_burned'])
            self.assertEqual(sum(e['event']=='player_hurt' for e in g.ledger.events),1)

    def test_expiry_and_same_tick_refresh_precede_ghost_contact_all_maps(self):
        for theme in range(4):
            for power in ('Crown','Titan'):
                for refresh in (False,True):
                    g=game.Match(1,theme,seed=18);p=g.players[0]
                    p.pos=(10,1);p.entry=p.safe=p.clock=0;p.effects={power:1/60}
                    g.items={p.pos:power} if refresh else {}
                    g.foes=[p.pos];g.foe_modes=['roaming'];g.foe_previous=[p.pos]
                    g.foe_release=[0];g.foe_zapped=[0];g.foe_ticks=[0]
                    g.update(1/60)
                    self.assertEqual(p.lives,3 if refresh else 2,(theme,power,refresh))
                    self.assertEqual(g.foe_modes[0],'eyes' if refresh else 'roaming')
                    self.assertEqual(sum(e['event']=='ghost_eaten' for e in g.ledger.events),int(refresh))

    def test_lure_expiry_releases_before_weapon_contact(self):
        g,_,owner=carried_fixture(lives=3)
        owner.effects={'Lure':1/60}
        victim=g.players[1-owner.idx];victim.effects={};victim.pos=(13,1)
        g.update(1/60)
        self.assertEqual(victim.lives,3)
        self.assertEqual(g.foe_carriers,{})
        self.assertEqual(g.foe_modes,['eyes'])


class RenderContactQA(unittest.TestCase):
    def test_powered_bay_entry_and_return_attach_only_inside_owner_pocket(self):
        app=game.App(simulate_controllers=True)
        try:
            app.count=8
            for theme in range(4):
                for returning in (False,True):
                    app.theme=theme;app.start();g=app.match;g.foes=[];g.items={}
                    for p in g.players:
                        spawn=g.arena.spawns[p.idx];inward=(0,1) if spawn[1]==0 else (0,-1)
                        p.pos=g.arena.entries[p.idx] if returning else spawn
                        p.direction=p.wanted=(-inward[0],-inward[1]) if returning else inward
                        p.entry=p.safe=0;p.clock=g.player_interval(p)-1/60;p.effects={'Flare':2}
                    app.reset_visuals();app.draw(0)
                    app.advance(1/60);app.draw(1/60)
                    for p in g.players:
                        spawn=g.arena.spawns[p.idx]
                        p.wanted=((0,1) if spawn[1]==0 else (0,-1)) if returning else (1,0)
                    app.advance(1/60)
                    calls=[];original=game.fire_plume
                    def capture(surface,start,end,direction,time):
                        calls.append((tuple(start),tuple(end),surface.get_clip().copy()))
                        return original(surface,start,end,direction,time)
                    before=digest(g)
                    with patch.object(game,'fire_plume',capture):app.draw(1/60)
                    self.assertEqual(digest(g),before)
                    board=game.pg.Rect(game.OX,game.TOP,game.COLS*game.TILE,game.ROWS*game.TILE)
                    for p in g.players:
                        visual=app.visual_positions[p.idx]
                        attached=[c for c in calls if game.distance(c[0],visual)<=1.5]
                        self.assertTrue(attached,(theme,returning,p.idx,visual))
                        spawn=g.arena.spawns[p.idx];upper=spawn[1]==0
                        mouth=game.TOP+4 if upper else game.TOP+game.ROWS*game.TILE-4
                        pocket=gate_geometry(game.center(spawn)[0],mouth,upper)['outer']
                        self.assertTrue(any(pocket.contains(c[2]) for c in attached),(theme,returning,p.idx))
                        for start,end,clip in attached:
                            self.assertTrue(board.contains(clip) or pocket.contains(clip))
                            self.assertAlmostEqual(start[0],end[0])
        finally:game.pg.quit()

    def test_flame_starts_at_visible_actor_and_keeps_corner_path(self):
        app=game.App(simulate_controllers=True)
        try:
            app.count=1;app.cabinet.settings['fill_bots']=False
            for theme in range(4):
                app.theme=theme;app.start();g=app.match;p=g.players[0]
                g.foes=[];g.items={}
                x=next(x for x in range(3,55) if (x,2) in g.arena.lanes and
                       (x-1,2) not in g.arena.lanes and (x-1,1) in g.arena.lanes)
                p.pos=(x-1,1);p.entry=0;p.clock=g.player_interval(p)-1/60
                p.direction=(1,0);p.wanted=(0,1);p.effects={'Flare':2}
                app.reset_visuals();app.draw(0)
                app.advance(1/60);app.draw(1/60)
                app.advance(1/60)
                with patch.object(game,'fire_plume',wraps=game.fire_plume) as fire:app.draw(1/60)
                segments=[call.args[1:3] for call in fire.call_args_list]
                self.assertTrue(segments)
                self.assertLessEqual(game.distance(segments[0][0],app.visual_positions[0]),1.5)
                for start,end in segments:
                    self.assertTrue(abs(start[0]-end[0])<1e-6 or abs(start[1]-end[1])<1e-6)
                for left,right in zip(segments,segments[1:]):
                    self.assertLessEqual(game.distance(left[1],right[0]),1.5)
        finally:game.pg.quit()

    def test_same_tick_owner_death_renders_returning_eyes(self):
        app=game.App(simulate_controllers=True)
        try:
            app.count=2;app.start();g,_,_=carried_fixture()
            app.match=g;app.reset_visuals();g.update(1/60)
            before=digest(g)
            with patch.object(game,'foe',wraps=game.foe) as draw:app.draw(1/60)
            self.assertTrue(draw.call_args_list)
            self.assertTrue(draw.call_args_list[0].args[7])
            self.assertEqual(digest(g),before)
        finally:game.pg.quit()

    def test_continuous_contacts_all_maps_one_two_eight_do_not_visual_jump(self):
        app=game.App(simulate_controllers=True)
        try:
            app.cabinet.settings.update(free_play=True,fill_bots=False)
            for theme in range(4):
                for count in (1,2,8):
                    app.theme=theme;app.count=count;app.start();g=app.match
                    g.foes=[];g.items={}
                    for i,p in enumerate(g.players):
                        p.pos=(7+i*3,1);p.entry=p.safe=p.clock=0
                        p.direction=p.wanted=(1 if i<count/2 else -1,0)
                    app.draw(0)
                    for _ in range(120):
                        previous=dict(app.visual_positions)
                        app.advance(1/60);before=digest(g);app.draw(1/60)
                        self.assertEqual(digest(g),before)
                        self.assertEqual(len({p.pos for p in g.players}),count)
                        for p in g.players:
                            delta=game.distance(previous[p.idx],app.visual_positions[p.idx])
                            self.assertLessEqual(delta,game.TILE/g.player_interval(p)/60+1e-6,(theme,count,p.idx))
        finally:game.pg.quit()


if __name__=='__main__':unittest.main(verbosity=2)
