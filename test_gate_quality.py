"""Photo-backed closed threshold lip and actual App gate-state QA."""
import os
os.environ['SDL_VIDEODRIVER']='dummy'
os.environ['SDL_AUDIODRIVER']='dummy'
import unittest
from unittest.mock import patch
import game
from gate_art import draw_station_gate,gate_geometry,GATE_LIP
from replay import digest

class GateQuality(unittest.TestCase):
    def test_tunnel_patch_respects_caller_clip_and_restores_it(self):
        from gate_art import draw_tunnel_neck
        for side in (-1,1):
            s=game.pg.Surface((200,160));s.fill((17,29,41))
            clip=game.pg.Rect(85,45,30,70);s.set_clip(clip)
            draw_tunnel_neck(s,100,80,side,game.PALETTES[4])
            self.assertEqual(s.get_clip(),clip)
            for point in ((84,53),(115,53),(100,44),(100,115)):
                self.assertEqual(tuple(s.get_at(point))[:3],(17,29,41))

    def test_tunnel_necks_have_highlight_and_halo_without_board_overpaint(self):
        from gate_art import draw_tunnel_neck
        for accent in game.PALETTES:
            for side in (-1,1):
                s=game.pg.Surface((200,160));s.fill((0,0,4))
                draw_tunnel_neck(s,100,80,side,accent)
                x=100+side*12
                peak=s.get_at((x,52))
                self.assertGreater(sum(peak[:3]),sum(accent))
                self.assertGreater(sum(s.get_at((x,49))[:3]),4)
                self.assertEqual(tuple(s.get_at((100-side*16,53)))[:3],(0,0,4))
                # Inner rail turns into its matching board frame core;
                # the old capped frame must not remain across the mouth.
                inner=107 if side<0 else 92
                for y in (58,57,56,50,44):
                    self.assertGreater(sum(s.get_at((inner,y))[:3]),sum(accent),(side,y))
                self.assertEqual(tuple(s.get_at((inner,80)))[:3],(0,0,4))

    def test_closed_lip_continuous_above_stripes_both_orientations(self):
        for accent in game.PALETTES:
            for upper in (False,True):
                s=game.pg.Surface((240,220));s.fill((0,0,4))
                geom=draw_station_gate(s,120,110,upper,accent,False)
                band=geom['hatch']
                self.assertTrue(all(tuple(s.get_at((x,band.top)))[:3]==GATE_LIP for x in range(band.left,band.right)))
                row=[tuple(s.get_at((x,band.top+3)))[:3] for x in range(band.left,band.right)]
                self.assertTrue(any(sum(c)<100 for c in row))
                self.assertTrue(any(sum(c)>400 for c in row))
                draw_station_gate(s,120,110,upper,accent,True)
                self.assertFalse(any(tuple(s.get_at((x,band.top)))[:3]==GATE_LIP for x in range(band.left,band.right)))

    def test_actual_all_profiles_palettes_and_station_states(self):
        app=game.App(simulate_controllers=True)
        try:
            app.cabinet.settings['free_play']=True
            for theme in range(4):
                for palette in range(len(game.PALETTES)):
                    for state in ('release','away','return','dead','empty'):
                        app.theme=theme;app.palette_override=palette
                        app.count=1 if state in ('release','empty') else 8
                        app.cabinet.settings['fill_bots']=state!='empty';app.start();g=app.match
                        for p in g.players:
                            p.score=123456789
                            if state=='away':
                                entry=g.arena.entries[p.idx]
                                p.pos=next(c for c in sorted(g.arena.lanes) if c[1]==entry[1] and abs(c[0]-entry[0])>4)
                                p.entry=0;p.wanted=(1,0)
                            elif state=='return':
                                p.pos=g.arena.entries[p.idx];p.entry=0
                                p.wanted=(0,-1) if g.arena.spawns[p.idx][1]==0 else (0,1)
                            elif state=='dead':p.lives=1;p.safe=0;p.effects={};g.hurt(p)
                        before=digest(g)
                        with patch.object(game,'muncher'):app.draw(0);app.draw(0)
                        self.assertEqual(digest(g),before)
                        for idx,spawn in enumerate(g.arena.spawns):
                            upper=spawn[1]==0;x=game.center(spawn)[0]
                            mouth=game.TOP+4 if upper else game.TOP+game.ROWS*game.TILE-4
                            band=gate_geometry(x,mouth,upper)['hatch']
                            hits=sum(tuple(app.canvas.get_at((px,band.top)))[:3]==GATE_LIP for px in range(band.left,band.right))
                            closed=state in ('away','dead') or state=='empty' and idx>0
                            self.assertEqual(hits,48 if closed else 0,(theme,palette,state,idx,hits))
        finally:game.pg.quit()

if __name__=='__main__':unittest.main(verbosity=2)
