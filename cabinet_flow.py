"""Deterministic per-station continuation windows for the original adaptation.

A 10-second default plus one-second reveal delay is an estimate, not a measured cabinet constant. Payment,
score restoration and final session settlement belong to the caller. Advancing
only during simulation play makes pause/guide time behavior explicit.
"""
import math


class ContinueOffers:
    def __init__(self, seconds=10., delay=1.):
        if type(seconds) not in (int,float) or not math.isfinite(seconds) or not 0<=seconds<=60:
            raise ValueError('Continue seconds must be finite and between0 and60')
        if type(delay) not in (int,float) or not math.isfinite(delay) or not 0<=delay<=5:
            raise ValueError('Continue delay must be finite and between0 and5')
        self.seconds=float(seconds)
        self.delay=float(delay)
        self._offers={}
        self._delays={}

    @staticmethod
    def _station(idx):
        if type(idx) is not int or not 0<=idx<8:
            raise ValueError('Station must be an integer0..7')

    @property
    def active(self):
        return bool(self._offers)

    def open(self, idx):
        self._station(idx)
        if self.seconds==0 or idx in self._offers:return False
        self._offers[idx]=self.seconds
        self._delays[idx]=self.delay
        return True

    def advance(self, dt):
        if type(dt) not in (int,float) or not math.isfinite(dt) or dt<0:
            raise ValueError('Continue elapsed time must be finite and nonnegative')
        expired=[]
        for idx,remaining in list(self._offers.items()):
            delay=self._delays[idx]
            self._delays[idx]=max(0.,delay-dt)
            if self._delays[idx]<=1e-10:self._delays[idx]=0.
            remaining-=max(0.,dt-delay)
            if remaining<=1e-10:
                del self._offers[idx];del self._delays[idx];expired.append(idx)
            else:self._offers[idx]=remaining
        return sorted(expired)

    def remaining(self, idx):
        self._station(idx)
        return self._offers.get(idx,0.)

    def pending(self, idx):
        self._station(idx)
        return self._delays.get(idx,0.)>0

    def can_accept(self, idx):
        return self.remaining(idx)>0 and not self.pending(idx)

    def accept(self, idx):
        self._station(idx)
        if not self.can_accept(idx):return False
        del self._offers[idx]
        del self._delays[idx]
        return True

    def clear(self):
        self._offers.clear()
        self._delays.clear()

    def snapshot(self):
        return {'seconds':self.seconds,'delay':self.delay,
                'offers':[[idx,value,self._delays[idx]] for idx,value in sorted(self._offers.items())]}
