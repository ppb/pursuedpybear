from dataclasses import dataclass
import logging
import re
from typing import Collection
from typing import Set
from typing import Optional

__all__ = (
    'EventMixin',
    'PreRender',
    'Quit',
    'Render',
    'Update',
)

boundaries_finder = re.compile('(.)([A-Z][a-z]+)')
boundaries_finder_2 = re.compile('([a-z0-9])([A-Z])')

def camel_to_snake(txt):
    s1 = boundaries_finder.sub(r'\1_\2', txt)
    return boundaries_finder_2.sub(r'\1_\2', s1).lower()


class BadEventHandlerException(TypeError):

    def __init__(self, instance, method, event):
        object_type = type(instance)
        event_type = type(event)
        o_name = object_type.__name__
        e_name = event_type.__name__
        article = ['a', 'an'][int(e_name.lower()[0] in "aeiou")]

        message = f"""
{o_name}.{method}() signature incorrect, it should accept {article} {e_name} object and a signal function.

{e_name} is a dataclass that represents an event. Its attributes 
tell you about the event.

The signal function is a function you can call that accepts an event instance
as its only parameter. Call it to add an event to the queue. You don't have to
use it, but it is a mandatory argument provided by ppb.

It should look like this:

def {method}({e_name.lower()}_event: {e_name}, signal_function):
    (Your code goes here.)
"""
        super().__init__(message)


class EventMixin:
    def __event__(self, bag, fire_event):
        elog = logging.getLogger('game.events')

        name = camel_to_snake(type(bag).__name__)
        meth_name = 'on_' + name
        meth = getattr(self, meth_name, None)
        if callable(meth):
            try:
                elog.debug(f"Calling handler {meth} for {name}")
                meth(bag, fire_event)
            except TypeError as ex:
                from inspect import signature
                sig = signature(meth)
                try:
                    sig.bind(bag, fire_event)
                except TypeError:
                    raise BadEventHandlerException(self, meth_name, bag) from ex
                else:
                    raise

# Import these late so we don't have circular import problems.
from ppb.buttons import MouseButton
from ppb.keycodes import KeyCode
from ppb.vector import Vector
from ppb.scenes import BaseScene

# Remember to define scene at the end so the pargs version of __init__() still works
@dataclass
class ButtonPressed:
    """
    Fired when a button is pressed
    """
    button: MouseButton
    position: Vector  # Scene position
    # TODO: Add frame position
    scene: Optional[BaseScene] = None


@dataclass
class ButtonReleased:
    """
    Fired when a button is released
    """
    button: MouseButton
    position: Vector  # Scene position
    # TODO: Add frame position
    scene: Optional[BaseScene] = None


@dataclass
class KeyPressed:
    key: KeyCode
    mods: Set[KeyCode]
    scene: Optional[BaseScene] = None


@dataclass
class KeyReleased:
    key: KeyCode
    mods: Set[KeyCode]
    scene: Optional[BaseScene] = None

@dataclass
class MouseMotion:
    """An event to represent mouse motion."""
    position: Vector
    screen_position: Vector
    delta: Vector
    buttons: Collection[MouseButton]
    scene: Optional[BaseScene] = None


@dataclass
class PreRender:
    """
    Fired before rendering.
    """
    scene: Optional[BaseScene] = None


@dataclass
class Quit:
    """
    Fired on an OS Quit event.
    """
    scene: Optional[BaseScene] = None


@dataclass
class Render:
    """
    Fired at render.
    """
    scene: Optional[BaseScene] = None


@dataclass
class Update:
    """
    Fired on game tick
    """
    time_delta: float
    scene: Optional[BaseScene] = None
