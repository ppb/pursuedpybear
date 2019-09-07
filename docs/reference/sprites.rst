.. py:currentmodule:: ppb.sprites

=================
All About Sprites
=================

.. automodule:: ppb.sprites

------------------
Default Sprite
------------------

This is the class you should instantiate or subclass for your games unless
you are changing the defaults.

.. autoclass:: ppb.Sprite
   :members:
   :inherited-members:

Note that ``ppb.BaseSprite`` is deprecated in favor of ppb.Sprite. Scheduled
for removal in ppb v0.8.0.

-------------------
Feature Mixins
-------------------

These mixins are the various features already available in Sprite. Here for
complete documentation.

.. autoclass:: ppb.sprites.RenderableMixin
   :members:

.. autoclass:: ppb.sprites.RotatableMixin
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


-------------------
Internals
-------------------

These classes are internals for various APIs included with mixins.

.. autoclass:: ppb.sprites.Side
   :members:
