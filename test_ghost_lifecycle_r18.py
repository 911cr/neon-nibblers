"""Ghost lifecycle/cadence QA for the authored R18 simulation policy."""
import os
os.environ.setdefault('SDL_VIDEODRIVER','dummy');os.environ.setdefault('SDL_AUDIODRIVER','dummy')
import unittest
from unittest.mock import patch
from game import Match,DIRS

class GhostLifecycleR18(unittest.TestCase):
    def game(self,theme=0):
        g=Match(1,theme,seed=314)
        g.players[0].effects={'Veil':1000}
        g.foe_release=[1000]*4
        return g
    def test_all_ghosts_return_through_door_and_leave_without_teleport(self):
        for theme in range(4):
            for ghost in range(4):
                for start in ((0,self.game(theme).arena.portals[0]),(58,self.game(theme).arena.portals[-1]),(1,1)):
                    g=self.game(theme);g.foes[ghost]=start;g.foe_modes[ghost]='eyes'
                    seen=set();home=g.arena.homes[ghost];door=g.arena.door;exit=g.arena.exit
                    protected={(door[0],y)for y in range(exit[1],home[1]+1)}
                    protected.update((x,home[1])for x in range(min(home[0],door[0]),max(home[0],door[0])+1))
                    for tick in range(220):
                        old=g.foes[ghost];g.update_foes(g.tuning['ghost_step_seconds']);new=g.foes[ghost]
                        seen.add(g.foe_modes[ghost])
                        self.assertTrue(new==old or new in [g.arena.step(old,d) for d in DIRS],(theme,ghost,old,new))
                        self.assertIn(new,g.arena.lanes|protected)
                        if g.foe_modes[ghost]=='house':self.assertEqual(new,home)
                        if g.foe_modes[ghost]=='roaming':break
                    self.assertEqual(g.foe_modes[ghost],'roaming')
                    self.assertTrue({'entering','house','leaving','roaming'}<=seen)
    def cadence(self,theme,fps,quake=False,smoke=False,stun=False):
        g=self.game(theme);g.foes[0]=sorted(g.arena.lanes)[30];g.foe_modes[0]='roaming';g.foe_previous[0]=g.foes[0]
        g.quake=100 if quake else 0;g.smoke={c:100 for c in g.arena.lanes}if smoke else {}
        g.foe_zapped[0]=100 if stun else 0
        duration=g.tuning['ghost_step_seconds']*4;elapsed=0;steps=0
        while elapsed<duration-1e-10:
            dt=min(1/fps,duration-elapsed);old=g.foes[0];g.update_foes(dt);elapsed+=dt
            steps+=old!=g.foes[0]
        return steps
    def test_slow_stack_and_local_stun_consistent_across_frame_rates(self):
        for theme in range(4):
            for fps in (30,60,144):
                self.assertEqual(self.cadence(theme,fps),4)
                self.assertEqual(self.cadence(theme,fps,quake=True),2)
                self.assertEqual(self.cadence(theme,fps,smoke=True),2)
                self.assertEqual(self.cadence(theme,fps,quake=True,smoke=True),1)
                self.assertEqual(self.cadence(theme,fps,stun=True),0)
    def test_protected_return_ignores_slow_and_stun_as_documented(self):
        for theme in range(4):
            g=self.game(theme);g.foes[0]=(1,1);g.foe_modes[0]='eyes'
            g.foe_zapped[0]=100;g.foe_stun=100;g.quake=100;g.smoke={c:100 for c in g.arena.lanes}
            for _ in range(150):
                g.update_foes(g.tuning['ghost_step_seconds'])
                if g.foe_modes[0]=='house':break
            self.assertEqual(g.foe_modes[0],'house');self.assertEqual(g.foes[0],g.arena.homes[0])
    def test_veil_suppresses_chase_but_does_not_freeze_roaming(self):
        for theme in range(4):
            g=self.game(theme);g.foes[0]=(1,1);g.foe_modes[0]='roaming';g.foe_previous[0]=g.foes[0]
            with patch.object(g,'lane_distances',side_effect=AssertionError('Invisible target tracked')):
                g.update_foes(g.tuning['ghost_step_seconds'])
            self.assertNotEqual(g.foes[0],(1,1));self.assertIn(g.foes[0],g.arena.lanes)
    def test_all_power_contact_categories_and_protected_modes(self):
        # Chosen adaptation contact policy, not a claim about unknown DX stacking.
        for theme in range(4):
            for power in ('Crown','Titan','Lure','Rush','Mist','Slick','Spark','Veil','Flare','Quake','Heart'):
                g=self.game(theme);p=g.players[0];p.pos=(1,1);p.safe=0;p.entry=0;p.effects={power:3}
                g.foes[0]=p.pos;g.foe_modes[0]='roaming';lives=p.lives
                g.combat()
                with self.subTest(map=theme,power=power):
                    if power in ('Crown','Titan'):
                        self.assertEqual(g.foe_modes[0],'eyes');self.assertEqual(p.lives,lives)
                    elif power=='Lure':
                        self.assertEqual(g.foe_modes[0],'carried');self.assertEqual(g.foe_carriers[0],p.idx)
                    else:self.assertEqual(p.lives,lives-1)
            for mode in ('house','leaving','eyes','entering'):
                g=self.game(theme);p=g.players[0];p.pos=(1,1);p.safe=0;p.effects={'Crown':3}
                g.foes[0]=p.pos;g.foe_modes[0]=mode;score=p.score;lives=p.lives
                g.combat()
                self.assertEqual((p.score,p.lives,g.foe_modes[0]),(score,lives,mode))

    def test_mixed_slow_expiry_never_bursts_or_leaves_lanes(self):
        for theme in range(4):
            g=self.game(theme);g.foes[0]=(1,1);g.foe_modes[0]='roaming';g.foe_previous[0]=g.foes[0]
            g.foe_ticks[0]=100 # accumulated house/recovery history
            times=[]
            for tick in range(240):
                g.quake=1 if tick<35 else 0
                g.smoke={c:1 for c in g.arena.lanes}if tick<57 else {}
                if tick==80:g.foe_zapped[0]=.5
                old=g.foes[0];g.update_foes(1/60)
                if old!=g.foes[0]:times.append((tick+1)/60)
                self.assertIn(g.foes[0],g.arena.lanes)
                self.assertTrue(old==g.foes[0]or g.foes[0]in[g.arena.step(old,d)for d in DIRS])
            self.assertGreater(len(times),2)
            self.assertTrue(all(b-a>=g.tuning['ghost_step_seconds']-1e-8 for a,b in zip(times,times[1:])))

if __name__=='__main__':unittest.main()
