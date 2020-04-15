.. py:currentmodule:: ppb.engine

================
GameEngine
================

The :py:class:`GameEngine` is the literal beating heart of ppb: It publishes the
event queue, is the source of the :class:`~events.Idle` event, and is the
root container of the object tree.

Some of the engine of the API is definitely intended for advanced users. Use
the various methods of :py:class:`GameEngine` with caution.

.. autoclass:: ppb.GameEngine
    :members:
    :undoc-members:
