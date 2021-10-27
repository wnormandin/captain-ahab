import os
import pathlib
import enum
import configparser

config = configparser.ConfigParser()
config.read(os.environ.get('CAPTAIN_AHAB_CONFIG', 'pequod.ini'))


# Add to this enum to learn more keys
class InputCode(enum.Enum):
    tab = 0x09
    a = 0x41
    b = 0x42
    d = 0x44
    e = 0x45
    r = 0x52
    f3 = 0x72


# Add to this enum to learn new images
class ImageRegistry(enum.Enum):
    # Fishing images
    line_cast = pathlib.Path('../images/line_cast.jpg')
    fish_hooked = pathlib.Path('../images/fish_hooked.jpg')


# Add to this enum to learn more triggers
class TriggerColors(enum.Enum):
    # Fishing colors
    safe_tension = (4, 227, 162)
    medium_tension = (230, 110, 22)
    unsafe_tension = (109, 18, 21)
