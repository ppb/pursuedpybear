Animation
=========
.. py:module:: ppb.features.animation

This is a simple animation tool, allowing individual frame files to be composed
into a sprite animation, like so:

.. code-block:: python

   import ppb
   from ppb.features.animation import Animation

   class MySprite(ppb.Sprite):
       image = Animation("sprite_{1..10}.png", 4)


Multi-frame files, like GIF or APNG, are not supported.

Pausing
~~~~~~~
Animations support being paused and unpaused. In addition, there is a "pause
level", where multiple calls to :py:meth:`pause` cause the animation to become
"more paused". This is useful for eg, pausing on both scene pause and effect.

.. code-block:: python

   import ppb
   from ppb.features.animation import Animation

   class MySprite(ppb.Sprite):
       image = Animation("sprite_{1..10}.png", 4)

       def on_scene_paused(self, event, signal):
           self.image.pause()

       def on_scene_continued(self, event, signal):
           self.image.unpause()

       def set_status(self, frozen):
           if frozen:
               self.image.pause()
           else:
               self.image.unpause()


Reference
~~~~~~~~~
.. autoclass:: ppb.features.animation.Animation
   :members:
   :special-members:
   :exclude-members: clock, __weakref__, __repr__

