Clocks
======

PPB has several ways to mark time: fixed-rate updates, frames, and idle time.
These are all exposed via the event system.


Updates
~~~~~~~

The :py:class:`ppb.events.Update` event is fired at a regular, fixed rate
(defaulting to 60 times a second). This is well-suited for simulation updates,
such as motion, running NPC AIs, physics, etc.


Frames
~~~~~~
The :py:class:`ppb.events.PreRender` and :py:class:`ppb.events.Render` are fired
every frame. This is best used for particle systems, animations, and anything
that needs to update every rendered frame (even if the framerate varies).

.. note::

   While both :py:class:`PreRender <ppb.events.PreRender>` and
   :py:class:`Render <ppb.events.Render>` are fired every frame, it is
   encouraged that games only use :py:class:`PreRender <ppb.events.PreRender>`
   to ensure proper sequencing. That is, it is not guaranteed when
   :py:meth:`on_render` methods are called with respect to the actual rendering.


Idle
~~~~
:py:class:`ppb.events.Idle` is fired whenever the core event loop has no more
events. While this is primarily used by systems for various polling things, it
may be useful for games which have low-priority calculations to perform.
