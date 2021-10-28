import abc
import time


class TimePiece(metaclass=abc.ABCMeta):
    def __init__(self, initial_value=None):
        self.start_time = self.current_time = initial_value

    @abc.abstractmethod
    def tick(self):
        return NotImplemented


class GameClock(TimePiece):
    def __init__(self):
        super().__init__(initial_value=time.time())
        self.mark = None

    def tick(self):
        self.current_time = time.time()

    @property
    def elapsed(self):
        return self.current_time - self.start_time

    @property
    def elapsed_since_mark(self):
        return (self.mark - self.start_time) if self.mark else 0

    def set_mark(self):
        self.mark = time.time()

    def clear_mark(self):
        self.mark = None


class StopWatch(TimePiece):
    def __init__(self, max_time=1):
        super().__init__()
        self.max_time = max_time
        self.done = False

    def start(self):
        self.start_time = time.time()

    def tick(self):
        self.current_time = time.time()
        if (self.current_time - self.start_time) >= self.max_time:
            self.done = True


__all__ = ['GameClock', 'StopWatch']
