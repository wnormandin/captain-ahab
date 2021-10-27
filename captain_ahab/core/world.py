import abc


class WorldObject(metaclass=abc.ABCMeta):
    pass


class SpriteObject(WorldObject):
    pass


class ColorTrigger(WorldObject):
    pass
