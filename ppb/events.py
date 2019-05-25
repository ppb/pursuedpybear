from dataclasses import dataclass
import logging
import re
from typing import Any
from typing import Collection
from typing import Dict
from typing import Set
from typing import Type
from typing import Union


__all__ = (
    'StartScene',
    'EventMixin',
    'PreRender',
    'Quit',
    'Render',
    'ReplaceScene',
    'SceneContinued',
    'ScenePaused',
    'SceneStarted',
    'SceneStopped',
    'StopScene',
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


# Remember to define scene at the end so the pargs version of __init__() still works

from ppb.scenes import BaseScene
from ppb.buttons import MouseButton
from ppb.keycodes import KeyCode
from ppb_vector import Vector


@dataclass
class ButtonPressed:
    """
    Fired when a button is pressed
    """
    button: MouseButton
    position: Vector  # Scene position
    # TODO: Add frame position
    scene: BaseScene = None


@dataclass
class ButtonReleased:
    """
    Fired when a button is released
    """
    button: MouseButton
    position: Vector  # Scene position
    # TODO: Add frame position
    scene: BaseScene = None


@dataclass
class StartScene:
    """
    Fired to start a new scene.

    new_scene can be an instance or a class. If a class, must include kwargs.
    If new_scene is an instance kwargs should be empty or None.

    Before the previous scene pauses, a ScenePaused event will be fired.
    Any events signaled in response will be delivered to the new scene.

    After the ScenePaused event and any follow up events have been delivered, a
    SceneStarted event will be sent.

    Examples:
        * `signal(new_scene=StartScene(MyScene(player=player))`
        * `signal(new_scene=StartScene, kwargs={"player": player}`
    """
    new_scene: Union[BaseScene, Type[BaseScene]]
    kwargs: Dict[str, Any] = None
    scene: BaseScene = None


@dataclass
class KeyPressed:
    key: KeyCode
    mods: Set[KeyCode]
    scene: BaseScene = None


@dataclass
class KeyReleased:
    key: KeyCode
    mods: Set[KeyCode]
    scene: BaseScene = None


@dataclass
class MouseMotion:
    """An event to represent mouse motion."""
    position: Vector
    screen_position: Vector
    delta: Vector
    buttons: Collection[MouseButton]
    scene: BaseScene = None


@dataclass
class PreRender:
    """
    Fired before rendering.
    """
    scene: BaseScene = None


@dataclass
class Quit:
    """
    Fired on an OS Quit event.

    You may also fire this event to stop the engine.
    """
    scene: BaseScene = None


@dataclass
class Render:
    """
    Fired at render.
    """
    scene: BaseScene = None


@dataclass
class ReplaceScene:
    """
    Fired to replace the current scene with a new one.

    new_scene can be an instance or a class. If a class, must include kwargs.
    If new_scene is an instance kwargs should be empty or None.

    Before the previous scene stops, a SceneStopped event will be fired.
    Any events signaled in response will be delivered to the new scene.

    After the SceneStopped event and any follow up events have been delivered,
    a SceneStarted event will be sent.

    Examples:
        * `signal(new_scene=ReplaceScene(MyScene(player=player))`
        * `signal(new_scene=ReplaceScene, kwargs={"player": player}`
    """
    new_scene: Union[BaseScene, Type[BaseScene]]
    kwargs: Dict[str, Any] = None
    scene: BaseScene = None


@dataclass
class SceneContinued:
    """
    Fired when a paused scene continues.

    This is delivered to a scene as it resumes operation after being paused via
    a ScenePaused event.

    From the middle of the event lifetime that begins with SceneStarted.
    """
    scene: BaseScene = None


@dataclass
class SceneStarted:
    """
    Fired when a scene starts.

    This is delivered to a Scene shortly after it starts. The beginning of the
    scene lifetime, ended with SceneStopped, paused with ScenePaused, and
    resumed from a pause with SceneContinued.
    """
    scene: BaseScene = None


@dataclass
class SceneStopped:
    """
    Fired when a scene stops.

    This is delivered to a scene and it's objects when a StopScene or
    ReplaceScene event is sent to the engine.

    The end of the scene lifetime, started with SceneStarted.
    """
    scene: BaseScene = None


@dataclass
class ScenePaused:
    """
    Fired when a scene pauses.

    This is delivered to a scene about to be paused when a StartScene event is
    sent to the engine. When this scene resumes it will receive a
    SceneContinued event.

    A middle event in the scene lifetime, started with SceneStarted.
    """
    scene: BaseScene = None


@dataclass
class StopScene:
    """
    Fired to stop a scene.

    Before the scene stops, a SceneStopped event will be fired. Any events
    signaled in response will be delivered to the previous scene if it exists.

    If there is a paused scene on the stack, a SceneContinued event will be
    fired after the responses to the SceneStopped event.
    """
    scene: BaseScene = None


@dataclass
class Idle:
    """
    An engine plumbing event to pump timing information to subsystems.
    """
    time_delta: float
    scene: BaseScene = None


@dataclass
class Update:
    """
    Fired on game tick
    """
    time_delta: float
    scene: BaseScene = None
