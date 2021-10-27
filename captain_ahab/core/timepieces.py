import abc


class TimePiece(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def tick(self):
        return NotImplemented


class GameClock(TimePiece):
    def tick(self):
        pass


class StopWatch(TimePiece):
    def __init__(self, max_time=1):
        self._done = False

    def tick(self):
        pass
