"""Session-stable input ownership. Never renumber a surviving controller."""
from enum import Enum


class Phase(str, Enum):
    ATTRACT = 'attract'
    PLAYING = 'playing'
    PAUSED = 'paused'
    GUIDE = 'guide'
    RESULTS = 'results'


def phase_for(match, guide=False):
    if guide: return Phase.GUIDE
    if match is None: return Phase.ATTRACT
    if match.over: return Phase.RESULTS
    if match.paused: return Phase.PAUSED
    return Phase.PLAYING


class StationBindings:
    """Live SDL instance IDs own stations; lost stations remain reserved.

    A unique GUID can reclaim a disconnected station. Identical controllers
    require explicit pairing, because a GUID identifies a model, not a unit.
    No claim of persistent physical identity is made without a serial number.
    """
    def __init__(self):
        self.by_instance = {}
        self.guids = {}
        self.reserved = {}
        self.disconnected = {}

    def sync(self, devices):
        for iid in set(self.by_instance)-set(devices):
            slot=self.by_instance.pop(iid)
            self.reserved[slot]=self.guids.pop(iid, '')
            self.disconnected[iid]=slot
        for iid,joy in devices.items():
            if iid in self.by_instance: continue
            guid=joy.get_guid() if hasattr(joy,'get_guid') else ''
            matches=[s for s,g in self.reserved.items() if guid and g==guid]
            same_live=guid in self.guids.values()
            same_new=sum((j.get_guid() if hasattr(j,'get_guid') else '')==guid
                         for j in devices.values())>1
            previous=self.disconnected.get(iid)
            if previous is not None and previous in self.reserved:
                slot=previous
            elif len(matches)==1 and not same_live and not same_new:
                slot=matches[0]
            elif matches:
                continue  # ambiguous reconnect: ask for explicit station pairing
            else:
                free=set(range(8))-set(self.by_instance.values())-set(self.reserved)
                if not free: continue
                slot=min(free)
            self.bind(iid,slot,guid)

    def bind(self, iid, slot, guid=''):
        if slot not in range(8): raise ValueError('Station must be 0..7')
        if any(i!=iid and s==slot for i,s in self.by_instance.items()):
            return False
        old=self.by_instance.get(iid)
        if old is not None and old!=slot: self.reserved.pop(old,None)
        self.by_instance[iid]=slot; self.guids[iid]=guid
        self.disconnected.pop(iid,None)
        self.reserved.pop(slot,None)
        return True

    def device_for(self, slot, devices):
        return next((devices[i] for i,s in self.by_instance.items()
                     if s==slot and i in devices),None)
