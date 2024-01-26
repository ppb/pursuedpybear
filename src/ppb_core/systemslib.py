"""
Systemslib is the core class for new subsystems. Systems add new features to 
the core ppb engine.
"""

import ppb_core.gomlib


class System(ppb_core.gomlib.GameObject):

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
