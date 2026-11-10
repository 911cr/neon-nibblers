"""Adversarial integration regressions; these do not certify commercial rules."""
import os
os.environ['SDL_VIDEODRIVER']='dummy'
os.environ['SDL_AUDIODRIVER']='dummy'
import unittest
from unittest.mock import patch
from game import App, Match, ITEMS, DIRS, station_hud, center, TOP, ROWS, TILE, pg


class GameplayQA(unittest.TestCase):
    def clean(self, count=2):
        g=Match(count,seed=91)
        g.items.clear()
        for p in g.players:
            p.entry=p.safe=p.stun=0
            p.pos=(1+4*p.idx,1)
            p.direction=p.wanted=(0,0)
        g.foe_modes=['house']*4
        return g

    def test_fixed_tick_configured_speed_not_rounded_down(self):
        moves={}
        for name,key in (('normal','player_step_seconds'),('Rush','rush_step_seconds'),('Slick','slick_step_seconds')):
            g=self.clean(1);p=g.players[0]
            expected=int((1.+1e-9)/g.tuning[key])
            p.pos=(1,9);p.direction=p.wanted=(1,0);p.safe=100
            if name!='normal':p.effects[name]=100
            count=0
            for _ in range(60):
                old=p.pos;g.update(1/60)
                count+=p.pos!=old
            moves[name]=count
            self.assertEqual(count,expected,(name,count))
        self.assertGreater(moves['Slick'],moves['Rush'])

    def test_spawn_and_item_clocks_retain_fractional_remainder(self):
        g=self.clean(1);g.players[0].safe=100
        with patch.object(g,'spawn_item') as spawn:
            for _ in range(180): g.update(1/60)
            self.assertEqual(spawn.call_count,1)
        # Fractional time must remain after each configured interval.
        self.assertAlmostEqual(g.item_clock,0)
        self.assertAlmostEqual(g.item_walk_clock,3 % g.tuning['item_step_seconds'])
        self.assertAlmostEqual(g.foe_clock,3 % g.tuning['ghost_step_seconds'])

    def test_bonus_life_cannot_silence_another_players_damage(self):
        g=self.clean(2);p,q=g.players
        p.score=9995;p.direction=p.wanted=(1,0)
        g.foes[0]=q.pos;g.foe_modes[0]='roaming'
        # Arrange both events on the next tick, before the ghost moves off q.
        p.clock=g.player_interval(p)-1/60
        sounds=g.update(1/60)
        self.assertEqual([p.lives,q.lives],[4,2])
        self.assertIn('hurt',sounds)
        self.assertEqual(sum(e['event']=='player_hurt' for e in g.ledger.events),1)

    def test_lightning_does_not_apply_effects_to_inactive_stations(self):
        g=Match(0,seed=1);g.join_station(0);p=g.players[0];p.pos=(1,1)
        g.collect(p,'Spark')
        self.assertTrue(all(q.stun==0 for q in g.players if not q.joined))
        self.assertTrue(g.join_station(1));q=g.players[1];q.pos=(2,1)
        g.collect(p,'Spark');self.assertEqual(q.stun,2)

    def test_simultaneous_carried_ghosts_award_exactly_one_damage(self):
        g=self.clean(2);p,q=g.players
        p.effects={'Lure':7}
        g.foes=[q.pos]*4;g.foe_modes=['carried']*4
        g.foe_carriers={i:0 for i in range(4)}
        g.combat()
        self.assertEqual(q.lives,2);self.assertEqual(p.score,300)
        self.assertEqual(sum(e['event']=='carried_ghost_hit' for e in g.ledger.events),1)
        self.assertEqual(g.ledger.totals()[1],300)

    def test_all_power_refresh_and_damage_clear_for_both_station_orders(self):
        for station in (0,7):
            for name in ITEMS:
                g=Match(0,seed=1);g.join_station(station);p=g.players[station]
                p.entry=p.safe=0;p.pos=(5,1)
                g.collect(p,name);g.collect(p,name)
                self.assertEqual(p.score,2*{'Crown':100,'Titan':1000}.get(name,75))
                if name in ('Heart','Spark','Quake'):
                    self.assertNotIn(name,p.effects)
                else:
                    expected=g.tuning['durations'][name]
                    self.assertEqual(p.effects[name],expected)
                if name=='Titan':p.effects.pop('Titan')
                self.assertTrue(g.hurt(p))
                self.assertEqual(p.effects,{})
                self.assertEqual(p.stun,0)

    def test_giant_locator_rings_clear_score_text_at_every_station(self):
        app=App(simulate_controllers=True)
        try:
            for theme in range(4):
                for count in (1,2,8):
                    app.count=count;app.theme=theme;app.start()
                    for value in (0,999999,999999999):
                        for p in app.match.players:
                            p.effects={'Titan':7};p.locate_remaining=2 if p.joined else 0;p.score=value
                        expected={center(app.match.arena.spawns[p.idx]) for p in app.match.players}
                        circles=[];draw_circle=pg.draw.circle
                        def capture(surface,color,position,radius,width=0,**kwargs):
                            if width==3 and tuple(position) in expected:
                                circles.append((tuple(position),radius))
                            return draw_circle(surface,color,position,radius,width,**kwargs)
                        with patch.object(pg.draw,'circle',capture):app.draw()
                        self.assertEqual(len(circles),count)
                        rects=[station_hud(app.match.arena.spawns[p.idx],p.score)['score']
                               for p in app.match.players]
                        for (x,y),radius in circles:
                            self.assertLessEqual(radius,44)
                            ring=pg.Rect(x-radius-2,y-radius-2,radius*2+4,radius*2+4)
                            self.assertFalse(any(ring.colliderect(r) for r in rects))
        finally:pg.quit()


if __name__=='__main__':unittest.main(verbosity=2)
