import time

class Aggregator:
    def __init__(self, n_seconds=30):
        self.n_seconds=n_seconds
        self.last = time.time()
    def check(self):
        now = time.time()
        if (now - self.last)>self.n_seconds:
            self.last = now
            return True
        return False

# For doing video
class AggregatorReplay:
    def __init__(self, n_frames=3):
        self.n=n_frames
        self.n_frames = n_frames
    def check(self):
        self.n-=1
        if self.n==0:
            self.n=self.n_frames
            return True
        return False