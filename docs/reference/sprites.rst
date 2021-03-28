.. py:module:: ppb.sprites

=================
Sprites
=================

.. automodule:: ppb.sprites
   :noindex:

------------------
Concrete Sprites
------------------

Concrete sprites are a combination of :class:`BaseSprite` and various mixins.
They implement a number of useful features for game development and should be
the primary classes you subclass when building game objects.

.. autoclass:: ppb.Sprite
   :members:
   :inherited-members:

.. autoclass:: ppb.RectangleSprite
   :members:
   :inherited-members:

-------------------
Feature Mixins
-------------------

These mixins are the various features already available in Sprite. Here for
complete documentation.

.. autoclass:: ppb.sprites.RenderableMixin
   :members:

.. autoclass:: ppb.sprites.RotatableMixin
   :members:

.. autoclass:: ppb.sprites.RectangleShapeMixin
   :members:

.. autoclass:: ppb.sprites.SquareShapeMixin
   :members:

-------------------
Base Classes
-------------------

The base class of Sprite, use this if you need to change the low level
expectations.

.. autoclass:: ppb.sprites.BaseSprite
   :members:
   :inherited-members:
