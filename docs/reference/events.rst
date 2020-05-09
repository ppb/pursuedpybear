.. py:currentmodule:: ppb.events

======
Events
======

.. automodule:: ppb.events

Basic Events
==================

These events are the basic events you'll want to build your games. You can make
a variety of games using just them.

.. autoclass:: ppb.events.Update
   :members:

.. autoclass:: ppb.events.PreRender
   :members:

.. autoclass:: ppb.events.ButtonPressed
   :members:

.. autoclass:: ppb.events.ButtonReleased
   :members:

.. autoclass:: ppb.events.KeyPressed
   :members:

.. autoclass:: ppb.events.KeyReleased
   :members:

.. autoclass:: ppb.events.MouseMotion
   :members:

Command Events
===================

These events are used in your code to achieve certain effects.

.. autoclass:: ppb.events.Quit
   :members:

.. autoclass:: ppb.events.StartScene
   :members:

.. autoclass:: ppb.events.ReplaceScene
   :members:

.. autoclass:: ppb.events.StopScene
   :members:

.. autoclass:: ppb.events.PlaySound
   :members:

Scene Transition Events
=======================

These are events triggered during the lifetime of a scene: it starting, stopping,
etc.

The ``scene`` property on these events always refers to the scene these are
about---``ScenePaused.scene`` is the scene that is being paused.

.. autoclass:: ppb.events.SceneStarted
   :members:

.. autoclass:: ppb.events.ScenePaused
   :members:

.. autoclass:: ppb.events.SceneContinued
   :members:

.. autoclass:: ppb.events.SceneStopped
   :members:

Engine Events
=============

These are additional events from the engine mostly for advanced purposes.

.. autoclass:: ppb.events.Idle
   :members:

.. autoclass:: ppb.events.Render
   :members:

.. autoclass:: ppb.events.AssetLoaded
   :members:
