"""Independently synthesized event cues; no commercial recordings or melodies."""
import math
from array import array
import pygame as pg

PATTERNS={
 'dot':((660,440),.045), 'power':((440,660,880),.20),
 'hurt':((220,165,90),.30), 'ghost':((740,990,1320),.16),
 'rival':((330,660,990,1320),.25), 'join':((392,523,784),.24),
 'find':((880,1174),.10), 'bonus':((523,659,784,1047),.35),
 'stage':((392,523,659,784),.40), 'finish':((784,659,523,1047),.60)}
EVENT_CUES={'match_start':'join','station_join':'join','locate':'find',
 'dot':'dot','pickup':'power','player_hurt':'hurt','ghost_eaten':'ghost',
 'ghost_burned':'ghost','rival_eaten':'rival','rival_burned':'rival',
 'carried_ghost_hit':'rival','bonus_life':'bonus','stage_start':'stage','match_end':'finish'}

def synthesize(name,rate=44100,channels=2):
    notes,duration=PATTERNS[name];samples=array('h')
    count=int(rate*duration)
    for i in range(count):
        t=i/rate; n=min(len(notes)-1,int(i/count*len(notes)))
        local=(i/count*len(notes))%1
        env=min(1,local*20)*min(1,(1-local)*5)
        fundamental=math.sin(2*math.pi*notes[n]*t)
        harmonic=.22*math.sin(4*math.pi*notes[n]*t)
        value=int(2800*env*(fundamental+harmonic))
        samples.extend([value]*channels)
    return samples.tobytes()

class ArcadeAudio:
    def __init__(self):
        self.sounds={};self.cursor=0;self.ledger=None
        try:
            if not pg.mixer.get_init():pg.mixer.init(44100,-16,2)
            rate,fmt,channels=pg.mixer.get_init()
            if fmt!=-16:return
            pg.mixer.set_num_channels(max(12,pg.mixer.get_num_channels()))
            self.sounds={name:pg.mixer.Sound(buffer=synthesize(name,rate,channels)) for name in PATTERNS}
        except pg.error:pass

    def silence(self):
        if not pg.mixer.get_init():return
        try:
            for lane in range(min(10,pg.mixer.get_num_channels())):pg.mixer.Channel(lane).stop()
        except pg.error:pass

    def consume(self,ledger,muted=False):
        if self.ledger is not ledger:self.ledger=ledger;self.cursor=0
        cues=[EVENT_CUES[e['event']] for e in ledger.events[self.cursor:] if e['event'] in EVENT_CUES]
        self.cursor=len(ledger.events)
        if muted:
            self.silence();return []
        # Independent lanes keep simultaneous feedback audible without dozens
        # of dot voices drowning out a death, bonus or match transition.
        lanes={'dot':0,'power':1,'hurt':2,'ghost':3,'rival':4,'join':5,
               'find':6,'bonus':7,'stage':8,'finish':9}
        if not pg.mixer.get_init():return cues
        try:
            for name in dict.fromkeys(cues):
                if name in self.sounds:pg.mixer.Channel(lanes[name]).play(self.sounds[name])
        except pg.error:pass
        return cues
