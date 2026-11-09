"""Rendered animation sequences and sizing checks for original procedural art."""
import math
import os
import unittest
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
import pygame as pg
from arcade_art import muncher, foe, power_icon, _power_sprite, fire_plume

POWERS = ('Crown','Titan','Rush','Mist','Slick','Spark','Veil','Flare','Quake','Heart','Lure')
DIRECTIONS = ((1,0),(-1,0),(0,-1),(0,1))


class AnimationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls): pg.init()

    def render(self, painter):
        surface = pg.Surface((128,128),pg.SRCALPHA)
        painter(surface)
        return surface

    def test_left_eye_stays_above_and_lighting_does_not_rotate(self):
        closed = 3*math.pi/(2*22)
        images = [self.render(lambda s,d=d: muncher(s,(64,64),(255,222,45),d,closed,36))
                  for d in DIRECTIONS]
        for surface in images[:2]:
            eye = [(x,y) for y in range(28,100) for x in range(28,100)
                   if surface.get_at((x,y)).a > 200 and
                   all(surface.get_at((x,y))[i] < limit for i,limit in enumerate((30,30,40)))]
            self.assertTrue(eye)
            self.assertLess(sum(y for _,y in eye)/len(eye),64)
        for position in ((47,47),(81,81),(47,81)):
            self.assertEqual(len({tuple(s.get_at(position)) for s in images}),1)

    def test_mouth_direction_and_animation_change(self):
        opened = math.pi/(2*22)
        for direction in DIRECTIONS:
            surface = self.render(lambda s: muncher(s,(64,64),(255,222,45),direction,opened,36))
            dx,dy = direction
            self.assertEqual(surface.get_at((64+dx*24,64+dy*24)).a,0)
            self.assertGreater(surface.get_at((64-dx*24,64-dy*24)).a,200)
        frames = [pg.image.tobytes(self.render(lambda s,t=t: muncher(s,(64,64),(255,222,45),(1,0),t,36)),'RGBA')
                  for t in (0,.04,.08,.12,.16)]
        self.assertEqual(len(set(frames)),len(frames))

    def test_normal_giant_and_translucent_sprites_fit(self):
        for radius in (17,36):
            for direction in DIRECTIONS:
                for time in (0,.05,.1,.15):
                    surface = self.render(lambda s: muncher(s,(64,64),(90,141,255),direction,time,radius,True,True,150))
                    bounds = surface.get_bounding_rect(min_alpha=1)
                    self.assertGreater(bounds.width,0)
                    self.assertTrue(pg.Rect(64-radius-10,64-radius-10,2*(radius+10),2*(radius+10)).contains(bounds))
                    self.assertLessEqual(max(pg.image.tobytes(surface,'RGBA')[3::4]),150)

    def test_ghost_stun_has_visible_animated_feedback(self):
        def frame(time=0,stunned=False,eyes=False):
            return pg.image.tobytes(self.render(lambda s: foe(s,(64,64),(255,83,80),time,stunned,(1,0),False,eyes)),'RGBA')
        self.assertNotEqual(frame(),frame(stunned=True))
        self.assertNotEqual(frame(stunned=True),frame(.3,True))
        self.assertEqual(frame(eyes=True),frame(stunned=True,eyes=True))

    def test_ghost_orbit_and_feet_do_not_clip_sprite_edges(self):
        for index in range(48):
            surface=self.render(lambda s: foe(s,(64,64),(255,83,80),index/24,True,(1,0)))
            bounds=surface.get_bounding_rect(min_alpha=1)
            self.assertGreater(bounds.top,35)
            self.assertGreater(bounds.left,35)
            self.assertLess(bounds.bottom,93)
            self.assertLess(bounds.right,93)

    def test_power_sizes_antialiasing_and_position_independent_bob(self):
        for name in POWERS:
            for size in (16,22,32,42,64,96):
                sprite = _power_sprite(name,size)
                self.assertEqual(sprite.get_size(),(size,size))
                self.assertGreater(sprite.get_bounding_rect().width,0)
                alphas = pg.image.tobytes(sprite,'RGBA')[3::4]
                self.assertTrue(any(0<a<255 for a in alphas))
            left = self.render(lambda s: power_icon(s,(40,64),name,.4))
            right = self.render(lambda s: power_icon(s,(80,64),name,.4))
            a,b = left.get_bounding_rect(),right.get_bounding_rect()
            self.assertEqual(a.y,b.y)
            self.assertEqual(a.move(40,0),b)

    def test_art_samples_match_at_shared_times_for_30_60_144_hz(self):
        def frame(time):
            surface=pg.Surface((640,240),pg.SRCALPHA)
            muncher(surface,(60,80),(255,222,45),(-1,0),time,36,True)
            foe(surface,(150,80),(255,108,195),time,True,(-1,0),True)
            for i,name in enumerate(POWERS):power_icon(surface,(24+i*55,180),name,time,42)
            return pg.image.tobytes(surface,'RGBA')
        for seconds in (0,.5,1,1.5):
            self.assertEqual(len({frame(round(seconds*hz)/hz) for hz in (30,60,144)}),1)

    def test_fire_plume_animates_without_overshooting_corridor(self):
        for direction in DIRECTIONS:
            dx,dy=direction; origin=(64,64); end=(64+dx*50,64+dy*50)
            frames=[]
            for time in (0,.07,.13):
                surface=self.render(lambda s: fire_plume(s,origin,end,direction,time))
                bounds=surface.get_bounding_rect(min_alpha=1)
                self.assertGreater(bounds.width,0)
                legal=(pg.Rect(min(origin[0],end[0]),48,51,33) if dx else
                       pg.Rect(48,min(origin[1],end[1]),33,51))
                self.assertTrue(legal.contains(bounds),(direction,bounds,legal))
                frames.append(pg.image.tobytes(surface,'RGBA'))
            self.assertEqual(len(set(frames)),3)
        surface=self.render(lambda s: fire_plume(s,(110,64),(10,64),(1,0),0))
        self.assertEqual(surface.get_bounding_rect().width,0)


if __name__=='__main__': unittest.main(verbosity=2)
