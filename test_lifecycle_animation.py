"""Presentation lifecycle checks never certify undocumented DX animation timings."""
import copy
import os
os.environ['SDL_VIDEODRIVER']='dummy'
os.environ['SDL_AUDIODRIVER']='dummy'
import unittest
import pygame as pg
from game import App,Match,center,COLORS,OX,TOP,COLS,ROWS,TILE,W,H,station_hud
from replay import digest
from presentation import LifecyclePresentation


class LifecycleTests(unittest.TestCase):
    def setUp(self):
        pg.init()
        self.g=Match(2,seed=12)
        self.fx=LifecyclePresentation()
        self.fx.update(self.g,0)
        self.board=pg.Rect(OX,TOP,COLS*TILE,ROWS*TILE)

    def tearDown(self):pg.quit()

    def image(self):
        surface=pg.Surface((W,H),pg.SRCALPHA)
        self.fx.draw_effects(surface,center,COLORS,self.board,self.g.arena.portals)
        return surface

    def test_growth_and_shrink_are_smooth_bounded_and_do_not_delay_rules(self):
        p=self.g.players[0]
        self.g.collect(p,'Titan');self.fx.update(self.g,0)
        self.assertTrue(self.g.active(p,'Titan'))
        self.assertEqual(self.fx.radius(0),17)
        values=[]
        for _ in range(15):self.fx.update(self.g,1/60);values.append(self.fx.radius(0))
        self.assertEqual(values[-1],36)
        self.assertEqual(values,sorted(values))
        self.assertTrue(all(type(r) is int and 17<=r<=36 for r in values))
        p.effects.clear();self.fx.update(self.g,0)
        self.assertFalse(self.g.active(p,'Titan'))
        self.assertEqual(self.fx.radius(0),36)
        self.fx.update(self.g,.125);self.assertTrue(17<self.fx.radius(0)<36)
        self.fx.update(self.g,.125);self.assertEqual(self.fx.radius(0),17)

    def test_rapid_power_toggle_continues_from_current_size_without_jump(self):
        p=self.g.players[0]
        self.g.collect(p,'Titan');self.fx.update(self.g,0);self.fx.update(self.g,.1)
        middle=self.fx.radius(0)
        p.effects.clear();self.fx.update(self.g,0)
        self.assertEqual(self.fx.radius(0),middle)
        self.fx.update(self.g,.05)
        smaller=self.fx.radius(0)
        self.g.collect(p,'Titan');self.fx.update(self.g,0)
        self.assertEqual(self.fx.radius(0),smaller)
        self.fx.update(self.g,.25);self.assertEqual(self.fx.radius(0),36)

    def test_death_uses_old_event_position_once_and_arrival_uses_bay(self):
        p=self.g.players[0];p.pos=(5,9);p.safe=0
        self.assertTrue(self.g.hurt(p))
        before=digest(self.g)
        self.fx.update(self.g,0)
        self.assertEqual(self.fx.deaths[0].position,(5,9))
        self.assertEqual(self.fx.arrivals[0].position,self.g.arena.spawns[0])
        self.assertEqual(p.pos,self.g.arena.spawns[0])
        self.fx.update(self.g,0)
        self.assertEqual(len(self.fx.deaths),1);self.assertEqual(len(self.fx.arrivals),1)
        self.image();self.assertEqual(digest(self.g),before)
        self.fx.update(self.g,.45)
        self.assertEqual(self.fx.deaths,[]);self.assertEqual(self.fx.arrivals,[])

    def test_last_life_death_has_no_false_respawn_arrival(self):
        p=self.g.players[0];p.lives=1;p.safe=0;p.pos=(5,9)
        self.g.hurt(p);self.fx.update(self.g,0)
        self.assertEqual(len(self.fx.deaths),1)
        self.assertEqual(self.fx.arrivals,[])

    def test_pause_freezes_all_feedback_and_preserves_match(self):
        p=self.g.players[0];p.pos=(5,9);p.safe=0;self.g.hurt(p)
        self.g.collect(self.g.players[1],'Titan');self.fx.update(self.g,0);self.fx.update(self.g,.1)
        before=(self.fx.time,copy.deepcopy(self.fx.radii),copy.deepcopy(self.fx.deaths),
                copy.deepcopy(self.fx.arrivals),pg.image.tobytes(self.image(),'RGBA'),digest(self.g))
        for _ in range(30):self.fx.update(self.g,0);self.image()
        after=(self.fx.time,self.fx.radii,self.fx.deaths,self.fx.arrivals,
               pg.image.tobytes(self.image(),'RGBA'),digest(self.g))
        self.assertEqual(before,after)

    def test_continuous_stage_keeps_feedback_but_new_session_resets(self):
        p=self.g.players[0];p.pos=(5,9);p.safe=0;self.g.hurt(p)
        self.fx.update(self.g,0)
        self.g.dots.clear();self.g.update(1/60);self.fx.update(self.g,0)
        self.assertEqual(len(self.fx.deaths),1);self.assertEqual(len(self.fx.arrivals),1)
        self.fx.update(self.g,.45)
        self.assertEqual(self.fx.deaths,[]);self.assertEqual(self.fx.arrivals,[])
        other=Match(1,seed=99)
        self.fx.update(other,0)
        self.assertIs(self.fx.ledger,other.ledger)
        self.assertEqual(set(self.fx.radii),{0})
        self.assertEqual(self.fx.time,0)

    def test_tunnel_death_duplicates_without_painting_hud(self):
        row=self.g.arena.portals[0]
        p=self.g.players[0];p.pos=(0,row);p.safe=0;p.lives=1
        self.g.hurt(p);self.fx.update(self.g,0);self.fx.update(self.g,.15)
        surface=self.image();bounds=surface.get_bounding_rect(min_alpha=1)
        self.assertTrue(self.board.contains(bounds))
        cy=center((0,row))[1]
        for rect in (pg.Rect(OX,cy-48,40,96),pg.Rect(self.board.right-40,cy-48,40,96)):
            self.assertGreater(pg.mask.from_surface(surface.subsurface(rect),0).count(),0)

    def test_arrival_stays_in_station_bay_and_restores_clip(self):
        self.g=Match(0,seed=12);self.g.join_station(0);self.g.join_station(3)
        self.fx.update(self.g,0);surface=self.image()
        mask=pg.mask.from_surface(surface,0)
        self.assertGreater(mask.count(),0)
        for spawn in self.g.arena.spawns:
            rect=station_hud(spawn)['score']
            self.assertEqual(pg.mask.from_surface(surface.subsurface(rect),0).count(),0)
        clipped=pg.Surface((W,H),pg.SRCALPHA);prior=pg.Rect(100,20,1000,670)
        clipped.set_clip(prior)
        self.fx.draw_effects(clipped,center,COLORS,self.board,self.g.arena.portals)
        self.assertEqual(clipped.get_clip(),prior)

    def test_shared_timestamps_match_at_30_60_144_hz(self):
        self.g.collect(self.g.players[0],'Titan')
        values=[]
        for fps in (30,60,144):
            fx=LifecyclePresentation();fx.update(self.g,0)
            for _ in range(fps//2):fx.update(self.g,1/fps)
            values.append(fx.radius(0))
        self.assertEqual(values,[36,36,36])

    def test_first_observed_growth_does_not_add_one_render_frame_delay(self):
        self.g.collect(self.g.players[0],'Titan')
        values=[]
        # At a shared 1/6-second timestamp, all rates should be equally grown
        # even when no separate zero-delta draw observes the pickup first.
        for fps in (30,60,144):
            fx=LifecyclePresentation()
            for _ in range(fps//6):fx.update(self.g,1/fps)
            values.append(fx.radius(0))
        self.assertEqual(len(set(values)),1)
        self.assertTrue(17<values[0]<36)

    def test_actual_app_integrates_lifecycle_without_simulation_mutation(self):
        app=App(simulate_controllers=True);app.count=1;app.start()
        p=app.match.players[0];p.pos=(5,9);p.entry=p.safe=0
        app.draw(0)
        app.match.collect(p,'Titan');before=digest(app.match)
        app.draw(.125)
        self.assertTrue(17<app.presentation.radius(0)<36)
        self.assertEqual(digest(app.match),before)
        app.match.paused=True
        radius=app.presentation.radius(0);time=app.presentation.time
        app.draw(.5)
        self.assertEqual((app.presentation.radius(0),app.presentation.time),(radius,time))
        app.match.paused=False;p.effects.clear();app.match.hurt(p)
        app.draw(.1)
        self.assertEqual(app.presentation.deaths[0].position,(5,9))
        self.assertEqual(len(app.presentation.arrivals),1)
        app.start()
        self.assertEqual(app.presentation.deaths,[])

    def test_eight_growing_players_reuse_lighting_and_bounded_size_cache(self):
        from arcade_art import sphere,_sphere_template
        app=App(simulate_controllers=True);app.count=8;app.start();app.match.items={}
        sphere.cache_clear();_sphere_template.cache_clear()
        app.draw(0)
        for p in app.match.players:app.match.collect(p,'Titan')
        for _ in range(15):app.draw(1/60)
        self.assertTrue(all(app.presentation.radius(p.idx)==36 for p in app.match.players))
        for p in app.match.players:p.effects.clear()
        for _ in range(15):app.draw(1/60)
        self.assertTrue(all(app.presentation.radius(p.idx)==17 for p in app.match.players))
        self.assertEqual(_sphere_template.cache_info().misses,8)
        self.assertLessEqual(sphere.cache_info().currsize,8*20)


if __name__=='__main__':unittest.main(verbosity=2)
