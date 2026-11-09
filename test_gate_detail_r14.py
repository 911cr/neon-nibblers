"""Actual station-gate rendering checks; static photo cannot prove gate timing."""
import os
os.environ['SDL_VIDEODRIVER']='dummy'
os.environ['SDL_AUDIODRIVER']='dummy'
import unittest
from unittest.mock import patch
import game

class GateDetailQA(unittest.TestCase):
    def setUp(self):
        self.app=game.App(simulate_controllers=True)
        self.app.cabinet.settings.update(free_play=True,fill_bots=True)
        self.app.count=1;self.app.start()
    def tearDown(self):game.pg.quit()
    def hatch_pixels(self,idx):
        spawn=self.app.match.arena.spawns[idx];sx=game.center(spawn)[0]
        y=game.TOP+4 if spawn[1]<game.ROWS//2 else game.TOP+game.ROWS*game.TILE-4
        crop=self.app.canvas.subsurface(game.pg.Rect(sx-20,y-6,40,12))
        return game.pg.mask.from_threshold(crop,game.GATE_HATCH,(2,2,2,255)).count()
    def draw_gates(self):
        # Hide actor artwork only so it cannot occlude a closed physical hatch.
        with patch.object(game,'muncher'):
            self.app.draw(0);self.app.draw(0)
    def start_profile(self,theme):
        self.app.theme=theme;self.app.start()
    def test_human_and_unjoined_ai_release_gates_open_all_profiles(self):
        for theme in range(4):
            self.start_profile(theme);self.draw_gates()
            for idx in range(8):
                self.assertGreater(self.app.match.players[idx].entry,0)
                self.assertEqual(self.hatch_pixels(idx),0,(theme,idx))
    def test_far_border_actor_does_not_open_its_distant_gate(self):
        for theme in range(4):
            self.start_profile(theme);g=self.app.match
            for p in g.players:
                entry=g.arena.entries[p.idx]
                p.pos=next(c for c in sorted(g.arena.lanes) if c[1]==entry[1] and abs(c[0]-entry[0])>4)
                p.entry=0;p.wanted=(1,0)
            self.draw_gates()
            for idx in range(8):self.assertGreater(self.hatch_pixels(idx),0,(theme,idx))
    def test_owner_return_opens_hatch_for_human_and_ai(self):
        for theme in range(4):
            self.start_profile(theme);g=self.app.match
            for p in g.players:
                p.pos=g.arena.entries[p.idx];p.entry=0
                p.wanted=(0,-1) if g.arena.spawns[p.idx][1]==0 else (0,1)
            self.draw_gates()
            for idx in range(8):self.assertEqual(self.hatch_pixels(idx),0,(theme,idx))
    def test_empty_eliminated_and_continue_waiting_gates_remain_closed(self):
        for theme in range(4):
            for count in (1,8):
                self.app.cabinet.settings['fill_bots']=False;self.app.count=count
                self.start_profile(theme);g=self.app.match
                for p in g.players:
                    p.safe=0;p.lives=1;p.effects={};g.hurt(p)
                self.assertTrue(g.continues.active)
                self.draw_gates()
                for idx in range(8):self.assertGreater(self.hatch_pixels(idx),0,(theme,count,idx))

    def test_closed_hatch_is_a_filled_band_and_open_throat_is_clear(self):
        for theme in range(4):
            self.app.cabinet.settings['fill_bots']=False
            self.start_profile(theme)
            self.draw_gates()
            for idx,spawn in enumerate(self.app.match.arena.spawns):
                sx=game.center(spawn)[0]
                y=game.TOP+4 if spawn[1]<game.ROWS//2 else game.TOP+game.ROWS*game.TILE-4
                # A filled yellow band may legitimately contain dark stripes.
                # Require yellow body coverage on every interior row, not solid
                # yellow pixels and not a lone line with sparse hatch marks.
                rows=[sum(sum(self.app.canvas.get_at((x,py))[:3])>100
                          for x in range(sx-16,sx+16)) for py in range(y-3,y+4)]
                if idx==0:
                    self.assertEqual(sum(rows),0,(theme,idx,'open throat'))
                else:
                    self.assertTrue(all(count>=10 for count in rows),(theme,idx,'filled hatch',rows))

    def test_normal_spawn_body_fits_physical_pocket_all_stations(self):
        from gate_art import gate_geometry
        for theme in range(4):
            self.start_profile(theme)
            for idx,spawn in enumerate(self.app.match.arena.spawns):
                x,y=game.center(spawn);upper=spawn[1]==0
                mouth=game.TOP+4 if upper else game.TOP+game.ROWS*game.TILE-4
                pocket=gate_geometry(x,mouth,upper)['outer']
                self.assertTrue(pocket.contains(game.pg.Rect(x-17,y-17,34,34)),(theme,idx,pocket,(x,y)))

    def test_departure_keeps_hatch_open_until_normal_body_clears(self):
        self.app.count=8
        for theme in range(4):
            self.start_profile(theme);g=self.app.match
            self.draw_gates()
            self.app.advance(.8)
            self.assertTrue(all(p.pos==g.arena.entries[p.idx] for p in g.players))
            for _ in range(30):
                with patch.object(game,'muncher'):self.app.draw(1/60)
                for idx,spawn in enumerate(g.arena.spawns):
                    upper=spawn[1]==0
                    mouth=game.TOP+4 if upper else game.TOP+game.ROWS*game.TILE-4
                    # Gate and body now share this frame's precomputed pose.
                    y=self.app.visual_positions[idx][1]
                    not_cleared=y-17<=mouth+5 if upper else y+17>=mouth-5
                    if not_cleared:self.assertEqual(self.hatch_pixels(idx),0,(theme,idx,y,mouth))

    def test_pocket_glow_clearance_from_scores_lives_and_canvas_edges(self):
        from gate_art import gate_geometry
        self.app.count=8
        for theme in range(4):
            self.start_profile(theme)
            for value in (0,999999,999999999):
                for idx,spawn in enumerate(self.app.match.arena.spawns):
                    x,_=game.center(spawn);upper=spawn[1]==0
                    mouth=game.TOP+4 if upper else game.TOP+game.ROWS*game.TILE-4
                    glow=gate_geometry(x,mouth,upper)['outer'].inflate(12,12)
                    hud=game.station_hud(spawn,value)
                    self.assertFalse(glow.colliderect(hud['score']),(theme,idx,value,glow,hud['score']))
                    self.assertFalse(glow.colliderect(hud['lives']))
                    self.assertTrue(game.pg.Rect(0,0,game.W,game.H).contains(glow),(theme,idx,glow))
                    self.assertTrue(game.pg.Rect(0,0,game.W,game.H).contains(hud['score']))

    def test_actual_normal_actor_render_has_unclipped_pocket_pass(self):
        for theme in range(4):
            self.start_profile(theme);calls=[];original=game.muncher
            def capture(*args,**kwargs):
                calls.append((args,game.pg.Rect(args[0].get_clip())))
                return original(*args,**kwargs)
            with patch.object(game,'muncher',capture):self.app.draw(0)
            for p in self.app.match.players:
                expected=game.center(p.pos)
                bodies=[(args,clip) for args,clip in calls if args[2]==game.COLORS[p.idx] and args[5]==17]
                self.assertTrue(any(tuple(args[1])==expected and clip.contains(game.pg.Rect(expected[0]-17,expected[1]-17,34,34))
                                    for args,clip in bodies),(theme,p.idx,expected,[(args[1],clip) for args,clip in bodies]))

    def test_parallel_gate_edges_and_visible_soft_halo_on_opaque_canvas(self):
        from gate_art import draw_station_gate
        for accent in game.PALETTES:
            for upper in (False,True):
                surface=game.pg.Surface((200,200));surface.fill((0,0,4))
                draw_station_gate(surface,100,100,upper,accent,True)
                y=80 if upper else 120
                outer=surface.get_at((68,y));inner=surface.get_at((74,y))
                between=surface.get_at((71,y));halo=surface.get_at((64,y))
                self.assertGreater(max(outer[:3]),150)
                self.assertGreater(max(inner[:3]),150)
                self.assertLess(max(between[:3]),150)
                self.assertGreater(sum(halo[:3]),12,(accent,upper,halo))
                self.assertLess(sum(halo[:3]),sum(outer[:3]))

    def test_house_contour_glow_survives_composition(self):
        from gate_art import draw_house
        surface=game.pg.Surface((240,200));surface.fill((0,0,4))
        draw_house(surface,game.pg.Rect(60,60,100,60),game.PALETTES[-1],110)
        halo=surface.get_at((56,90));core=surface.get_at((60,90))
        self.assertGreater(sum(halo[:3]),12)
        self.assertLess(sum(halo[:3]),sum(core[:3]))

if __name__=='__main__':unittest.main(verbosity=2)
