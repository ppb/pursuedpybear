Collisions
==========

.. automodule:: ppb.features.collision

Basic usage is as follows:

.. code-block:: python

    import ppb
    from ppb.features import CollisionCheckerSystem

    with ppb.GameEngine(ppb.BaseScene, systems=[CollisionCheckerSystem]):
        ppb.run()

To add the colliders, just add the mixin to the list of parent classes.
If this is the only mixin, you can subclass them directly as they are
already subclasses of BaseSprite.

    .. autoclass:: CollisionCheckerSystem
        :members:

    .. autoclass:: CollidedWithMixin
        :members:

    .. autoclass:: CanCollideCircleMixin
        :members:

    .. autoclass:: CanCollideCircleMixin
        :members:
