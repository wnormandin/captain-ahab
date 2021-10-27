import abc
from ..utils.constants import config, ImageRegistry, TriggerColors
from .angler import Angler
from .sight import Eyes
from .mobility import Legs
from .voice import Voice
from .world import SpriteObject, ColorTrigger


class CaptainTrainer(metaclass=abc.ABCMeta):
    def __init__(self, captain):
        self.captain = captain

    @abc.abstractmethod
    def train(self):
        return NotImplemented


class SightTrainer(CaptainTrainer):
    """ Trainer which provides an initialized set of Eyes with known sprites/triggers loaded """

    def train(self):
        self.captain.eyes = Eyes(*self.captain.visual_field)

        for image in ImageRegistry:
            self.captain.eyes.learn_image(image.name, image.value)

        for trigger in TriggerColors:
            self.captain.eyes.learn_trigger(trigger.name, trigger.value)


class MovementTrainer(CaptainTrainer):
    """ Trainer which provides an initialized set of Legs with known movement patterns """

    def train(self):
        self.captain.legs = Legs()


class VoiceTrainer(CaptainTrainer):
    """ Trainer which provides an initialized Voice with known chatting patterns """

    def train(self):
        self.captain.voice = Voice()


class FishingTrainer(CaptainTrainer):
    """ Trainer which provides an instance of the Angler ability """

    def train(self):
        self.captain.angler = Angler()


__all__ = ['SightTrainer', 'MovementTrainer', 'VoiceTrainer']
