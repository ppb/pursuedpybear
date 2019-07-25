"""
A big pile of the events defined in PPB.
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


@dataclass
class PlaySound:
    """
    Fire to start a sound playing.
    """
    sound: 'ppb.assets.Asset'

@dataclass
class AssetLoaded:
    """
    Fired whenever an asset finished loading.
    """
    asset: 'ppb.assets.Asset'
    total_loaded: int
    total_queued: int
