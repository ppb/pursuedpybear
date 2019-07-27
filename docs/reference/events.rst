======
Events
======

All game objects (the engine, scenes, sprites, systems, etc) receive events.
Handlers are methods that start with ``on_``, eg ``on_update``,
``on_button_pressed``.

The signature of these handlers are the same: ``(event, signal)``:

* ``event``: An object containing all the properties of the event, such as the
  button pressed, the position of the mouse, the current scene
* ``signal``: A callable that accepts an object, which will be raised as an
  event: ``signal(StartScene(new_scene=OtherScene()))``


Engine Events
=============

These are core events from hardware and the engine itself.

.. autoclass:: ppb.events.Update
   :members:

.. autoclass:: ppb.events.PreRender
   :members:

.. autoclass:: ppb.events.Idle
   :members:

.. autoclass:: ppb.events.Render
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

API Events
==========

These "events" are more for code to call into the engine.

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

These are events triggered about the lifetime of a scene: it starting, stopping,
etc.

The ``scene`` property on these events always refers to the scene these are
about--``ScenePaused.scene`` is the scene that is being paused.

.. autoclass:: ppb.events.SceneStarted
   :members:

.. autoclass:: ppb.events.SceneStopped
   :members:

.. autoclass:: ppb.events.ScenePaused
   :members:

.. autoclass:: ppb.events.SceneContinued
   :members:
