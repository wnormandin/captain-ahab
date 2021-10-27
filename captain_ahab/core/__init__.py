import logging
from queue import PriorityQueue
from .actions import *
from .trainers import SightTrainer, MovementTrainer, VoiceTrainer
from .sight import Eyes
from .mobility import Legs
from .voice import Voice


logger = logging.getLogger(__name__)


class CaptainAhab:
    """
    CaptainAhab is an automaton designed to streamline fishing activities in New World

    The author is not responsible for suspensions or bans as the result of the use of this software or any of its
    components.
    """

    def __init__(self, visual_x, visual_y, visual_width, visual_height):
        self.action_queue = PriorityQueue()
        self.action_wait_timeout = 0.5
        self.visual_field = (visual_x, visual_y, visual_width, visual_height)
        self._eyes = None
        self._legs = None
        self._voice = None
        logger.debug('CaptainAhab lives')

    @property
    def eyes(self):
        return self._eyes

    @eyes.setter
    def eyes(self, new_eyes: Eyes):
        assert isinstance(new_eyes, Eyes)
        self._eyes = new_eyes
        logger.debug('CaptainAhab can see (new Eyes received)')

    @property
    def legs(self):
        return self._legs

    @legs.setter
    def legs(self, new_legs):
        assert isinstance(new_legs, Legs)
        self._legs = new_legs
        logger.debug('CaptainAhab grew legs (new Legs received)')

    @property
    def voice(self):
        return self._voice

    @voice.setter
    def voice(self, new_voice):
        assert isinstance(new_voice, Voice)
        self._voice = new_voice
        logger.debug('CaptainAhab learned to speak (new Voice received)')

    async def train(self):
        """ Training will initialize _eyes/_legs/_voice, etc """

        logger.debug('CaptainAhab is going in for training')
        for trainer_cls in (SightTrainer, MovementTrainer, VoiceTrainer):
            trainer = trainer_cls(captain=self)
            trainer.train()

        logger.debug('CaptainAhab has finished training')

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
