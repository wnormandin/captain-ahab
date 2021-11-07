import logging
from numpy import array
from PIL import ImageGrab
from cv2 import cv2 as cv
from typing import Union, Set
from ..utils.constants import ImageRegistry, TriggerColors, VERBOSITY, SAMPLE_PATH


logger = logging.getLogger(__name__)


class Eyes:
    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._w = width
        self._h = height
        self._current_view = None
        self._current_view_bw = None
        self._known_images = {}
        self._known_triggers = {}
        self._variance = 6

    @property
    def visual_field(self):
        return self._x, self._y, self._w, self._h

    def sample(self, target_field=None):
        # Sample the field of vision
        image = ImageGrab.grab(bbox=target_field or self.visual_field)

        # Save a copy of the image for debugging if the configuration has a path set
        if SAMPLE_PATH:
            image.save(SAMPLE_PATH)

        self._current_view = array(image)
        # Convert color for match
        self._current_view_bw = cv.cvtColor(self._current_view, cv.COLOR_BGR2GRAY)

    def look(self, target_field=None) -> Union[ImageRegistry, Set[TriggerColors], None]:
        self.sample(target_field=target_field)

        if VERBOSITY >= 2:
            logger.debug('Checking for known images in the sample')

        for image_key, image in self._known_images.items():
            found = cv.matchTemplate(self._current_view_bw, image, cv.TM_CCOEFF_NORMED)
            if (found >= 0.75).any():
                return ImageRegistry[image_key]

        if VERBOSITY >= 2:
            logger.debug('Checking for pixels matching known triggers in the sample')

        matched_pixels = set()
        for trigger_key, trigger in self._known_triggers.items():
            if self.match(self._current_view, trigger, trigger_key):
                matched_pixels.add(TriggerColors[trigger_key])

        return matched_pixels or None

    def match(self, image, color, color_name) -> bool:
        lower, upper = (
            array([color[0] - self._variance, color[1] - self._variance, color[2] - self._variance]),
            array([color[0] + self._variance, color[1] + self._variance, color[2] + self._variance])
        )
        match = cv.inRange(image, lower, upper).any()
        matched = (match >= 0.74).any()

        if VERBOSITY >= 3:
            logger.debug(f'Pixel match result for {color_name}: {matched}')

        return matched

    def learn_image(self, image_key, image_path):
        image = cv.imread(str(image_path))

        if image is None or not image.any():
            raise ValueError(f'Invalid image path (file does not exist): {image_path}')

        self._known_images[image_key] = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

        if VERBOSITY >= 3:
            logger.info(f'Learned image: {image_path}')

    def learn_trigger(self, trigger_key, trigger_rgb):
        self._known_triggers[trigger_key] = trigger_rgb

        if VERBOSITY >= 3:
            logger.info(f'Learned pixel color trigger: {trigger_key}')
