from .timepieces import StopWatch, GameClock
from ..utils import Singleton


class Cortex(metaclass=Singleton):
    """ Core temporal operations """

    def __init__(self):
        self.clock = GameClock()
        self.timers = {}

    async def update(self):
        self.clock.tick()
        for timer in self.timers.values():
            timer.tick()

    def start_timer(self, name, duration=1):
        if name in self.timers:
            raise ValueError(f'{name} already exists in timers list')

        self.timers[name] = StopWatch(max_time=duration)

    def purge_timer(self, name):
        self.timers.pop(name, None)
