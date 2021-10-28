import logging
from queue import PriorityQueue
from ..utils import Singleton
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
    def run(cls, x, y, w, h):
        operator = AnimaLiaison(captain=cls(x, y, w, h))
        operator.dispatch()

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
        self.dead = False

    @property
    def ready(self):
        return self.__initialized

    async def update(self):
        await self.cortex.update()
        await self.eyes.look()

    async def train(self):
        """ Training will initialize _eyes/_legs/_voice, etc """

        logger.debug('CaptainAhab is going in for training')
        for trainer_cls in (SightTrainer, MovementTrainer, VoiceTrainer, FishingTrainer):
            trainer = trainer_cls(captain=self)
            trainer.train()

        logger.debug('CaptainAhab has finished training')
        self.__initialized = True

    async def perform_next_action(self):
        try:
            queued_item = self.action_queue.get(timeout=self.action_wait_timeout)
            queued_item.action.invoke()
            self.action_queue.task_done()
        except Exception as e:
            pass

    async def queue_action(self, action_cls, priority=None):
        self.action_queue.put(PrioritizedAction(priority=priority or action_cls.default_priority, action=action_cls()))

    async def queue_actions(self, action_list, priority=None):
        for action_cls in action_list:
            await self.queue_action(action_cls=action_cls, priority=priority)

    async def cast(self):
        await self.queue_action(CastLine)

    async def hook(self):
        await self.queue_action(HookFish)

    async def reel(self):
        await self.queue_action(ReelIn)

    async def release(self):
        await self.queue_action(ReleaseTension)

    async def wait(self):
        await self.queue_action(Wait)

    async def repair(self):
        await self.queue_action(RepairGear)

    async def bait(self):
        await self.queue_action(EquipBait)

    async def shift(self):
        await self.queue_action(ShiftPosition)

    async def move(self):
        await self.queue_action(Move)

    async def speak(self):
        await self.queue_action(Speak)

    async def look(self):
        await self.queue_action(Look)


__all__ = ['CaptainAhab']
