==============
Text Rendering
==============

ppb supports basic text rendering: single font, single style, no wrapping. Rendered fonts are graphical Assets that can be used any place you'd use :py:class:`ppb.Image`

.. code-block:: python

   class Label(ppb.sprite):
       image = ppb.Text("Hello, World", font=ppb.Font("resources/noto.ttf", size=12))

TrueType and OpenType fonts (both ``.ttf``) are supported, but must be shipped with your game. (System fonts are not supported.)

Note that fonts require a size in points. This controls the size the text is rendered at, but the size on screen is still controlled by :py:attr:`Sprite.size`.

.. autoclass:: ppb.Font

.. autoclass:: ppb.Text
