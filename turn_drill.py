"""Local two-person turn drill using the game's SDL input and fixed simulation loop."""
import argparse
import json
import time
from pathlib import Path

import pygame as pg
from cabinet import CabinetStore
from game import App, Match, KEYS, DIRS
from gameplay_tuning import load_tuning


FORWARD = (pg.K_RIGHT, pg.K_d)
TURN = (pg.K_DOWN, pg.K_s)
JUNCTION = (16, 42)  # Golden Rails, top corridor
KEY_NAMES = ({pg.K_RIGHT:'Right', pg.K_LEFT:'Left', pg.K_DOWN:'Down', pg.K_UP:'Up'},
             {pg.K_d:'D', pg.K_a:'A', pg.K_s:'S', pg.K_w:'W'})


class DrillMatch(Match):
    def update(self, dt):
        before = [(p.pos, p.wanted) for p in self.players]
        sounds = super().update(dt)
        self.report_step(before)
        return sounds


class TurnDrill(App):
    def __init__(self, folder):
        folder.mkdir(parents=True, exist_ok=True)
        super().__init__(simulate_controllers=True, cabinet=CabinetStore(folder))
        self.log_path = folder/'turns.jsonl'
        self.log = self.log_path.open('x', encoding='utf-8', buffering=1)
        self.started = time.perf_counter()
        self.round_no = 0
        self.stage = 'ready'
        self.theme = 0
        self.palette_override = 4
        self.tuning = load_tuning(Path(__file__).with_name('tuning.keyboard-playtest.json'))
        self.new_round()
        pg.display.set_caption('Neon Nibblers | Two-player turn test')

    def record(self, event, **data):
        self.log.write(json.dumps(dict(event=event, round=self.round_no,
            ms=round((time.perf_counter()-self.started)*1000), tick=self.match.tick,
            frame_ms=self.clock.get_time(), **data))+'\n')

    def new_round(self):
        self.round_no += 1
        self.match = DrillMatch(2, 0, seed=5, tuning=self.tuning,
                                rules={'fill_bots':False,'match_seconds':0})
        self.match.report_step = self.step_seen
        self.match.foes = []
        self.match.items.clear()
        self.match.players[0].safe = self.match.players[1].safe = 0
        for p,x in zip(self.match.players,JUNCTION):
            p.pos=(x-6,1); p.entry=0; p.clock=0
            p.direction=p.wanted=(1,0)
        self.fixed_accumulator=0
        self.pending_turns.clear(); self.keyboard_pressed.clear()
        self.reset_visuals()
        self.prepare_mazes()
        self.stage='ready'
        self.sequence=0
        self.pending_ids={}
        self.replaced_by={}
        self.taps=[[],[]]
        self.turned=[False,False]
        self.last_held=None
        self.status_notice='Hold together:  Yellow RIGHT ARROW   +   Pink D.   Watch here for TAP NOW.'
        self.record('ready', expected=['Down','S'], hold=['Right','D'], targets=JUNCTION)

    def events(self, events=None):
        for e in pg.event.get() if events is None else events:
            if e.type==pg.QUIT or (e.type==pg.KEYDOWN and e.key==pg.K_ESCAPE):
                if self.stage=='go': self.finish('ended early')
                self.running=False
                continue
            if e.type==pg.WINDOWFOCUSLOST:
                if self.stage=='go':self.finish('focus lost')
                super().events([e]);continue
            if e.type==pg.KEYDOWN and e.key==pg.K_SPACE and self.stage=='done':
                self.new_round(); continue
            if e.type not in (pg.KEYDOWN,pg.KEYUP):continue
            owner=next((n for n,group in enumerate(KEY_NAMES) if e.key in group),None)
            if owner is None or self.stage=='done':continue
            name=KEY_NAMES[owner][e.key]
            down=e.type==pg.KEYDOWN
            fresh=down and e.key not in self.keyboard_pressed and not getattr(e,'repeat',False)
            super().events([e])
            self.sequence+=1
            p=self.match.players[owner]
            received=self.stage=='go' and fresh and owner in self.pending_turns
            self.record('key',id=self.sequence,stage=self.stage,player=owner+1,key=name,
                        edge='down' if down else 'up',fresh=fresh,buffered=received,pos=p.pos,
                        event_timestamp=getattr(e,'timestamp',None))
            if received:
                old=self.pending_ids.get(owner)
                if old is not None:
                    self.replaced_by[old]=name
                    self.record('replaced',player=owner+1,id=old,by=self.sequence,key=name)
                self.pending_ids[owner]=self.sequence
            if e.key==TURN[owner] and down and fresh:
                self.taps[owner].append((self.sequence,self.stage,p.pos))

    def inputs(self):
        super().inputs()
        keys=pg.key.get_pressed()
        held=tuple(tuple(name for key,name in group.items() if keys[key]) for group in KEY_NAMES)
        if self.stage!='done' and held!=self.last_held:
            self.record('held',keys=held);self.last_held=held
        if self.stage=='ready' and all(keys[key] for key in FORWARD):
            self.pending_turns.clear();self.pending_ids.clear()
            for p in self.match.players:p.wanted=(1,0)
            self.stage='go'
            self.status_notice='TAP NOW together:  Yellow DOWN ARROW   +   Pink S.   Keep holding RIGHT and D.'
            self.record('cue')

    def step_seen(self,before):
        for p,(origin,wanted) in zip(self.match.players,before):
            if p.pos==origin:continue
            d=self.pending_turns.get(p.idx)
            accepted=d is not None and p.pos==self.match.arena.step(origin,d)
            self.record('movement',player=p.idx+1,origin=origin,to=p.pos,wanted=wanted,
                        pending=d,id=self.pending_ids.get(p.idx),took_pending=accepted,
                        pending_legal=(self.match.arena.can_enter(self.match.arena.step(origin,d),p) if d else None))
            if accepted:self.pending_ids.pop(p.idx,None)
            if origin==(JUNCTION[p.idx],1) and p.pos==(JUNCTION[p.idx],2):self.turned[p.idx]=True

    def advance(self,dt):
        if self.stage!='go':return []
        sounds=super().advance(dt)
        if self.match.elapsed>=2.4:self.finish('complete')
        return sounds

    def finish(self,reason):
        results=[]
        for n,key in enumerate(('Down','S')):
            attempts=[pos for _,stage,pos in self.taps[n] if stage=='go']
            if self.turned[n]: result=f'{key} turn taken'
            elif reason!='complete':result=f'{key} trial interrupted'
            elif not attempts:
                result=f'{key} tapped before cue' if self.taps[n] else f'no {key} key-down received'
            elif all(pos[0]>JUNCTION[n] for pos in attempts):result=f'{key} received past junction'
            elif self.taps[n][-1][0] in self.replaced_by:
                result=f'{key} replaced by {self.replaced_by[self.taps[n][-1][0]]}'
            elif self.pending_turns.get(n)==(0,1):result=f'{key} still buffered'
            else:result=f'{key} received; see trace'
            results.append(result)
        self.stage='done'
        self.status_notice=f'Yellow: {results[0]}   |   Pink: {results[1]}   |   SPACE to retry'
        self.record('result',reason=reason,results=results)


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--folder',required=True,type=Path)
    app=TurnDrill(parser.parse_args().folder)
    try:app.run()
    finally:app.log.close()
