"""Headless integration and deterministic rule checks. No controller required."""
import os
os.environ['SDL_VIDEODRIVER']='dummy'
os.environ['SDL_AUDIODRIVER']='dummy'
import unittest
import pygame as pg
from game import Arena, Match, App, ITEMS, DIRS, add, steer_demo

class Smoke(unittest.TestCase):
    def test_all_arenas_connected(self):
        for theme in range(4):
            a=Arena(theme); seen={a.spawns[0]}; todo=list(seen)
            todo=list(seen)
            while todo:
                c=todo.pop()
                for d in DIRS:
                    n=add(c,d)
                    if n in a.floor and n not in seen: seen.add(n); todo.append(n)
            self.assertEqual(seen,a.floor)

    def test_movement_scoring_and_walls(self):
        g=Match(8,seed=1); g.items.clear(); p=g.players[0]; p.pos=(1,1); p.wanted=(1,0)
        g.update(.16)
        self.assertEqual(p.pos,(2,1)); self.assertEqual(p.score,10)
        p.pos=(1,1); p.direction=p.wanted=(-1,0)
        g.update(.16); self.assertEqual(p.pos,(1,1))

    def test_all_eleven_items(self):
        self.assertEqual(len(ITEMS),11)
        for name in ITEMS:
            g=Match(2,seed=4); p,q=g.players; p.safe=q.safe=0
            p.pos=q.pos=(2,1); g.foes=[(2,1)]
            before=p.score; g.collect(p,name)
            self.assertGreaterEqual(p.score,before+75)
            if name=='Heart': self.assertEqual(p.lives,4)
            elif name=='Slick': self.assertEqual(p.effects['Slick'],2)
            elif name=='Spark': self.assertEqual(q.stun,2)
            elif name=='Quake': self.assertEqual(g.quake,5)
            elif name=='Flare': self.assertEqual(p.effects['Flare'],3)
            else: self.assertGreater(p.effects[name],0)

    def test_combat_respawn_and_immunity(self):
        g=Match(2,seed=1); p,q=g.players
        p.pos=q.pos=(2,1); p.safe=q.safe=0; g.foes=[]
        p.effects['Titan']=7
        g.combat(); self.assertEqual(q.lives,2); self.assertEqual(p.score,300)
        g.hurt(q); self.assertEqual(q.lives,2)
        q.safe=0; q.effects['Veil']=7; g.hurt(q); self.assertEqual(q.lives,1)

    def test_stage_and_end(self):
        g=Match(8,seed=1); g.dots.clear(); g.update(.01)
        self.assertEqual(g.stage,2); self.assertTrue(g.dots)
        g.time=.01; g.update(.02); self.assertTrue(g.over)
        g=Match(1); g.players[0].lives=0; g.update(.01); self.assertTrue(g.over)

    def test_long_simulations(self):
        for count in (1,2,4,8):
            for theme in range(4):
                g=Match(count,theme,seed=42)
                for frame in range(3600):
                    if frame%10==0:
                        for p in g.players: p.wanted=g.rng.choice(DIRS)
                    g.update(.05)
                    for p in g.players:
                        self.assertIn(p.pos,g.arena.floor)
                        self.assertGreaterEqual(p.lives,0)

    def test_render_and_lifecycle(self):
        app=App(); app.draw()
        app.count=8; app.start(); app.draw()
        app.help=True; app.draw(); app.help=False
        app.match.paused=True; app.draw()
        app.match.over=True; app.draw()
        app.start(); self.assertFalse(app.match.over)
        # Exercise stick, hat, dead zone and all eight controller assignments.
        class Pad:
            def get_numaxes(self): return 2
            def get_axis(self,i): return 1 if i==0 else 0
            def get_numhats(self): return 0
        app.pads={i:Pad() for i in range(8)}
        app.inputs()
        self.assertTrue(all(p.wanted==(1,0) for p in app.match.players))
        app.pads={}; app.run(frames=5)

    def test_every_pair_and_crossing(self):
        for count in (2,8):
            for theme in range(4):
                for attacker in range(count):
                    for victim in range(count):
                        if attacker==victim: continue
                        g=Match(count,theme,seed=9); g.foes=[]
                        p,q=g.players[attacker],g.players[victim]
                        p.safe=q.safe=0; p.effects['Titan']=7
                        p.pos=(2,1); q.pos=(1,1)
                        old=[r.pos for r in g.players]
                        old[attacker],old[victim]=q.pos,p.pos
                        g.combat(old)
                        self.assertEqual(q.lives,2)
                        self.assertEqual(p.score,300)

    def test_all_counts_all_stage_transitions(self):
        for count in (1,2,8):
            g=Match(count,seed=3)
            for stage in range(1,9):
                before=[p.score for p in g.players]
                time=g.time
                g.dots.clear(); g.update(.01)
                self.assertEqual(g.stage,stage+1)
                self.assertEqual(g.arena.theme,stage%4)
                self.assertAlmostEqual(g.time,time-.01)
                self.assertEqual([p.score for p in g.players],[s+500 for s in before])
                self.assertTrue(all(p.lives==3 for p in g.players))

    def test_menu_events_and_pause(self):
        app=App()
        for count in (1,2,8):
            app.match=None
            pg.event.post(pg.event.Event(pg.KEYDOWN,key=pg.K_0+count))
            app.events(); self.assertEqual(app.count,count)
            pg.event.post(pg.event.Event(pg.KEYDOWN,key=pg.K_RETURN))
            app.events(); self.assertEqual(len(app.match.players),count)
            app.match.players[0].pos=(1,1)
            pg.event.post(pg.event.Event(pg.KEYDOWN,key=pg.K_RIGHT))
            app.events(); app.match.update(.16)
            self.assertEqual(app.match.players[0].pos,(2,1))
            pg.event.post(pg.event.Event(pg.KEYDOWN,key=pg.K_p))
            app.events(); self.assertTrue(app.match.paused)
            t=app.match.time; app.match.update(1); self.assertEqual(app.match.time,t)
            app.match.over=True
            pg.event.post(pg.event.Event(pg.KEYDOWN,key=pg.K_RETURN))
            app.events(); self.assertFalse(app.match.over)
            self.assertEqual(app.match.time,180)
        pg.quit()

    def test_complete_autoplay_matches(self):
        for count in (1,2,8):
            for theme in range(4):
                g=Match(count,theme,seed=20+theme)
                moved=set()
                for tick in range(3601):
                    if tick%3==0: steer_demo(g)
                    previous=[p.pos for p in g.players]
                    g.update(.05)
                    moved.update(p.idx for p,old in zip(g.players,previous) if p.pos!=old)
                    if g.over: break
                self.assertTrue(g.over)
                self.assertEqual(len(moved),count)
                self.assertGreater(sum(p.score for p in g.players),0)

    def test_tunnels_and_power_strength(self):
        from game import COLS
        for theme in range(4):
            g=Match(2,theme,seed=4); g.items.clear(); g.foes=[]
            p,q=g.players
            p.pos=(0,9); p.direction=p.wanted=(-1,0)
            g.update(.11); self.assertEqual(p.pos,(COLS-1,9))
            p.safe=q.safe=0; p.pos=q.pos=(1,1)
            p.effects['Crown']=7
            g.combat(); self.assertEqual(q.lives,3)
            p.effects['Titan']=7; p.pos=q.pos=(1,1)
            g.combat(); self.assertEqual(q.lives,2)

    def test_resize_preserves_aspect(self):
        app=App(); app.start()
        app.screen=pg.display.set_mode((800,800),pg.RESIZABLE)
        app.draw()
        self.assertEqual(tuple(app.screen.get_at((400,0)))[:3],(0,0,0))
        self.assertEqual(tuple(app.screen.get_at((400,799)))[:3],(0,0,0))
        pg.quit()

    def test_roaming_collectibles(self):
        for theme in range(4):
            g=Match(1,theme,seed=20); g.foes=[]
            fixed={c:n for c,n in g.items.items() if n in ('Crown','Titan')}
            roaming={c for c,n in g.items.items() if n not in ('Crown','Titan')}
            count=len(g.items)
            for _ in range(10): g.update(.25)
            self.assertEqual(len(g.items),count)
            self.assertTrue(all(g.items.get(c)==n for c,n in fixed.items()))
            self.assertNotEqual({c for c,n in g.items.items() if n not in ('Crown','Titan')},roaming)
            self.assertTrue(all(c in g.arena.floor for c in g.items))

    def test_single_lane_geometry_and_visible_routes(self):
        from game import COLS, ROWS, TILE, THEMES
        from arcade_art import maze_background
        pg.init()
        for theme in range(4):
            arena=Arena(theme)
            art=maze_background(arena.floor,COLS,ROWS,TILE,THEMES[theme][1])
            for x,y in arena.lanes:
                self.assertFalse(all(c in arena.lanes for c in ((x+1,y),(x,y+1),(x+1,y+1))),
                                 'A two-lane open square must never be generated')
                neighbors=[arena.step((x,y),d) for d in DIRS if arena.step((x,y),d) in arena.lanes]
                self.assertGreaterEqual(len(neighbors),2,'Unintended blind corridor')
                self.assertEqual(tuple(art.get_at((x*TILE+10,y*TILE+10)))[:3],(0,0,4))
                for nx,ny in neighbors:
                    if abs(nx-x)+abs(ny-y)==1:
                        for t in range(TILE):
                            px=x*TILE+10+(nx-x)*t; py=y*TILE+10+(ny-y)*t
                            self.assertEqual(tuple(art.get_at((px,py)))[:3],(0,0,4),'Visible wall blocks movement edge')
        pg.quit()

    def test_player_gate_launch_return_and_respawn(self):
        for theme in range(4):
            g=Match(8,theme,seed=19); g.foes=[]; g.items.clear()
            for p in g.players:
                gate=g.arena.spawns[p.idx]; entry=g.arena.entries[p.idx]
                self.assertEqual(p.pos,gate)
                self.assertNotIn(gate,g.dots)
                self.assertTrue(g.arena.can_enter(gate,p))
                for other in g.players:
                    if other is not p: self.assertFalse(g.arena.can_enter(gate,other))
            for _ in range(49): g.update(1/60)
            for p in g.players:
                gate=g.arena.spawns[p.idx]; entry=g.arena.entries[p.idx]
                self.assertEqual(p.pos,entry)
                p.wanted=p.direction=(0,-1 if gate[1]==0 else 1)
            g.update(.11)
            for p in g.players:
                self.assertEqual(p.pos,g.arena.spawns[p.idx])
                p.wanted=p.direction=(0,1 if p.pos[1]==0 else -1)
            g.update(.11)
            for p in g.players:
                self.assertEqual(p.pos,g.arena.entries[p.idx])
                p.safe=0; self.assertTrue(g.hurt(p))
                self.assertEqual(p.pos,g.arena.spawns[p.idx])
                self.assertEqual(p.lives,2)
            for _ in range(49): g.update(1/60)
            self.assertTrue(all(p.pos==g.arena.entries[p.idx] for p in g.players))

    def test_ghost_house_departure_and_continuous_return(self):
        for theme in range(4):
            g=Match(1,theme,seed=11)
            self.assertTrue(all(15<=f[1]<=19 for f in g.foes))
            for _ in range(90): g.update_foes(.16)
            self.assertEqual(g.foe_modes,['roaming']*4)
            self.assertTrue(all(f in g.arena.lanes for f in g.foes))
            for i in range(4):
                g.foes[i]=(25,13); g.reset_foe(i)
            saw_enter=[False]*4; saw_house=[False]*4
            for _ in range(100):
                old=list(g.foes); g.update_foes(.16)
                for i in range(4):
                    self.assertLessEqual(abs(old[i][0]-g.foes[i][0])+abs(old[i][1]-g.foes[i][1]),1)
                    saw_enter[i]|=g.foe_modes[i]=='entering'
                    saw_house[i]|=g.foe_modes[i]=='house'
                if all(saw_house): break
            self.assertTrue(all(saw_enter)); self.assertTrue(all(saw_house))

    def test_magnet_capture_weapon_and_expiry(self):
        g=Match(2,seed=2); p,q=g.players
        p.pos=(1,1); q.pos=(5,1); p.safe=q.safe=0
        p.effects['Lure']=7; p.direction=(1,0)
        g.foes=[p.pos]; g.foe_modes=['roaming']; g.foe_release=[0]; g.foe_ticks=[0]; g.foe_zapped=[0]
        g.combat(); self.assertEqual(g.foe_modes[0],'carried'); self.assertEqual(p.lives,3)
        g.update_foes(.17); self.assertEqual(g.foes[0],(2,1))
        q.pos=(2,1); g.combat(); self.assertEqual(q.lives,2); self.assertEqual(p.score,300)
        p.effects.clear(); g.update_foes(.17); self.assertEqual(g.foe_modes[0],'eyes')

    def test_local_effects_and_no_wall_penetration(self):
        g=Match(3,seed=2); p,q,r=g.players
        p.pos=(1,1); q.pos=(3,1); r.pos=(53,29)
        g.collect(p,'Spark'); self.assertEqual(q.stun,2); self.assertEqual(r.stun,0)
        g.collect(p,'Mist'); p.direction=p.wanted=(1,0); p.entry=0
        g.update(.11); self.assertIn((1,1),g.smoke)
        g.collect(p,'Quake'); self.assertGreater(g.quake,0)
        p.pos=(1,1); p.direction=(-1,0); p.effects['Flare']=3
        self.assertEqual(g.fire_cells(p),[])
        p.direction=(1,0); self.assertEqual(g.fire_cells(p),[(2,1),(3,1),(4,1),(5,1),(6,1)])
        q.pos=(3,1); q.safe=0; g.apply_fire(); self.assertEqual(q.lives,2)

    def test_normal_bumps_bonus_life_and_crossing_ghost(self):
        g=Match(2,seed=2); p,q=g.players; g.foes=[]
        p.pos=q.pos=(5,1); p.safe=q.safe=0
        g.combat(); self.assertNotEqual(p.pos,q.pos)
        self.assertEqual((p.lives,q.lives),(3,3)); self.assertEqual((p.score,q.score),(0,0))
        p.score=10000; g.update(.01); self.assertEqual(p.lives,4)
        g.update(.01); self.assertEqual(p.lives,4)
        g.foes=[(1,1)]; g.foe_modes=['roaming']; p.pos=(2,1); p.safe=0
        g.combat([(1,1),q.pos],[(2,1)]); self.assertEqual(p.lives,3)

    def test_spawn_clocks_reset_between_arenas(self):
        g=Match(8,seed=9); g.item_clock=2.9; g.item_walk_clock=.23
        g.new_arena(1)
        self.assertEqual(g.item_clock,0); self.assertEqual(g.item_walk_clock,0)
        self.assertTrue(all(c in g.arena.lanes for c in g.items))

    def test_carried_ghost_cannot_attack_after_expiry_or_death(self):
        for expired in (True,False):
            g=Match(2); p,q=g.players; p.pos=(1,1); q.pos=(2,1); p.direction=(1,0)
            p.effects['Lure']=7; q.safe=0
            g.foes=[q.pos]; g.foe_modes=['carried']; g.foe_carriers={0:0}
            if expired: p.effects.clear()
            else: p.lives=0
            g.combat(); self.assertEqual(q.lives,3); self.assertEqual(p.score,0)
            self.assertEqual(g.foe_modes[0],'eyes')
        g=Match(1); p=g.players[0]; p.pos=(1,1); p.safe=2; p.effects['Crown']=7
        g.foes=[p.pos]; g.foe_modes=['roaming']
        g.combat(); self.assertEqual(p.score,200); self.assertEqual(p.lives,3)

    def test_speed_skid_quake_and_local_smoke(self):
        def ready():
            g=Match(1,seed=4); g.items.clear(); g.foes=[]
            p=g.players[0]; p.pos=(1,1); p.entry=0; p.direction=p.wanted=(1,0)
            return g,p
        normal,p=ready(); normal.update(.07); self.assertEqual(p.pos,(1,1))
        fast,p=ready(); p.effects['Rush']=7; fast.update(.07); self.assertEqual(p.pos,(2,1))
        slow,p=ready(); slow.quake=5; slow.update(.11); self.assertEqual(p.pos,(1,1))
        skid,p=ready(); p.effects['Slick']=2; p.wanted=(0,1); skid.update(.06)
        self.assertEqual(p.pos,(2,1))
        for smoke in (False,True):
            g=Match(1,seed=1); g.foes=[(5,1)]; g.foe_modes=['roaming']; g.foe_ticks=[0]; g.foe_release=[0]; g.foe_zapped=[0]
            if smoke: g.smoke[(5,1)]=2
            g.update_foes(.17)
            self.assertEqual(g.foes[0]==(5,1),smoke)

    def test_adversarial_crowds_crossings_and_gate_reset(self):
        g=Match(8); g.foes=[]; g.items.clear()
        for p in g.players: p.pos=(5,1); p.entry=0; p.safe=0
        g.combat(); self.assertEqual(len({p.pos for p in g.players}),8)
        g.players[0].pos=g.players[1].pos=(5,1)
        g.combat(); self.assertEqual(len({p.pos for p in g.players}),8)
        g=Match(2); g.foes=[]; g.items.clear(); p,q=g.players
        p.pos=(1,1); q.pos=(2,1); p.entry=q.entry=0; p.safe=q.safe=0
        p.direction=p.wanted=(1,0); q.direction=q.wanted=(-1,0)
        g.update(.11)
        self.assertEqual(p.direction,(-1,0)); self.assertEqual(q.direction,(1,0))
        self.assertLess(p.pos[0],q.pos[0])
        p.stun=2; p.clock=.09; p.safe=0; g.hurt(p)
        self.assertEqual((p.stun,p.clock),(0,0))
        for _ in range(49): g.update(1/60)
        self.assertEqual(p.pos,g.arena.entries[0])
        p.stun=2; p.clock=.09; g.new_arena(1)
        self.assertEqual((p.stun,p.clock),(0,0))
        p.score=9500; g.dots.clear(); g.update(.01)
        self.assertTrue(p.bonus_life)

    def test_seam_copies_preserve_giant_and_veil(self):
        from unittest.mock import patch
        import game
        app=App(); app.count=1; app.start(); p=app.match.players[0]
        p.pos=(1,9); p.effects={'Titan':7,'Veil':7}; p.entry=0
        calls=[]
        original=game.muncher
        def capture(*args,**kwargs):
            calls.append((args,kwargs)); return original(*args,**kwargs)
        with patch.object(game,'muncher',capture): app.draw()
        bodies=[args for args,kwargs in calls if len(args)>5 and args[5]==36]
        self.assertEqual(len(bodies),2)
        self.assertTrue(all(args[8]==150 for args in bodies))
        pg.quit()

if __name__=='__main__': unittest.main(verbosity=2)

