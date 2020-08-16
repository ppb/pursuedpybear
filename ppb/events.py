"""
Events are the primary way objects in ppb communicate. This module contains the
events defined by various systems in ppb.

To respond to an event your event handler should be snake_cased
``on_event_name`` and accept an event instance and a signal function as
parameters. Example: ::

   class MySprite(Sprite):
       def on_update(self, event: Update, signal):
           . . .

The :meth:`~ppb.GameEngine.signal` function accepts one parameter: an
instance of an event class. You are not limited to predefined event types, but
can provide arbitrary instances.

Events as defined here are :func:`dataclasses.dataclass`, but ppb does
not expect dataclasses; they are just a simple way to quickly define new events.
The name of the handler will always be based on the name of the class, with the
TitleCase name of the class converted to on_event_name function. The instance
passed to :meth:`~ppb.GameEngine.signal` will be passed to all the event
handlers as the event parameter.
"""
from dataclasses import dataclass
from typing import Any
from typing import Collection
from typing import Dict
from typing import Set
from typing import Type
from typing import Union


__all__ = (
    'StartScene',
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
    'AssetLoaded',
)

# Remember to define scene at the end so the pargs version of __init__() still works

from ppb.scenes import BaseScene
from ppb.buttons import MouseButton
from ppb.keycodes import KeyCode
from ppb_vector import Vector
import ppb


@dataclass
class ButtonPressed:
    """
    A mouse button was pressed.

    The button is a :class:`~ppb.buttons.MouseButton` instance.

    This represents the button in the active state. For acting when a button
    is released see :class:`ButtonReleased`.
    """
    button: MouseButton
    position: Vector  # Scene position
    scene: BaseScene = None


@dataclass
class ButtonReleased:
    """
    A mouse button was released.

    The button is a :class:`~ppb.buttons.MouseButton` instance.

    This represents the button in the inactive state. For acting when a button
    is clicked see :class:`ButtonPressed`.
    """
    button: MouseButton  #: A mouse button: Primary, Secondary, or Tertiary
    position: Vector  #: The game-world position of the event.
    scene: BaseScene = None  #: The currently running scene.


@dataclass
class StartScene:
    """
    An object requested a new scene to be started.

    ``new_scene`` can be an instance or a class. If a class, must include kwargs.
    If new_scene is an instance kwargs should be empty or None.

    Before the previous scene pauses, a ScenePaused event will be fired.
    Any events signaled in response will be delivered to the new scene.

    After the ScenePaused event and any follow up events have been delivered, a
    SceneStarted event will be sent.

    Examples:
        * `signal(new_scene=StartScene(MyScene(player=player))`
        * `signal(new_scene=StartScene, kwargs={"player": player}`

    .. warning::
       In general, you should not respond to :class:`StartScene`, if you want to respond to
       a new scene, see :class:`SceneStarted`.
    """
    new_scene: Union[BaseScene, Type[BaseScene]]  #: A :class:`~ppb.scenes.BaseScene` class or instance
    kwargs: Dict[str, Any] = None  #: Keyword arguments to be passed to a scene type.
    scene: BaseScene = None  #: The currently running scene.


@dataclass
class KeyPressed:
    """
    A keyboard key was pressed.

    The buttons are defined in :mod:`ppb.keycodes`.

    This represents the key entering an active state, to respond to when a key
    is released see :class:`KeyReleased`.
    """
    key: KeyCode  #: A :class:`~ppb.keycodes.KeyCode` flag.
    mods: Set[KeyCode]  #: A set of :class:`KeyCodes <ppb.keycodes.KeyCode>`
    scene: BaseScene = None  #: The currently running scene


@dataclass
class KeyReleased:
    """
    A keyboard key was released.

    The buttons are defined in :mod:`ppb.keycodes`.

    This represents the key entering an inactive state, to respond to when a key
    is pressed see :class:`KeyPressed`.
    """
    key: KeyCode  #: A :class:`~ppb.keycodes.KeyCode` flag.
    mods: Set[KeyCode]  #: A set of :class:`KeyCodes <ppb.keycodes.KeyCode>`
    scene: BaseScene = None  #: The currently running scene


@dataclass
class MouseMotion:
    """
    The mouse moved.

    If something should be tracking the mouse, this is the event to listen to.
    """
    position: Vector  #: The game-world location of the mouse cursor.
    screen_position: Vector  #: The screen space location of the mouse cursor.
    delta: Vector  #: The change in position since the last :class:`MouseMotion` event.
    buttons: Collection[MouseButton]  #: The state of the mouse buttons.
    scene: BaseScene = None  #: The currently running scene.


@dataclass
class PreRender:
    """
    The :class:`~ppb.systems.Renderer` is preparing to render.

    :class:`PreRender` is called before every frame is rendered. Things that are
    strictly for display purposes (like the text of a score board or the
    position of the camera) should happen ``on_pre_render``.
    """
    time_delta: float  #: Seconds since last PreRender.
    scene: BaseScene = None  #: The currently running scene.


@dataclass
class Quit:
    """
    A request to quit the program.

    Fired in response to a close request from the OS, but can be signaled from
    inside one of your handlers to end the program.

    For example: ::

       def on_update(self, event, signal):
           signal(Quit())

    This will stop the engine.

    Respond with ``on_quit`` to perform any shut down tasks (like saving data.)
    """
    scene: BaseScene = None  #: The currently running scene.


@dataclass
class Render:
    """
    The :class:`~ppb.systems.Renderer` is rendering.

    .. warning::
       In general, responses to :class:`Render` will not be reflected until the next
       render pass. If you want changes to effect this frame, see
       :class:`PreRender`
    """
    scene: BaseScene = None  #: The currently running scene.


@dataclass
class ReplaceScene:
    """
    An object requested a new scene to replace it.

    ``new_scene`` can be an instance or a class. If a class, must include kwargs.
    If new_scene is an instance kwargs should be empty or None.

    Before the previous scene stops, a SceneStopped event will be fired.
    Any events signaled in response will be delivered to the new scene.

    After the SceneStopped event and any follow up events have been delivered,
    a SceneStarted event will be sent.

    Examples:
        * `signal(ReplaceScene(MyScene(player=player))`
        * `signal(ReplaceScene(new_scene=ReplacementScene, kwargs={"player": player}))`

    .. warning::
       In general, you should not respond to :class:`ReplaceScene`, if you want to
       respond to a new scene, see :class:`SceneStarted`.
    """
    new_scene: Union[BaseScene, Type[BaseScene]]  #: A :class:`~ppb.scenes.BaseScene` class or instance
    kwargs: Dict[str, Any] = None  #: Keyword arguments to be passed to a scene type.
    scene: BaseScene = None  #: The currently running scene.


@dataclass
class SceneContinued:
    """
    A scene that had been paused has continued.

    This is delivered to a scene as it resumes operation after being paused via
    a :class:`ScenePaused` event.

    From the middle of the event lifetime that begins with
    :class:`SceneStarted`.
    """
    scene: BaseScene = None  #: The scene that is resuming.


@dataclass
class SceneStarted:
    """
    A new scene has started running.

    This is delivered to a Scene shortly after it starts.

    Responding to SceneStarted is a good choice for :mod:`ppb.systems` that
    change behavior based on the running scene, or if you have start up work
    that requires the initial state to be set before it happens.

    The scene lifetime events happen in the following order:

    1. Always: :class:`SceneStarted`
    2. Optionally, Repeatable: :class:`ScenePaused`
    3. Optionally, Repeatable: :class:`SceneContinued`
    4. Optionally: :class:`SceneStopped`
    """
    scene: BaseScene = None  #: The scene that is starting.


@dataclass
class SceneStopped:
    """
    A scene is being stopped and will no longer be available.

    This is delivered to a scene and it's objects when a :class:`StopScene` or
    :class:`ReplaceScene` event is sent to the engine.

    This is technically an optional event, as not all scenes in the stack will
    receive a :class:`SceneStopped` event if a :class:`Quit` event was sent.

    This is the end of the scene lifetime, see :class:`SceneStarted`.
    """
    scene: BaseScene = None  #: The scene that is stopping.


@dataclass
class ScenePaused:
    """
    A scene that is running is being paused to allow a new scene to run.

    This is delivered to a scene about to be paused when a :class:`StartScene`
    event is sent to the engine. When this scene resumes it will receive a
    :class:`SceneContinued` event.

    A middle event in the scene lifetime, started with :class:`SceneStarted`.
    """
    scene: BaseScene = None  #: The scene that has paused.


@dataclass
class StopScene:
    """
    An object has requested the current scene be stopped.

    Before the scene stops, a :class:`SceneStopped` event will be fired. Any
    events signaled in response will be delivered to the previous scene if it
    exists.

    If there is a paused scene on the stack, a :class:`SceneContinued` event
    will be fired after the responses to the :class:`SceneStopped` event.

    .. warning::
       In general, you should not respond to :class:`StopScene`, if you want to respond
       to a scene ending, see :class:`SceneStopped`.
    """
    scene: BaseScene = None  #: The scene that is stopping.


@dataclass
class Idle:
    """
    A complete loop of the :class:`~ppb.engine.GameEngine` main loop has
    finished.

    This is an engine plumbing event to pump timing information to subsystems.
    """
    time_delta: float  #: Seconds since last Idle.
    scene: BaseScene = None  #: The currently running scene.


@dataclass
class Update:
    """
    A simulation tick.

    Respond via ``on_update`` to advance the simulation of your game objects.
    Movement and other things that happen "over time" are best implemented in
    your on_update methods.
    """
    time_delta: float  #: Seconds since last Update
    scene: BaseScene = None  #: The currently running scene.


@dataclass
class PlaySound:
    """
    An object requested a sound be played.

    Signal in an event handler to have a sound played.

    Example: ::

       signal(PlaySound(my_sound))
    """
    sound: 'ppb.assetlib.Asset'  #: A :class:`~ppb.systems.sound.Sound` asset.


@dataclass
class AssetLoaded:
    """
    An asset has finished loading.
    """
    asset: 'ppb.assetlib.Asset'  #: A :class:`~ppb.assetlib.Asset`
    total_loaded: int  #: The total count of loaded assets.
    total_queued: int  #: The number of requested assets still waiting.
