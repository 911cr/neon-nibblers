"""Presentation-path geometry against every authored maze, without SDL."""
import copy
import unittest
from types import SimpleNamespace
from effect_paths import corridor_segments
from map_library import get_map

O=(50,50)
def point(c):return (O[0]+c[0]*20+10,O[1]+c[1]*20+10)

class EffectPaths(unittest.TestCase):
    def arena(self,index):
        m=get_map(index)
        return SimpleNamespace(lanes=set(m.lanes),portals=m.portals)

    def test_all_maps_every_neighbor_and_corner(self):
        for index in range(4):
            a=self.arena(index);corners=0
            for x,y in a.lanes:
                for dx,dy in ((1,0),(0,1),(-1,0),(0,-1)):
                    b=(x+dx,y+dy)
                    if b not in a.lanes:continue
                    first=point((x,y));last=point(b)
                    self.assertEqual(corridor_segments(a,[first,last]),[(first,last,(dx,dy))])
                    c=(b[0]-dy,b[1]+dx)
                    if c in a.lanes:
                        segments=corridor_segments(a,[first,last,point(c)])
                        self.assertEqual(len(segments),2)
                        self.assertEqual(segments[0][1],segments[1][0]);corners+=1
            self.assertGreater(corners,0)

    def test_all_maps_wall_links_and_gates_are_rejected(self):
        for index in range(4):
            a=self.arena(index);m=get_map(index);checked=0
            for x,y in a.lanes:
                for dx,dy in ((1,0),(0,1)):
                    if (x+dx,y+dy) not in a.lanes:
                        self.assertEqual(corridor_segments(a,[point((x,y)),point((x+2*dx,y+2*dy))]),[])
                        checked+=1
            self.assertGreater(checked,0)
            for spawn,entry in zip(m.spawns,m.entries):
                self.assertEqual(corridor_segments(a,[point(spawn),point(entry)]),[])

    def test_all_maps_portals_split_both_directions(self):
        for index in range(4):
            a=self.arena(index)
            for row in a.portals:
                for start,end,direction in ((58,0,(1,0)),(0,58,(-1,0))):
                    seg=corridor_segments(a,[point((start,row)),point((end,row))])
                    self.assertEqual(len(seg),2)
                    self.assertTrue(all(s[2]==direction for s in seg))
                    self.assertEqual(sum(abs(s[1][0]-s[0][0]) for s in seg),20)

    def test_fractional_origin_coalescing_and_no_input_mutation(self):
        a=SimpleNamespace(lanes={(x,1) for x in range(5)},portals=())
        points=[(64.5,80),point((1,1)),point((2,1)),point((3,1))]
        before=copy.deepcopy((a,points))
        self.assertEqual(corridor_segments(a,points),[(points[0],points[-1],(1,0))])
        self.assertEqual(a.lanes,before[0].lanes);self.assertEqual(points,before[1])

    def test_diagonal_and_offcenter_links_never_repaired(self):
        a=SimpleNamespace(lanes={(x,y) for x in range(4) for y in range(4)},portals=())
        self.assertEqual(corridor_segments(a,[point((1,1)),point((2,2))]),[])
        self.assertEqual(corridor_segments(a,[(75,75),(95,75)]),[])
        self.assertEqual(corridor_segments(a,[(float('nan'),80),(80,80)]),[])

    def test_portal_edge_and_missing_half(self):
        a=SimpleNamespace(lanes={(0,1),(58,1)},portals=(1,))
        self.assertEqual(corridor_segments(a,[(50,80),(1220,80)]),[((1230,80),(1220,80),(-1,0))])
        a.lanes.remove((58,1))
        self.assertEqual(corridor_segments(a,[point((0,1)),point((58,1))]),[])

    def test_nonportal_and_different_rows_do_not_wrap(self):
        a=SimpleNamespace(lanes={(0,1),(58,1),(58,2)},portals=(2,))
        self.assertEqual(corridor_segments(a,[point((0,1)),point((58,1))]),[])
        self.assertEqual(corridor_segments(a,[point((0,1)),point((58,2))]),[])

    def test_float_drift_still_outputs_exact_axis_segments(self):
        a=SimpleNamespace(lanes={(0,1),(1,1)},portals=())
        segments=corridor_segments(a,[(60,80),(80,80+1e-8)])
        self.assertEqual(segments,[((60,80),(80,80),(1,0))])

    def test_invalid_gap_never_bridges_and_reversal_keeps_direction(self):
        a=SimpleNamespace(lanes={(x,1) for x in range(5)},portals=())
        pts=[point((0,1)),point((1,1)),point((1,2)),point((2,1)),point((3,1)),point((2,1))]
        seg=corridor_segments(a,pts)
        self.assertEqual(len(seg),3)
        self.assertEqual([s[2] for s in seg],[(1,0),(1,0),(-1,0)])

if __name__=='__main__':unittest.main()
