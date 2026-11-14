"""Local operator configuration, credits and high scores for our adaptation."""
import json
import os
from pathlib import Path
import time
import math
import errno
from contextlib import contextmanager

DEFAULTS={'starting_lives':3,'bonus_threshold':10000,'match_seconds':180,
          'free_play':True,'attract_sound':True,'fill_bots':True}

def atomic_json(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    temporary=path.with_name(path.name+'.tmp')
    temporary.write_text(json.dumps(value,indent=2),encoding='utf-8')
    temporary.replace(path)

def data_directory():
    if os.environ.get('NEON_NIBBLERS_DATA'):return Path(os.environ['NEON_NIBBLERS_DATA'])
    if os.name=='nt':return Path(os.environ.get('LOCALAPPDATA',Path.home()))/'NeonNibblers'
    return Path(os.environ.get('XDG_DATA_HOME',Path.home()/'.local/share'))/'neon-nibblers'

@contextmanager
def cabinet_session(directory=None):
    """Hold the profile's OS lock from initial load through the final save."""
    directory = Path(directory) if directory is not None else data_directory()
    directory.mkdir(parents=True, exist_ok=True)
    # Keep the same lock file across sessions. Closing the handle (also on a
    # process crash) releases ownership without racing a new process's open.
    with (directory / 'cabinet.lock').open('a+b') as handle:
        try:
            if os.name == 'nt':
                import msvcrt
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            else:
                import fcntl
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as error:
            if error.errno in (errno.EACCES, errno.EAGAIN, errno.EDEADLK):
                raise BlockingIOError('Another game is using this cabinet save folder. '
                                      'Return to that game or choose a different --data-dir.') from error
            raise
        yield CabinetStore(directory)

class CabinetStore:
    def __init__(self,directory=None):
        self.directory=Path(directory) if directory is not None else data_directory()
        self.path=self.directory/'cabinet.json';self.error=''
        self.settings=dict(DEFAULTS);self.credits=0;self.high_scores=[];self.recorded=set()
        try:
            raw=json.loads(self.path.read_text(encoding='utf-8'))
            self.settings=self.validate(raw.get('settings',{}))
            self.credits=max(0,min(999,int(raw.get('credits',0))))
            for row in raw.get('high_scores',[])[:20]:
                if isinstance(row,dict) and type(row.get('score')) is int and row['score']>=0:
                    stamp=float(row.get('time',0))
                    if not math.isfinite(stamp):raise ValueError('Invalid score timestamp')
                    name=''.join(c for c in str(row.get('name','PLAYER')) if c.isprintable())[:24] or 'PLAYER'
                    self.high_scores.append({'name':name,
                        'score':row['score'],'player_id':max(1,min(8,int(row.get('player_id',1)))),
                        'time':stamp, 'session':row.get('session') if isinstance(row.get('session'),str) else None})
            self.high_scores.sort(key=lambda r:(-r['score'],r['time']))
            self.recorded=set(str(x) for x in raw.get('recorded',[])[:100])
        except FileNotFoundError:pass
        except (OSError,ValueError,TypeError,AttributeError):
            self.settings=dict(DEFAULTS);self.credits=0;self.high_scores=[];self.recorded=set()
            self.error='Saved cabinet data could not be read; defaults are active.'

    @staticmethod
    def validate(settings):
        result=dict(DEFAULTS)
        for key,low,high in [('starting_lives',1,5),('bonus_threshold',0,1000000),('match_seconds',30,1800)]:
            value=settings.get(key,result[key])
            if type(value) is not int or not (low<=value<=high or key=='match_seconds' and value==0):raise ValueError('Invalid '+key)
            result[key]=value
        for key in ('free_play','attract_sound','fill_bots'):
            value=settings.get(key,result[key])
            if type(value) is not bool:raise ValueError('Invalid '+key)
            result[key]=value
        return result

    def save(self):
        try:
            atomic_json(self.path,{'schema_version':1,'settings':self.settings,'credits':self.credits,
                'high_scores':self.high_scores[:20],'recorded':sorted(self.recorded)[-100:]})
            self.error='';return True
        except OSError:
            self.error='Cabinet data could not be saved. Check the data-folder permissions.';return False

    def configure(self,settings):
        previous=self.settings;self.settings=self.validate(settings)
        if self.save():return True
        self.settings=previous;return False

    def add_credit(self):
        previous=self.credits;self.credits=min(999,self.credits+1)
        if self.save():return True
        self.credits=previous;return False

    def pay(self,count):
        if type(count) is not int or not 1<=count<=8:raise ValueError('Station count must be1..8')
        if self.settings['free_play']:return True
        if self.credits<count:return False
        previous=self.credits;self.credits-=count
        if self.save():return True
        self.credits=previous;return False

    def record(self,match,token):
        if not match.over or token in self.recorded:return False
        return self.record_rows(match.rankings(),token)

    def record_rows(self,rows,token):
        if token in self.recorded:return False
        previous=list(self.high_scores)
        now=time.time()
        for row in rows:
            self.high_scores.append({'name':f"P{row['player_id']}",'score':row['score'],
                                    'player_id':row['player_id'],'time':now,'session':token})
        self.high_scores.sort(key=lambda r:(-r['score'],r['time']))
        self.high_scores=self.high_scores[:20];self.recorded.add(token)
        if self.save():return True
        self.high_scores=previous;self.recorded.discard(token);return False

    def rename_score(self, token, player_id, initials):
        """Rename only this session's qualifying row; failed writes roll back."""
        if not isinstance(initials,str) or len(initials)!=3 or any(c not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' for c in initials):
            raise ValueError('Initials must be three A-Z letters')
        matches=[i for i,row in enumerate(self.high_scores)
                 if row.get('session')==token and row['player_id']==player_id]
        if not matches:
            self.error='This score has no saved qualifying entry.';return False
        previous=self.high_scores
        self.high_scores=[dict(row) for row in previous]
        for i in matches:self.high_scores[i]['name']=initials
        if self.save():return True
        self.high_scores=previous;return False

def spectator_view(match,phase,map_name=''):
    return {'schema_version':1,'updated':time.time(),'phase':phase,'map':map_name,
            'stage':match.stage if match else 0,'remaining':match.time if match else 0,
            'timed':match.rules['match_seconds']>0 if match else False,
            'ranking':match.rankings() if match else []}
