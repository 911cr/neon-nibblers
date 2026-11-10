"""Exercise the real Windows SDL message pump, targeting only this process's game HWND."""
import ctypes,os,sys,json,time
from ctypes import wintypes as wt
from pathlib import Path
root=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(root))
from turn_drill import TurnDrill,pg
folder=root/'work'/('auto-keyboard-'+time.strftime('%Y%m%d-%H%M%S'));folder.mkdir(parents=True)
a=TurnDrill(folder);pg.display.set_caption('Neon Nibblers | Automated input test')
user=ctypes.WinDLL('user32',use_last_error=True)
post=user.PostMessageW;post.argtypes=[wt.HWND,wt.UINT,wt.WPARAM,wt.LPARAM];post.restype=wt.BOOL
owner=user.GetWindowThreadProcessId;owner.argtypes=[wt.HWND,ctypes.POINTER(wt.DWORD)];owner.restype=wt.DWORD
hwnd=pg.display.get_wm_info()['window']
def key(vk,pressed):
 pid=wt.DWORD();owner(hwnd,ctypes.byref(pid));assert pid.value==os.getpid()
 sc=user.MapVirtualKeyW(vk,0);flags=1|(sc<<16)|((vk in (39,40))<<24)
 if not pressed:flags|=0xc0000000
 if not post(hwnd,0x100 if pressed else 0x101,vk,flags):raise ctypes.WinError(ctypes.get_last_error())
normal=[('both',gap) for gap in (0,0,0,100,100,185,185,235,235,235)]
cases=normal+[('omit_S',185),('late',0)];results=[]
try:
 for mode,gap in cases:
  if results:a.new_round()
  start=time.monotonic();last=start;armed=False;tapped=False
  while a.stage!='done':
   a.clock.tick(60);now=time.monotonic();dt=min(.25,now-last);last=now
   if now-start>8:raise RuntimeError('Timed out in '+a.stage)
   a.events();assert a.running;a.inputs();a.advance(dt);a.draw(dt)
   if a.stage=='ready' and not armed:
    key(39,True);key(68,True);armed=True
   if a.stage=='go' and not tapped and a.match.elapsed>=(1.3 if mode=='late' else .45):
    key(40,True)
    if mode!='omit_S':key(83,True)
    time.sleep(.008);key(40,False)
    if mode!='omit_S':key(83,False)
    time.sleep(gap/1000);tapped=True
  for vk in (39,68):key(vk,False)
  pg.time.wait(20);a.events()
  rows=[json.loads(line) for line in a.log_path.read_text().splitlines()];rows=[r for r in rows if r['round']==a.round_no]
  final=next(r['results'] for r in reversed(rows) if r['event']=='result');expected={'both':['Down turn taken','S turn taken'],'omit_S':['Down turn taken','no S key-down received'],'late':['Down received past junction','S received past junction']}[mode]
  press=[r for r in rows if r['event']=='key' and r['edge']=='down' and r['key'] in ('Down','S')]
  item=dict(round=a.round_no,mode=mode,inserted_delay_ms=gap,outcomes=final,passed=final==expected,presses=[(r['key'],r['frame_ms'],r['id']) for r in press]);results.append(item)
  print(item,flush=True)
finally:
 a.log.close();pg.quit();(folder/'summary.json').write_text(json.dumps({'method':'Windows key messages posted only to the SDL game window owned by this test. Held state and fixed-step movement were real game code.','trace':str(folder/'turns.jsonl'),'trials':results},indent=2))
assert len(results)==len(cases) and all(r['passed'] for r in results)
