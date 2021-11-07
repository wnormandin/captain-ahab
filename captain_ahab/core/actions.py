import abc
import logging
import time
import win32api
import win32con
from dataclasses import dataclass, field
from ..utils.constants import InputCode, TriggerColors, ImageRegistry, VERBOSITY, fishing_config
from .randomizer import random_float, random_wait


logger = logging.getLogger(__name__)


class Action(metaclass=abc.ABCMeta):
    """ Abstract base class from which all Actions will be derived """

    default_priority = 3

    def __init__(self, captain):
        self.__args = set()
        self.__kwargs = {}
        self.captain = captain

    def __str__(self):
        return f'action:{self.__class__.__name__}'

    @property
    def args(self) -> list:
        return list(self.__args)

    @property
    def kwargs(self) -> dict:
        return self.__kwargs

    @abc.abstractmethod
    def _prepare(self):
        """ Must be implemented in an Action child, prepare internal arguments for invocation """

    @abc.abstractmethod
    def _perform_action(self, *args, **kwargs):
        """ Must be implemented in an Action child, execute the given action """

    @staticmethod
    def press_key(key):
        if isinstance(key, str):
            key = InputCode[key]

        win32api.keybd_event(key.value, 0, 0, 0)

    @staticmethod
    def release_key(key):
        if isinstance(key, str):
            key = InputCode[key]

        win32api.keybd_event(key.value, 0, win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def point_mouse(position):
        win32api.SetCursorPos(position)

    @staticmethod
    def click_mouse():
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)

    @staticmethod
    def release_mouse():
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    @staticmethod
    def wait(duration):
        time.sleep(duration)

    @staticmethod
    def wait_range(minimum=0.0, maximum=1.0):
        time.sleep(random_float(minimum=minimum, maximum=maximum))

    def invoke(self):
        if VERBOSITY >= 3:
            logger.debug(f'{self} invoked')

        self._prepare()
        return self._perform_action(*self.args, **self.kwargs)

    def click_at(self, position, duration=0.05):
        self.point_mouse(position)
        self.wait(duration/2)
        self.click_mouse()
        self.wait(duration)
        self.release_mouse()

    def keystroke(self, key, duration=0.05):
        self.press_key(key)
        self.wait(duration)
        self.release_key(key)

    def random_keystroke(self, key, burst_min, burst_max):
        duration = random_float(burst_min, burst_max)
        self.keystroke(key, duration=duration)


@dataclass(order=True)
class PrioritizedAction:
    priority: int
    action: Action = field(compare=False)


class KeyStroke(Action, metaclass=abc.ABCMeta):
    config = NotImplemented
    config_delay_key = NotImplemented
    keystroke = None

    def _prepare(self):
        self.kwargs['burst_min'] = int(self.config[f'{self.config_delay_key}_min'])
        self.kwargs['burst_max'] = int(self.config[f'{self.config_delay_key}_max'])

    def _perform_action(self, burst_min, burst_max):
        if self.keystroke:
            logger.debug(f'Pressing {self.keystroke} for ({burst_min}-{burst_max})s')
            self.random_keystroke(key=self.keystroke, burst_min=burst_min, burst_max=burst_max)


class FishingKeyStroke(KeyStroke):
    config = fishing_config
    keystroke = InputCode.e


class CastLine(FishingKeyStroke):
    config_delay_key = 'cast_delay'


class HookFish(FishingKeyStroke):
    config_delay_key = 'hook_delay'


class ReelIn(FishingKeyStroke):
    config_delay_key = 'reel_delay'


class ReleaseTension(Action):
    default_priority = 1

    def _prepare(self):
        pass

    def _perform_action(self):
        logger.debug(f'Releasing {InputCode.e}')
        self.release_key(InputCode.e)
        self.captain.purge_queue()


class Wait(Action):
    default_priority = 4

    def _prepare(self):
        self.kwargs['delay'] = random_wait()

    def _perform_action(self, delay):
        logger.debug(f'Waiting {delay}s')
        self.wait(delay)


class RepairGear(Action):
    def _prepare(self):
        pass

    def _perform_action(self):
        pass


class EquipBait(Action):
    def _prepare(self):
        pass

    def _perform_action(self):
        pass


class ShiftPosition(Action):
    def _prepare(self):
        pass

    def _perform_action(self):
        pass


class Speak(Action):
    def _prepare(self):
        pass

    def _perform_action(self):
        pass


class Move(Action):
    def _prepare(self):
        pass

    def _perform_action(self):
        pass


class Look(Action):
    def _prepare(self):
        pass

    def _perform_action(self):
        found = self.captain.eyes.look()

        if found is None:
            logger.debug(f'CaptainAhab did not notice anything')
        else:
            logger.info(f'CaptainAhab saw {found}')
            if isinstance(found, set):
                for match in found:
                    if match is TriggerColors.safe_tension:
                        self.captain.reel()
                    elif match is TriggerColors.medium_tension:
                        self.captain.release()
                    elif match is TriggerColors.unsafe_tension:
                        self.captain.release()
            elif isinstance(found, ImageRegistry):
                if found is ImageRegistry.line_cast:
                    self.captain.wait()
                elif found is ImageRegistry.fish_hooked:
                    self.captain.hook()


__all__ = ['CastLine', 'HookFish', 'ReelIn', 'ReleaseTension', 'Wait', 'RepairGear', 'EquipBait', 'ShiftPosition',
           'PrioritizedAction', 'Speak', 'Move', 'Look']
