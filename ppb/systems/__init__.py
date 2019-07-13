import time
import logging

import ppb.eventlib as eventlib
import ppb.events as events

logger = logging.getLogger(__name__)


default_resolution = 800, 600


class System(eventlib.EventMixin):

    def __init__(self, **_):
        pass

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


from ppb.systems.inputs import EventPoller
from .renderer import Renderer, Image
from .clocks import Updater
