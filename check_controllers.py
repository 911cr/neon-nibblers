"""Observe real SDL controller input; never substitutes synthetic test events."""
import argparse
import json
import platform
import time
from pathlib import Path
import pygame as pg


def observe_controls(record, axes, hats, buttons):
    x=axes[0] if axes else 0
    y=axes[1] if len(axes)>1 else 0
    for hx,hy in hats:
        if hx or hy: x,y=hx,-hy
    for name,seen in [('left',x<-.6),('right',x>.6),('up',y<-.6),('down',y>.6),('button',any(buttons))]:
        if seen: record['observed'][name]=True


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--expected',type=int,choices=range(1,9),default=8)
    parser.add_argument('--seconds',type=int,default=120)
    parser.add_argument('--output',default='controller_check_results.json')
    args=parser.parse_args()
    pg.init(); screen=pg.display.set_mode((1050,620)); pg.display.set_caption('Neon Nibblers controller verification')
    font=pg.font.Font(None,27); clock=pg.time.Clock()
    active={}; records=[]; changes=[]
    def attach(index):
        joy=pg.joystick.Joystick(index); iid=joy.get_instance_id()
        if iid in active: return
        record={'name':joy.get_name(),'guid':joy.get_guid(),'instance_id':iid,'observed':dict.fromkeys(('left','right','up','down','button'),False)}
        records.append(record); active[iid]=(joy,record)
    for i in range(pg.joystick.get_count()): attach(i)
    start=time.monotonic(); running=True
    while running and time.monotonic()-start<args.seconds:
        for event in pg.event.get():
            if event.type==pg.QUIT or event.type==pg.KEYDOWN and event.key==pg.K_ESCAPE: running=False
            elif event.type==pg.JOYDEVICEADDED:
                attach(event.device_index); changes.append({'action':'attached','seconds':round(time.monotonic()-start,2)})
            elif event.type==pg.JOYDEVICEREMOVED:
                active.pop(event.instance_id,None); changes.append({'action':'removed','seconds':round(time.monotonic()-start,2)})
        screen.fill((8,12,21))
        lines=['Move every stick / D-pad in all four directions, then press a button.',
               f'Expected: {args.expected} | Connected: {len(active)} | Escape saves and exits.',
               'This observes device input. It does not certify gameplay or eight humans.','']
        for joy,record in active.values():
            observe_controls(record,[joy.get_axis(i) for i in range(joy.get_numaxes())],
                             [joy.get_hat(i) for i in range(joy.get_numhats())],
                             [joy.get_button(i) for i in range(joy.get_numbuttons())])
            marks='  '.join(k+(' OK' if v else ' --') for k,v in record['observed'].items())
            lines.append(record['name'][:38]+'  '+marks)
        if not active: lines.append('No SDL controllers detected. Connect the controllers to this computer.')
        for i,line in enumerate(lines): screen.blit(font.render(line,True,(225,232,244)),(22,24+i*39))
        pg.display.flip(); clock.tick(30)
    verified=[r for _,r in active.values() if all(r['observed'].values())]
    result={'platform':platform.system(),'expected_controllers':args.expected,'connected_at_end':len(active),
            'controllers_with_all_inputs_observed':len(verified),'input_check_passed':len(verified)>=args.expected,
            'physical_hardware_confirmation_required':True,'devices':records,'hotplug_events':changes,
            'elapsed_seconds':round(time.monotonic()-start,2)}
    Path(args.output).write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2)); pg.quit()


if __name__=='__main__': main()
