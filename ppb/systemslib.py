"""
Systemslib is the core class for new subsystems. Systems add new features to 
the core ppb engine.
"""

import ppb.gomlib


class System(ppb.gomlib.GameObject):

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
