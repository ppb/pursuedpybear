 How ppb Fits Together
===========================================================

This document is an overall reference of what ppb is, how it's organized, and
how to use the various pieces.

The Conceptual Necessities
-----------------------------------------------------------
.. _arch-the-basics:

Put some introduction here.

It is conceptually useful to consider PursuedPyBear applications as a tree of
nodes. In :code:`ppb` parlance, we refer to nodes as
:py:class:`GameObjects <ppb.gomlib.GameObject>`. A game object can have any
number of children and are allowed to organize their internal children however
the developer likes. Each :py:class:`~ppb.gomlib.GameObject` is capable of
responding to :ref:`events <arch-events>`, which is the primary messaging
utility in :code:`ppb`. Ultimately, though, a :py:class:`~ppb.gomlib.GameObject`
is of little use in a vacuum. As such, :code:`ppb` provides a number of semantic
:py:class:`GameObjects <ppb.gomlib.GameObject>` with focused roles.

The expected root of the :py:class:`~ppb.gomlib.GameObject` tree is the
:py:class:`~ppb.GameEngine`. It is important that you use
:py:class:`~ppb.GameEngine`, either directly or indirectly, for this object
because all other assumptions in :code:`ppb` are built on how
:ref:`the engine interacts with its children <arch-game-engine>`.

The children of the :py:class:`~ppb.GameEngine` come in two flavors:
:py:class:`Scenes <ppb.Scene>` and :py:class:`Systems <ppb.systemslib.System>`.

The :py:class:`Systems <ppb.systemslib.System>` are how :code:`ppb` developers
add new features to the engine. They also allow you to add code that crosses
:py:class:`~ppb.Scene` boundaries, or interacts with external software or
systems. They are Python context managers to allow for setup and teardown of
external resources, and include their own children like any
:py:class:`~ppb.gomlib.GameObject`.

.. todo::

   Need a link to the Systems section. Might need to add language?

:py:class:`Scenes <ppb.Scene>` allow you to break up your applications into
discreet parts. Most of the time, :py:class:`Scenes <ppb.Scene>` need little
more than an initialization function as they're ultimately there to hold
together the pieces that make up a section of a game, but like other
:py:class:`GameObjects <ppb.gomlib.GameObject>` they can respond to events. The
Scene's children are usually :py:class:`Sprites <ppb.Sprite>`.

A basic outline of the core elements of using ppb:
    3. Sprites
    4. Events, EventTypes, Event Handlers
    5. Flags?
    6. Assets?

This section should be light and to the point: It's basically a technical
reference version of getting started and link to more detailed descriptions
further in this document.

Things not included in this list but will be important to document:

3. Time?
4. Camera

Events
-----------------------------------------------------------
.. _arch-events:

1. What is an event
2. Event classes
    1. dataclasses/attr classes
3. Event dispatch
    1. The queue
    2. Conversion from EventName to on_event_name
    3. publication
4. Event handlers
    1. Naming rules
    2. Parameters
    3. accessible data

The Game Engine
-----------------------------------------------------------
.. _arch-game-engine:

1. Context managers
2. The children types (scenes, systems)
3. Event publication?
4. The run function
5. Events the Engine responds to
6. Idle event!

Systems
-----------------------------------------------------------

.. _arch-systems:

1. Behaviors specific to the engine/across scenes
2. Context managers
    1. Why context managers
    2. Examples
3. Children (GameObjects)
4. Events!

Scenes
-----------------------------------------------------------

.. _arch-scenes:

1. Conceptualization: a container that allows separating parts of games
2. Holds GameObjects
    1. Adding and removing game objects
    2. Querying Game Objects
    3. The Camera
3. The Scene lifecycle with examples
4. events

Sprites
-----------------------------------------------------------

.. _arch-sprites:

1. What a Sprite is
2. How to build a sprite
    1. built in
    2. use basesprite to mixin in your own
3. Events

Assets
-----------------------------------------------------------

.. _arch-assets:

1. An asset hooks into the built in asset loader
    1. Asynchrounous!
    2. Allows you to do work in a background thread
    3. Good for things you don't want happening during the game loop proper.
2. Usage
    1. How to instantiate.
    2. Expectations
3. Building new assets

Flags
-----------------------------------------------------------

.. _arch-flags:

What they are, why we want them, constraints for the oddity of implementation.

Renderer
-----------------------------------------------------------

.. _arch-renderer:

Details about the metadata driven renderer.

sprite.image
sprite.position
sprite.facing/rotation
sprite.tint
sprite.opacity
???

Camera
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. _arch-camera:

Details about the camera, when it's instantiated, how it works (notes about
the aspect ratio being more important that the requested width/height.)

Timekeeping
-----------------------------------------------------------

.. _arch-time:

utils.get_time
wall time
game time

Input
-----------------------------------------------------------

.. _arch-input:

Supported inputs
what the flags look like
reasoning for uncommon names (button.Primary, Secondary, Tertiary)
How to interact with them
Warnings
