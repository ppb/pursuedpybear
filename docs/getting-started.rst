Getting Started
===================

This guide will start by getting you a fresh virtual environment and installing
ppb, then walk you through building a basic game (that will look a lot like our
sample game targets.py).

Prerequisites
--------------

Before you get started here, you should know the basics of Python. We use
classes extensively in ppb, and you should be comfortable with them. Consider
the `Python.org tutorial<https://docs.python.org/3/tutorial/index.html>` or
`automate the boring stuff <http://automatetheboringstuff.com/>` to get started.

Additionally, you need to have Python 3.6 or later on your machine. You can
install this via `Python.org<https://www.python.org/downloads/>` or
`Anaconda<https://www.anaconda.com/python-3-7-package-build-out-miniconda-release/>`
whichever is more comfortable for you.


Installing ppb
--------------

Once you have a working Python install, you're going to want to make a new
folder. Open your shell (Terminal on Mac, CMD or Powershell on Windows, your
favorite tool on Linux) and run:

All Systems::

   mkdir path/to/my_game
   cd path/to/my_game

``path/to/my_game`` can be any path you'd like, and the name can be anything you'd like.
We cd into it so we have a place to work.

The next step we're going to do is set up a virtual environment. Python 3.6
comes with a tool to create them, so in your terminal again:

All Systems::

   python3 -m venv .venv

This creates a new python environment that we'll use to make our game.
To make the next few steps easier, we'll want to activate our virtual
environment. This is different on Windows than anywhere else, so make sure to
use the right command.

Windows::

   .venv/bin/activate.bat

Linux and Mac::

   source .venv/bin/activate

After you've done this, your shell prompt should include ``(.venv)``. We're
ready for installing ``ppb``:

All Systems::

   pip install ppb

You should see a few libraries get put together in your terminal, and when
you have a prompt again, we're ready to go! So the next step is to make a new
file. If you're using an IDE, open your game folder in that and make a new file
called ``main.py``. If you're using a plain text editor, you'll want to open a
new file and save it as ``main.py``.

*Note: ``main.py`` is just being used as a convention and this file can be named
anything. If you change the name you'll want to use the new name in further commands.*

In your code file, add this:

``main.py``::

   import ppb


   ppb.run()

Save your file, then run it from your shell:

All Systems::

   python main.py

You should have a window! It will be 800 pixels wide and 600 pixels tall, and if you click the x
button, it should close.

Now let's add a sprite. Sprites are game objects that can often move and are
drawn to the screen. Add the following code after your ``import``. Note that
``ppb.run`` has a new parameter.

``main.py``::

   import ppb


   class Player(ppb.BaseSprite):
       pass


   def setup(scene):
       scene.add(Player())


   ppb.run(setup=setup)

When you run this, you should have the same window with a colored square in the
middle.

At this point, if you have a png on your computer, you can move it into your
project folder and call it ``player.png``. Rerun the file to see your character
on screen!

Our sprite is currently static, but let's change that. Inside your ``Player``
class, we're going to add a function and some class attributes.

``main.py``::

   class Player(ppb.BaseSprite):
       velocity = ppb.Vector(0, 1)

       def on_update(self, update_event, signal):
           self.position += self.velocity * update_event.time_delta

Now, your sprite should fly off screen.