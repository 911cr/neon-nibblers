import os
os.environ.setdefault('SDL_VIDEODRIVER','dummy')
os.environ.setdefault('SDL_AUDIODRIVER','dummy')
import unittest
import pygame as pg
from maze_transition import render_background,wall_scale,actor_scale

class MazeTransitionTests(unittest.TestCase):
    def setUp(self):
        self.old=pg.Surface((200,100));self.old.fill((0,0,4))
        self.new=self.old.copy()
        pg.draw.rect(self.old,(80,100,255),(5,5,190,90),3)
        pg.draw.rect(self.new,(255,100,80),(15,15,170,70),3)
    def test_endpoints_and_inputs_are_exact(self):
        old=pg.image.tobytes(self.old,'RGB');new=pg.image.tobytes(self.new,'RGB')
        self.assertEqual(pg.image.tobytes(render_background(self.old,self.new,0),'RGB'),old)
        self.assertEqual(pg.image.tobytes(render_background(self.old,self.new,1),'RGB'),new)
        for p in (.2,.5,.8):render_background(self.old,self.new,p)
        self.assertEqual(pg.image.tobytes(self.old,'RGB'),old)
        self.assertEqual(pg.image.tobytes(self.new,'RGB'),new)
    def test_midpoint_is_compressed_visible_and_actors_enlarged(self):
        image=render_background(self.old,self.new,.5)
        self.assertEqual(image.get_size(),(200,100))
        self.assertEqual(image.get_at((0,0))[:3],(0,0,4))
        self.assertGreater(sum(pg.image.tobytes(image,'RGB')),200*100*4+10000)
        self.assertAlmostEqual(wall_scale(.5),.90)
        self.assertAlmostEqual(actor_scale(.5),1.35)
        for p in (0,1):self.assertEqual(actor_scale(p),1)
    def test_scale_is_smooth_symmetric_and_time_based(self):
        for p in (0,.1,.25,.4,.5):
            self.assertAlmostEqual(wall_scale(p),wall_scale(1-p))
            self.assertAlmostEqual(actor_scale(p),actor_scale(1-p))
        for fps in (30,60,144):
            self.assertEqual(wall_scale((fps//2)/fps),wall_scale(.5))
        self.assertLess(abs(wall_scale(.5001)-wall_scale(.4999)),.0001)
    def test_validates_sizes_and_progress(self):
        with self.assertRaises(ValueError):render_background(self.old,pg.Surface((2,2)),.5)
        for value in (float('nan'),float('inf')):
            with self.assertRaises(ValueError):render_background(self.old,self.new,value)
        self.assertEqual(wall_scale(-1),1)
        self.assertEqual(wall_scale(2),1)

if __name__=='__main__':unittest.main()
