import sys
import code
import ppb
import threading
import logging


class ReplThread(threading.Thread):
    banner = """
    """
    def __init__(self, engine):
        super().__init__(name='repl')
        self.engine = engine
        self.locals = self.build_locals()

    def build_locals(self):
        return {
            "__name__": "__console__",
            "__doc__": None,
            "Vector": ppb.Vector,
            "BaseScene": ppb.BaseScene,
            "BaseSprite": ppb.BaseSprite, 
            "current_scene": self.get_scene,
            "signal": self.signal,
        }

    def signal(self, event):
        self.engine.signal(event)

    def get_scene(self):
        return self.engine.current_scene

    def run(self):
        # Stolen from stdlib code.interact()
        console = code.InteractiveConsole(self.locals)
        if sys.__interactivehook__ is not None:
            sys.__interactivehook__()

        console.interact(banner=self.banner, exitmsg="")
        self.signal(ppb.events.Quit())


logging.basicConfig(level=logging.INFO)

with ppb.GameEngine(ppb.BaseScene) as eng:
    repl = ReplThread(eng)
    repl.start()
    eng.run()
    print("Engine has quit")
