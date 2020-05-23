Getting Started
===================

This guide will start by getting you a fresh virtual environment and installing
ppb.  It will then walk you through building a basic game that will look a lot like our
sample game targets.py.

Prerequisites
--------------

Before you get started here, you should know the basics of Python. We use
classes extensively in ppb, and you should be comfortable with them. Consider
the `Python.org tutorial <https://docs.python.org/3/tutorial/index.html>`_ or
`automate the boring stuff <http://automatetheboringstuff.com/>`_ to get started.

Additionally, you need to have Python 3.6 or later on your machine. You can
install this via `Python.org <https://www.python.org/downloads/>`_ or
`Anaconda <https://www.anaconda.com/python-3-7-package-build-out-miniconda-release/>`_
whichever is more comfortable for you.


Installing ppb
--------------

Once you have a working Python install, you're going to want to make a new
folder. Open your shell (Terminal on Mac, CMD or Powershell on Windows, your
favorite tool on Linux) and run:

All Systems::

   mkdir -p path/to/my_game
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


Additionally, on Linux only you must install the SDL library:

Debian, Ubuntu::

   sudo apt install libsdl2-2.0-0 libsdl2-mixer-2.0-0 libsdl2-image-2.0-0 libsdl2-gfx-1.0-0 libsdl2-ttf-2.0-0

Fedora, CentOS, RHEL ::

    sudo dnf install SDL2 SDL2_ttf SDL2_image SDL2_gfx SDL2_mixer

You should see a few libraries get put together in your terminal, and when
you have a prompt again, we're ready to go!

A Basic Game
------------

The next step is to make a new file. If you're using an IDE, open your game
folder in that and make a new file called ``main.py``. If you're using a plain
text editor, you'll want to open a new file and save it as ``main.py``.

*Note:* ``main.py`` *is just being used as a convention and this file can be
named anything. If you change the name you'll want to use the new name in
further commands.*

In your code file, add this:

``main.py``::

   import ppb


   ppb.run()

Save your file, then run it from your shell:

All Systems::

   python main.py

You should have a window! It will be 800 pixels wide and 600 pixels tall, and if you click the x
button (or the red dot on MacOS), it should close.

Now let's add a ``Sprite``. Sprites are game objects that can often move and are
drawn to the screen. Add the following code after your ``import``. Note that
``ppb.run`` has a new parameter.

``main.py``::

   import ppb


   class Player(ppb.Sprite):
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

   class Player(ppb.Sprite):
       velocity = ppb.Vector(0, 1)

       def on_update(self, update_event, signal):
           self.position += self.velocity * update_event.time_delta

Now, your sprite should fly up off the screen.

Taking Control
--------------

This is cool, but most people expect a game to be something you can interact
with. Let's use keyboard controls to move our ``Player`` around. First things
first, we have some new things we want to import:

``main.py``::

   import ppb
   from ppb import keycodes
   from ppb.events import KeyPressed, KeyReleased

These are the classes we'll want in the next section to work.

The next step is we'll need to redo out ``Player`` class. Go ahead and delete
it, and put this in its place:

``main.py``::

   class Player(ppb.Sprite):
       position = ppb.Vector(0, -3)
       direction = ppb.Vector(0, 0)
       speed = 4

       def on_update(self, update_event, signal):
           self.position += self.direction * self.speed * update_event.time_delta

This new ``Player`` moves a certain distance based on time, and a direction
vector and its own speed. Right now, our direction is not anything (it's the
zero-vector), but we'll change that in a moment. For now, go ahead and run the
program a few times, changing the parameters to the ``direction`` ``Vector`` and
the speed and see what happens. You can also modify ``position`` to see where
you like your ship.

Now that you're comfortable with the base mechanics of our new class, revert
your changes to ``position``, ``speed``, and ``direction``. Then we can wire up
our controls.

First, we're going to define the four arrow keys as our controls. These can be
set as class variables so we can change them later:

``main.py``::

   class Player(ppb.Sprite):
       position = ppb.Vector(0, -3)
       direction = ppb.Vector(0, 0)
       speed = 4
       left = keycodes.Left
       right = keycodes.Right

The ``keycodes`` module contains all of the keys on a US based keyboard. If you
want different controls, you can look at the module documentation to find ones
you prefer.

Now, under our ``on_update`` function we're going to add two new event handlers.
The snippet below doesn't include the class attributes we just defined, but
don't worry, just add the new methods at the end of the class, beneath your
``on_update`` method.

``main.py``::

   class Player(ppb.Sprite):


       def on_key_pressed(self, key_event: KeyPressed, signal):
           if key_event.key == self.left:
               self.direction += ppb.Vector(-1, 0)
           elif key_event.key == self.right:
               self.direction += ppb.Vector(1, 0)

       def on_key_released(self, key_event: KeyReleased, signal):
           if key_event.key == self.left:
               self.direction += ppb.Vector(1, 0)
           elif key_event.key == self.right:
               self.direction += ppb.Vector(-1, 0)

So now, you should be able to move your player back and forth using the arrow
keys.

Reaching Out
------------

The next step will to make our player "shoot". I use shoot loosely here,
your character can be throwing things, or blowing kisses, or anything, the only
mechanic is we're going to have a new object start at the player, and fly up.

First, we need a new class. We'll put it under ``Player``, but above ``setup``.


``main.py``::

   class Projectile(ppb.Sprite):
      size = 0.25
      direction = ppb.Vector(0, 1)
      speed = 6

      def on_update(self, update_event, signal):
          if self.direction:
              direction = self.direction.normalize()
          else:
              direction = self.direction
          self.position += direction * self.speed * update_event.time_delta

If we wanted to, we could pull out this ``on_update`` function into a mixin that
we could use with either of these classes, but I'm going to leave that as an
exercise to the reader. Just like the player, we can put a square image in the
same folder with the name ``projectile.png`` and it'll get rendered, or we can
let the engine make a colored square for us.

Let's go back to our player class. We're going to add a new button to the class
attributes, then update the ``on_key_pressed`` method. Just like before, I've
removed some code from the sample, you don't need to delete anything here, just
add the new lines: The class attributes ``right`` and ``projector`` will go
after the line about ``speed`` and the ``new elif`` will go inside your
``on_key_pressed`` handler after the previous ``elif``.

``main.py``::

   class Player(ppb.Sprite):

       right = keycodes.Right
       projector = keycodes.Space

       def on_key_pressed(self, key_event: KeyPressed, signal):
           if key_event.key == self.left:
               self.direction += ppb.Vector(-1, 0)
           elif key_event.key == self.right:
               self.direction += ppb.Vector(1, 0)
           elif key_event.key == self.projector:
               key_event.scene.add(Projectile(position=self.position + ppb.Vector(0, 0.5)))

Now, when you press the space bar, projectiles appear. They only appear once
each time we press the space bar. Next we need something to hit with
our projectiles!

Something to Target
-------------------

We're going to start with the class like we did before. Below your Projectile
class, add

``main.py``::

   class Target(ppb.Sprite):

       def on_update(self, update_event, signal):
           for p in update_event.scene.get(kind=Projectile):
               if (p.position - self.position).length <= self.size:
                   update_event.scene.remove(self)
                   update_event.scene.remove(p)
                   break

This code will go through all of the ``Projectiles`` available, and if one is inside
the ``Target``, we remove the ``Target`` and the ``Projectile``. We do this by
accessing the scene that exists on all events in ppb, and using its ``get``
method to find the projectiles. We also use a simplified circle collision, but
other versions of collision can be more accurate, but left up to your research.

Next, let's instantiate a few of our targets to test this.

``main.py``::

   def setup(scene):
       scene.add(Player())

       for x in range(-4, 5, 2):
           scene.add(Target(position=ppb.Vector(x, 3)))

Now you can run your file and see what happens. You should be able to move back
and forth near the bottom of the screen, and shoot toward the top, where your
targets will disappear when hit by a bullet.

Congratulations on making your first game.

For next steps, you should explore other :doc:`tutorials </tutorials/index>`.
Similarly, you can discover new events in the
:doc:`event documentation </reference/events>`.
