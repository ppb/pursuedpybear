import sys
import code
import ppb
import threading
import logging
import readline
import pathlib
import textwrap
import atexit
import signal


class InteractiveConsole(code.InteractiveConsole):
    last_prompt = ""

    def raw_input(self, prompt):
        self.last_prompt = prompt
        return super().raw_input(prompt)

    def interject(self, text):
        sys.stdout.write(
            "\r\x1B[2K"  # ANSI for "move to the begining of the line, then erase it"
            + text
            + "\n"
            + self.last_prompt
             # readline.redisplay() doesn't seem to do anything
            + readline.get_line_buffer()
        )
        sys.stdout.flush()

# Reset terminal on exit
# atexit.register(print, "\x1Bc", flush=True)

class ReadlineHandler(logging.Handler):
    def __init__(self, *p, **kw):
        super().__init__(*p, **kw)
        self.output = print

    def emit(self, record):
        # Blatently stolen from logging.StreamHandler.emit()
        try:
            msg = self.format(record)
            self.output(msg)

        except Exception:
            self.handleError(record)


class BaseSprite(ppb.BaseSprite):
    resource_path = pathlib.Path.cwd()


class ReplThread(threading.Thread):
    banner = """
    PPB Interactive Console

    Vector, BaseSprite, BaseScene, ppb and several other things are imported.

    scene is preloaded with the starting scene. Defining things in the REPL show
    up on the scene. Event handlers work.

    current_scene() gets the current scene.
    signal() injects an event.

    Type "help" for more information.
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
            "BaseSprite": BaseSprite,
            "DoNotRender": ppb.flags.DoNotRender,
            "ppb": ppb,
            "events": ppb.events,
            "keycodes": ppb.keycodes,
            "buttons": ppb.buttons,
            "current_scene": self.get_scene,
            "signal": self.signal,
        }

    def signal(self, event):
        self.engine.signal(event)

    def get_scene(self):
        return self.engine.current_scene

    def run(self):
        # Stolen from stdlib code.interact()
        self.console = InteractiveConsole(self.locals)
        if sys.__interactivehook__ is not None:
            sys.__interactivehook__()

        try:
            self.console.interact(banner=textwrap.dedent(self.banner), exitmsg="")
        finally:
            self.signal(ppb.events.Quit())

    def interject(self, text):
        if self.console is None:
            print(text)
        else:
            self.console.interject(text)

repl = None

class ReplScene(ppb.BaseScene):
    def __init__(self, *p, **kw):
        super().__init__(*p, **kw)
        repl.locals['scene'] = self

    last_event_error = None

    def __event__(self, event, signal):
        try:
            super().__event__(event, signal)
        except Exception:
            event_name = type(event).__name__
            if self.last_event_error != event_name:
                logging.exception("Error handling %s event", event_name)
                self.last_event_error = event_name

    def __getattribute__(self, name):
        global repl
        if repl is not None:
            try:
                return repl.locals[name]
            except KeyError:
                pass # Fall through
        return super().__getattribute__(name)


handler = ReadlineHandler()
logging.basicConfig(level=logging.INFO, handlers=[handler])

# Don't let Ctrl-C kill the game engine
# FIXME: Figure out some way to raise KeyboardInterrupt in the repl thread
signal.signal(signal.SIGINT, signal.SIG_IGN)

with ppb.GameEngine(ReplScene) as eng:
    repl = ReplThread(eng)
    handler.output = repl.interject
    repl.start()
    eng.run()
    repl.interject("Engine has quit")
