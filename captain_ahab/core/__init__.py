import logging
from typing import Coroutine
from queue import PriorityQueue, Empty
from ..utils import Singleton
from ..utils.constants import SAMPLE_X, SAMPLE_Y, SAMPLE_W, SAMPLE_H
from .actions import *
from .trainers import SightTrainer, MovementTrainer, VoiceTrainer, FishingTrainer
from .angler import Angler
from .sight import Eyes
from .mobility import Legs
from .voice import Voice
from .cortex import Cortex
from .liaison import AnimaLiaison


logger = logging.getLogger(__name__)


class CaptainAhab(metaclass=Singleton):
    """
    CaptainAhab is an automaton designed to streamline fishing activities in New World

    The author is not responsible for suspensions or bans as the result of the use of this software or any of its
    components.
    """

    @classmethod
    def run(cls, x=None, y=None, w=None, h=None):
        x = x or SAMPLE_X
        y = y or SAMPLE_Y
        w = w or SAMPLE_W
        h = h or SAMPLE_H
        captain = cls(x, y, w, h)
        AnimaLiaison(captain=captain).dispatch()

    def __init__(self, visual_x, visual_y, visual_width, visual_height):
        self.action_queue = PriorityQueue()
        self.action_wait_timeout = 0.5
        self.visual_field = (visual_x, visual_y, visual_width, visual_height)
        self.eyes = None
        self.legs = None
        self.voice = None
        self.angler = None
        self.cortex = Cortex()
        logger.debug('CaptainAhab lives')
        self.__initialized = False
        self.__dead = False

    @property
    def ready(self):
        return self.__initialized

    @property
    def alive(self):
        return not self.__dead

    def kill(self):
        logger.info(f'CaptainAhab has died')
        self.__dead = True

    async def update(self):
        if self.__dead:
            return

        await self.cortex.update()

    async def train(self):
        """ Training will initialize _eyes/_legs/_voice, etc """

        logger.debug('CaptainAhab is going in for training')
        for trainer_cls in (SightTrainer, MovementTrainer, VoiceTrainer, FishingTrainer):
            trainer = trainer_cls(captain=self)
            trainer.train()

        logger.debug('CaptainAhab has finished training')
        self.__initialized = True

    async def perform_next_action(self) -> Coroutine:
        try:
            queued_item = self.action_queue.get(timeout=self.action_wait_timeout)
            result = queued_item.action.invoke()
            self.action_queue.task_done()
            return result
        except Empty:
            raise
        except Exception:
            logger.exception(f'Error during queued task')
            self.kill()

    def purge_queue(self):
        qsize = self.action_queue.qsize()

        with self.action_queue.mutex:
            self.action_queue.queue.clear()

        logger.debug(f'Purged queue: {qsize}')

    def queue_action(self, action_cls, priority=None):
        action = action_cls(captain=self)
        self.action_queue.put(PrioritizedAction(priority=priority or action_cls.default_priority,
                                                action=action))
        logger.debug(f'Queued {action}')

    def queue_actions(self, action_list, priority=None):
        for action_cls in action_list:
            self.queue_action(action_cls=action_cls, priority=priority)

    def cast(self):
        self.queue_actions([CastLine, Wait])

    def hook(self):
        self.queue_action(HookFish)

    def reel(self):
        self.queue_action(ReelIn)

    def release(self):
        self.queue_actions([ReleaseTension, Wait])

    def wait(self):
        self.queue_action(Wait)

    def repair(self):
        self.queue_action(RepairGear)

    def bait(self):
        self.queue_action(EquipBait)

    def shift(self):
        self.queue_action(ShiftPosition)

    def move(self):
        self.queue_actions([Move, Wait])

    def speak(self):
        self.queue_actions([Speak, Wait])

    def look(self):
        self.queue_action(Look)


__all__ = ['CaptainAhab']
