import abc
import time
import win32api, win32con
from dataclasses import dataclass, field
from ..utils.constants import InputCode


class Action(metaclass=abc.ABCMeta):
    """ Abstract base class from which all Actions will be derived """

    default_priority = 3

    def __init__(self):
        self.__args = set()
        self.__kwargs = {}

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

    def invoke(self):
        self._prepare()
        self._perform_action(*self.args, **self.kwargs)

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


@dataclass(order=True)
class PrioritizedAction:
    priority: int
    action: Action = field(compare=False)


class CastLine(Action):
    def _prepare(self):
        pass

    def _perform_action(self):
        pass


class HookFish(Action):
    def _prepare(self):
        pass

    def _perform_action(self):
        pass


class ReelIn(Action):
    def _prepare(self):
        pass

    def _perform_action(self):
        pass


class ReleaseTension(Action):
    default_priority = 1

    def _prepare(self):
        pass

    def _perform_action(self):
        pass


class Wait(Action):
    default_priority = 4

    def _prepare(self):
        pass

    def _perform_action(self):
        pass


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
        pass


__all__ = ['CastLine', 'HookFish', 'ReelIn', 'ReleaseTension', 'Wait', 'RepairGear', 'EquipBait', 'ShiftPosition',
           'PrioritizedAction', 'Speak', 'Move', 'Look']
