"""Optional 720p/60fps H.264 all-map capture with original event audio.

Install Pillow and imageio-ffmpeg only for capture, not for playing.
python record_video.py --players 8 --seconds 6
"""
import os
os.environ['SDL_VIDEODRIVER']='dummy'
os.environ['SDL_AUDIODRIVER']='dummy'
import argparse
import subprocess
import json
import wave
from array import array
from pathlib import Path
import pygame as pg
import imageio_ffmpeg
from game import App, Match
from arcade_audio import EVENT_CUES, synthesize

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--players',type=int,choices=range(1,9),default=8)
    parser.add_argument('--seconds',type=int,default=6)
    parser.add_argument('--untimed',action='store_true',help='Record the optional life-survival mode.')
    args=parser.parse_args()
    if not 1<=args.seconds<=30:parser.error('Seconds per map must be 1..30')
    encoder=imageio_ffmpeg.get_ffmpeg_exe()
    output=Path(__file__).parent/f'gameplay_{args.players}_player.mp4'
    silent=output.with_suffix('.silent.mp4');audio=output.with_suffix('.audio.wav')
    process=subprocess.Popen([encoder,'-v','error','-y','-f','rawvideo','-pix_fmt','rgb24',
        '-s','1280x720','-r','60','-i','-','-an','-c:v','libx264','-preset','fast',
        '-crf','18','-pix_fmt','yuv420p',str(silent)],stdin=subprocess.PIPE)
    app=App(simulate_controllers=True);app.demo=True;app.untimed=args.untimed
    cues=[];scenarios=[]
    try:
        for theme in range(4):
            app.count=args.players;app.theme=theme;app.seed=20+theme;app.start();cursor=0
            for tick in range(args.seconds*60):
                if tick==120:app.station_action(0)
                app.advance(1/60);app.draw(1/60)
                process.stdin.write(pg.image.tobytes(app.canvas,'RGB'))
                names={EVENT_CUES[e['event']] for e in app.match.ledger.events[cursor:] if e['event'] in EVENT_CUES}
                for name in sorted(names):cues.append((theme*args.seconds+tick/60,name))
                cursor=len(app.match.ledger.events)
            scenarios.append({'profile':theme,'seed':app.match.seed,'human_stations':args.players,
                'ai_stations':8-args.players,'actors_automated':True,'rules':app.match.rules,
                'tuning':app.match.tuning,'events':app.match.ledger.events,
                'rankings':app.match.rankings()})
        process.stdin.close()
        if process.wait()!=0:raise RuntimeError('Video encoding failed')
        mixed=array('i',[0])*(4*args.seconds*44100*2)
        pcm={name:array('h',synthesize(name)) for name in {n for _,n in cues}}
        for timestamp,name in cues:
            start=round(timestamp*44100)*2
            for offset,value in enumerate(pcm[name]):
                if start+offset>=len(mixed):break
                mixed[start+offset]+=value
        data=array('h',(max(-32768,min(32767,v)) for v in mixed))
        with wave.open(str(audio),'wb') as file:
            file.setnchannels(2);file.setsampwidth(2);file.setframerate(44100);file.writeframes(data.tobytes())
        subprocess.run([encoder,'-v','error','-y','-i',str(silent),'-i',str(audio),
            '-c:v','copy','-c:a','aac','-b:a','192k','-shortest','-movflags','+faststart',str(output)],check=True)
        output.with_suffix('.json').write_text(json.dumps({'width':1280,'height':720,'fps':60,
            'seconds':args.seconds*4,'scenarios':scenarios},indent=2),encoding='utf-8')
        print(f'Recorded {output.name}:1280x720,60fps,{args.seconds*4}s,original event audio')
    finally:
        pg.quit()
        if process.poll() is None:process.kill();process.wait()
        for temp in (silent,audio):
            if temp.exists():temp.unlink()

if __name__=='__main__':main()
