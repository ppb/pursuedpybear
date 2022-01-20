===============================
Opening a Window
===============================

So we've installed everything we need, but it's always a good idea to make
sure our environment is right before moving on. A good first step for any video
game is to make sure you can make an empty window.

Inside your :doc:`project directory <setup>` we need to create a file. Do so using your
code editor, and call it ``main.py``. Make sure to open it so we can add code
to it.

.. note:: We're using ``main.py`` here, but like the name of your virtual
   environment, this is just convention. If you change it, make sure to replace
   the name ``main.py`` in any console commands shown later. We do suggest
   keeping the name, though.

If you haven't already, open up ``main.py`` in your code editor. Inside, add
the following code:

.. code-block:: python
   :caption: main.py
   :linenos:

   import ppb

   ppb.run()

Save this file and go back to your terminal. There, you should enter the
following command to run your game.

.. code-block::
   :caption: Terminal

   python main.py

You should have a window open that looks like this:

(Add image.)

To run any python script (not just our ``main.py``) you call ``python``, add a
space and then the name of the script you're wanting to run. There's lots of
other options, but this is all you need to know so far.

Before we continue, we're going to do one more thing. The default resolution of
800x600 is great, but you might want a bigger (or smaller) window. We're going
to add a constant value and give that to ppb to tell it how big of a window we
want. We'll also add a title to our game, which shows up in the title bar of
the window we create.

.. code-block::
   :caption: main.py
   :linenos:
   :emphasize-lines: 3,5

   import ppb

   RESOLUTION = (1200, 900)

   ppb.run(resolution=RESOLUTION, title="Hello Window!")

Save this and rerun it and the screen should be bigger this time and say
"Hello Window!" on the top.

The reason ``RESOLUTION`` is spelled with all caps is because this is a what
programmers call a constant. As a community, Python developers use `special
capitalization rules`_ to tell the difference between different kinds of
variables. The value is what we call a tuple, which is collection of values
that can't be changed. These values are the width and height of the window in
screen pixels.

Just defining this value isn't enough. The :class:`ppb.GameEngine` doesn't look
for values, you have to tell it what you want. In this case the keyword argument
`resolution` is how you inform ``ppb`` what you want. So in this case,
``resolution=RESOLUTION`` is giving our constant to the engine to change the
size of the window.

You can change either the width or the height in ``RESOLUTION`` to find a
window size you like. The Atari 2600 had a maximum resolution of 160x192, but
this is exceptionally small on modern screens. It's better to pick bigger, we
can manipulate the size of the things on the screen later. When you change the
value, you should use ``python main.py`` again to see the result. Keep experimenting

Once you've found a screen size and shape you like, we can move on to putting
something on screen.

.. _special capitalization rules: https://www.python.org/dev/peps/pep-0008/
