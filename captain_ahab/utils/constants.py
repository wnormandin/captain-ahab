import logging
import os
import pathlib
import enum
import configparser
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
config = configparser.ConfigParser()
config.read(os.environ.get('CAPTAIN_AHAB_CONFIG', 'pequod.ini'))
fishing_config = config['fishing']

TEST = bool(config['captain']['test'])
VERBOSITY = int(config['captain']['verbosity'])
SAMPLE_X = int(config['sample_dimensions']['x'])
SAMPLE_Y = int(config['sample_dimensions']['y'])
SAMPLE_WIDTH = int(config['sample_dimensions']['w'])
SAMPLE_HEIGHT = int(config['sample_dimensions']['h'])
SAMPLE_W = SAMPLE_X + SAMPLE_WIDTH
SAMPLE_H = SAMPLE_Y + SAMPLE_HEIGHT
LOG_LEVEL = getattr(logging, config['logging']['log_level'])
CONSOLE_LOGGING = bool(config['logging']['console_logging'])

if config['captain']['sample_image_path']:
    SAMPLE_PATH = pathlib.Path(config['captain']['sample_image_path'])
else:
    SAMPLE_PATH = None

if config['logging']['log_file']:
    LOG_PATH = pathlib.Path(config['logging']['log_file'])
else:
    LOG_PATH = None


# Log setup
def get_handler(handler_cls, log_format='%(message)s', **kwargs):
    formatter = logging.Formatter(fmt=log_format)
    handler = handler_cls(**kwargs)
    handler.setFormatter(formatter)
    return handler


handlers = []
if CONSOLE_LOGGING:
    handlers.append(get_handler(handler_cls=logging.StreamHandler))

if LOG_PATH:
    handlers.append(get_handler(
        handler_cls=logging.FileHandler,
        log_format='%(asctime)s:%(levelname)s:%(name)s(%(process)s): %(message)s',
        filename=LOG_PATH,
        mode='w'
    ))

if handlers:
    logging.basicConfig(level=LOG_LEVEL, force=True, handlers=handlers)

logger = logging.getLogger(__name__)
logger.info(f'Using log path: {LOG_PATH}')


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
    line_cast = pathlib.Path(os.path.abspath('./captain_ahab/images/line_cast.jpg'))
    fish_hooked = pathlib.Path(os.path.abspath('./captain_ahab/images/fish_hooked.jpg'))


# Add to this enum to learn more triggers
class TriggerColors(enum.Enum):
    # Fishing colors
    safe_tension = (4, 227, 162)
    medium_tension = (230, 110, 22)
    unsafe_tension = (109, 18, 21)
    test_color = (108, 135, 197)
