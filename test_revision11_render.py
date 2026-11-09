"""Actual render-call and animation-state checks, independent of commercial art."""
import copy
import os
os.environ['SDL_VIDEODRIVER']='dummy'
os.environ['SDL_AUDIODRIVER']='dummy'
import unittest
from unittest.mock import patch
import game
from replay import digest


class RenderQA(unittest.TestCase):
    def setUp(self):
        self.app=game.App(simulate_controllers=True)
        self.app.seed=71;self.app.count=8;self.app.start()

    def tearDown(self):game.pg.quit()

    def test_pause_guide_results_freeze_interpolation_and_transients(self):
        a=self.app;g=a.match;p=g.players[0]
        p.pos=(5,9);p.entry=0;g.items={(5,1):'Rush'}
        a.draw()
        p.pos=(6,9)
        g.award(p,'pickup')
        a.draw()
        for phase in ('paused','guide','results'):
            g.paused=phase=='paused';a.help=phase=='guide';g.over=phase=='results'
            before=(a.animation_time,copy.deepcopy(a.visual_positions),
                    copy.deepcopy(a.visual_foes),copy.deepcopy(a.visual_items),
                    copy.deepcopy(a.popups),digest(g))
            a.draw(.5);a.draw(.5)
            after=(a.animation_time,a.visual_positions,a.visual_foes,a.visual_items,
                   a.popups,digest(g))
            self.assertEqual(before,after,phase)

    def test_local_ghost_stun_matches_on_both_tunnel_images(self):
        a=self.app;g=a.match
        g.foes[0]=(0,g.arena.portals[0]);g.foe_modes[0]='roaming';g.foe_zapped[0]=1
        calls=[];original=game.foe
        def capture(*args,**kwargs):
            if args[2]==game.COLORS[3]:calls.append(args)
            return original(*args,**kwargs)
        with patch.object(game,'foe',capture):a.draw()
        self.assertEqual(len(calls),2)
        self.assertTrue(all(call[4] for call in calls))
        self.assertEqual(abs(calls[0][1][0]-calls[1][1][0]),game.COLS*game.TILE)

    def test_same_kind_item_tracks_survive_sort_reversal_and_collection(self):
        a=self.app;g=a.match
        old_a=(5,1);old_b=(5,9);new_a=(6,1);new_b=(4,9)
        self.assertTrue({old_a,old_b,new_a,new_b}<=g.arena.lanes)
        g.items={old_a:'Rush',old_b:'Rush'};a.draw()
        key_a=min(a.visual_items,key=lambda key:game.distance(a.visual_items[key],game.center(old_a)))
        key_b=min(a.visual_items,key=lambda key:game.distance(a.visual_items[key],game.center(old_b)))
        g.items={new_b:'Rush',new_a:'Rush'}
        tracks=a.item_tracks(g.items,g.arena.portals)
        self.assertEqual(tracks[new_a],key_a);self.assertEqual(tracks[new_b],key_b)
        a.draw()
        g.items={new_b:'Rush'}
        tracks=a.item_tracks(g.items,g.arena.portals)
        self.assertEqual(tracks[new_b],key_b)
        self.assertEqual(set(a.visual_items),{key_b})

    def test_item_track_uses_short_tunnel_distance(self):
        a=self.app
        a.visual_items={('Rush',0):game.center((0,9)),('Rush',1):game.center((53,9))}
        tracks=a.item_tracks({(58,9):'Rush',(52,9):'Rush'},(9,25))
        self.assertEqual(tracks[(58,9)],('Rush',0))
        self.assertEqual(tracks[(52,9)],('Rush',1))

    def test_damage_and_stage_start_discard_old_position_cache(self):
        a=self.app;g=a.match;p=g.players[0]
        p.pos=g.arena.entries[0];p.entry=p.safe=0;p.direction=p.wanted=(0,0)
        a.draw();self.assertTrue(g.hurt(p));a.draw()
        self.assertEqual(a.visual_positions[0],game.center(p.pos))
        p.pos=g.arena.entries[0];p.entry=0;a.draw()
        g.dots.clear();g.update(1/60);a.draw()
        self.assertEqual(g.stage,2)
        self.assertEqual(a.visual_positions[0],game.center(p.pos))

    def test_all_maps_counts_and_720_1080_render_without_footer_clipping(self):
        a=self.app
        for size in ((1280,720),(1920,1080)):
            a.screen=game.pg.display.set_mode(size)
            for theme in range(4):
                for count in (1,2,8):
                    a.theme=theme;a.count=count;a.start()
                    a.simulate_controllers=False;a.pads={}
                    footer=[]
                    class CaptureSurface(game.pg.Surface):
                        def blit(self,source,dest,*args,**kwargs):
                            point=dest.topleft if isinstance(dest,game.pg.Rect) else dest
                            if point[1]>=700:footer.append(source.get_rect(topleft=point))
                            return super().blit(source,dest,*args,**kwargs)
                    a.canvas=CaptureSurface((game.W,game.H))
                    before=digest(a.match)
                    a.draw()
                    self.assertEqual(digest(a.match),before)
                    self.assertEqual(a.screen.get_size(),size)
                    self.assertTrue(footer)
                    self.assertTrue(all(game.pg.Rect(0,0,game.W,game.H).contains(rect) for rect in footer))
                    bottom=sorted(c[0] for c in a.match.arena.spawns if c[1]==game.ROWS-1)
                    left=game.center((bottom[1],game.ROWS-1))[0]+164
                    right=game.center((bottom[2],game.ROWS-1))[0]-39
                    self.assertTrue(all(left<=rect.left and rect.right<=right for rect in footer),(theme,count,footer))

    def test_timer_and_station_scores_have_disjoint_actual_draw_bounds(self):
        a=self.app
        original=game.arcade_digits
        for theme in range(4):
            for count in (1,2,8):
                a.theme=theme;a.count=count;a.start()
                for score in (999999,123456789):
                    for player in a.match.players:player.score=score
                    rectangles=[]
                    def capture(surface,text,x,y,color,scale=3):
                        # Actual bitmap digits occupy five columns, with one blank
                        # column between characters (including the timer colon).
                        rectangles.append((str(text),game.pg.Rect(x,y,(6*len(str(text))-1)*scale,7*scale)))
                        return original(surface,text,x,y,color,scale)
                    with patch.object(game,'arcade_digits',capture):a.draw(0)
                    timers=[rect for label,rect in rectangles if ':' in label]
                    scores=[rect for label,rect in rectangles if label==str(score)]
                    self.assertEqual(len(timers),1)
                    self.assertEqual(len(scores),count)
                    for rect in scores:
                        self.assertFalse(rect.colliderect(timers[0]),(theme,count,score,rect,timers[0]))
                        self.assertTrue(game.pg.Rect(0,0,game.W,game.H).contains(rect))
                    self.assertTrue(game.pg.Rect(0,0,game.W,game.TOP).contains(timers[0]))

    def test_fire_and_zap_animate_then_freeze_and_remain_clipped(self):
        a=self.app;g=a.match;p=g.players[0]
        p.pos=(5,9);p.direction=(1,0);p.effects={'Flare':3}
        g.items={};g.zaps=[(p.pos,.5)]
        original_plume=game.fire_plume;original_lines=game.pg.draw.lines
        def sample(dt):
            calls=[]
            def plume(surface,origin,end,direction,time):
                isolated=game.pg.Surface(surface.get_size(),game.pg.SRCALPHA)
                original_plume(isolated,origin,end,direction,time)
                calls.append(('fire',game.pg.image.tobytes(isolated,'RGBA'),tuple(surface.get_clip())))
                return original_plume(surface,origin,end,direction,time)
            def lines(surface,color,closed,points,width=1):
                if color==(140,230,255):
                    calls.append(('zap',tuple(tuple(point) for point in points),tuple(surface.get_clip())))
                return original_lines(surface,color,closed,points,width)
            with patch.object(game,'fire_plume',plume),patch.object(game.pg.draw,'lines',lines):a.draw(dt)
            return calls
        first=sample(.02);second=sample(.08)
        self.assertNotEqual([c for c in first if c[0]=='fire'],[c for c in second if c[0]=='fire'])
        self.assertNotEqual([c for c in first if c[0]=='zap'],[c for c in second if c[0]=='zap'])
        bounds=(game.OX,game.TOP,game.COLS*game.TILE,game.ROWS*game.TILE)
        self.assertTrue(all(c[-1]==bounds for c in first+second))
        g.paused=True
        self.assertEqual(sample(.5),sample(.5))

    def test_flame_stops_at_wall_and_wrap_does_not_cross_board(self):
        a=self.app
        for theme in range(4):
            a.theme=theme;a.start();g=a.match;p=g.players[0];g.items={}
            cell,direction=next((cell,d) for cell in sorted(g.arena.lanes)
                                for d in game.DIRS if g.arena.step(cell,d) not in g.arena.lanes)
            p.pos=cell;p.direction=direction;p.effects={'Flare':3}
            self.assertEqual(g.fire_cells(p),[])
            with patch.object(game,'fire_plume') as plume:a.draw(0)
            plume.assert_not_called()
            row=g.arena.portals[0]
            for cell,direction in (((game.COLS-1,row),(1,0)),((0,row),(-1,0))):
                p.pos=cell;p.direction=direction;p.effects={};a.visual_positions={}
                a.draw(0)
                middle=game.pg.Rect(game.OX+200,game.center(cell)[1]-28,game.COLS*game.TILE-400,56)
                before=game.pg.image.tobytes(a.canvas.subsurface(middle),'RGB')
                p.effects={'Flare':3}
                calls=[];original=game.fire_plume
                def capture(surface,origin,end,direction,time):
                    calls.append((origin,end,direction))
                    return original(surface,origin,end,direction,time)
                with patch.object(game,'fire_plume',capture):a.draw(0)
                after=game.pg.image.tobytes(a.canvas.subsurface(middle),'RGB')
                self.assertEqual(before,after)
                self.assertEqual(len(calls),2)
                for origin,end,d in calls:
                    self.assertLessEqual(game.distance(origin,end),5*game.TILE)
                    self.assertGreater((end[0]-origin[0])*d[0],0)

    def test_world_effect_pixels_do_not_overpaint_station_hud(self):
        a=self.app;g=a.match;p=g.players[0]
        p.pos=(1,1);p.direction=(1,0);p.effects={};g.items={};a.draw(0)
        regions=[game.pg.Rect(0,0,game.W,game.TOP),
                 game.pg.Rect(0,game.TOP+game.ROWS*game.TILE,game.W,game.H-game.TOP-game.ROWS*game.TILE)]
        before=[game.pg.image.tobytes(a.canvas.subsurface(rect),'RGB') for rect in regions]
        p.effects={'Flare':3};g.zaps=[((1,1),.5),((57,29),.5)]
        g.smoke={(1,1):2.5,(57,29):2.5};a.draw(0)
        after=[game.pg.image.tobytes(a.canvas.subsurface(rect),'RGB') for rect in regions]
        self.assertEqual(before,after)

    def test_palette_changes_preserve_logic_and_recolor_each_layout(self):
        a=self.app
        for theme in range(4):
            a.theme=theme;a.palette_override=None;a.start()
            before=digest(a.match);images=[]
            for step in range(len(game.PALETTES)):
                game.pg.event.clear()
                game.pg.event.post(game.pg.event.Event(game.pg.KEYDOWN,key=game.pg.K_F12))
                a.events();a.draw(0)
                palette=(theme+step+1)%len(game.PALETTES)
                self.assertEqual(a.palette_override,palette)
                self.assertEqual(digest(a.match),before)
                key=(a.match.arena.map_id,a.match.arena.map_revision,palette)
                background=a.backgrounds[key]
                color=game.PALETTES[palette]
                count=game.pg.mask.from_threshold(background,color,(1,1,1,255)).count()
                self.assertGreater(count,100)
                images.append(game.pg.image.tobytes(background,'RGB'))
            self.assertEqual(len(set(images)),len(game.PALETTES))


if __name__=='__main__':unittest.main(verbosity=2)
