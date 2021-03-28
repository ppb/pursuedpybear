============================================
A Ball That Bounces
============================================

1. Sprites
    1. vectors
    2. Rendering
    3. events
2. setup function
3. Basic collision detection
4. Reflections

Our next major step is to create a ball. The ball should move a little each
frame, bounce off the edges of the screen, and look like a ball. In order to do
that we'll need to create a :class:`~ppb.Sprite``, then put a copy of that
sprite into the game :class:`~ppb.Scene`.

.. todo:: Explain basic object orientation

Right now, we don't need to define our own scene, ppb provides one for us when
we call :func:`~ppb.run`. The run function does accept a function argument that
lets us initialize this first scene.

.. code-block::
   :caption: main.py
   :linenos:
   :emphasize-lines: 3,4,6

   RESOLUTION = (1200, 900)

   def setup(scene):
       scene.background_color = (0, 0, 0)

   ppb.run(setup, resolution=RESOLUTION)

In this step, we will set the background color of our scene object to pure
black. This better matches our example game, and demonstrates writing a
function.

Additionally, we've added the setup function as an argument to the call of the
ppb.run function. With that in place, let's explore :class:`~ppb.Sprite`.

Let's start by using the default sprite class directly:

.. code-block::
   :caption: main.py
   :linenos:
   :emphasize-lines: 3

   def setup(scene):
       scene.background_color = (0, 0, 0)
       scene.add(ppb.Sprite(image=ppb.Circle(255, 255, 255), size=1))

The :class:`~ppb.Sprite` does a lot of heavy lifting for us. Once added to a
running scene, it'll display its image at its location on the screen. If you run
your main script now, you should see a black background with a white circle in
the center. The size parameter allows us to adjust the size of the object on
screen. If you want the ball bigger (or smaller!) you can adjust this parameter.

.. todo:: Explain the __init__

So we now have a ball that looks like a ball, but it doesn't move. So we're
going to need to edit this code. First, let's define our first class.

.. code-block::
   :caption: main.py
   :linenos:
   :emphasize-lines: 4-6, 10

   RESOLUTION = (800, 600)


   class Ball(ppb.Sprite):
       image = ppb.Circle(255, 255, 255)
       size = 1


   def setup(scene):
       scene.background_color = (0, 0, 0)
       scene.add(Ball())

Run your program again and you'll note that nothing should have changed from
our last run. This version is functionally identical to our last step. Let's
talk about what's going on in this block now:

The `class` keyword tells Python we're creating a class, a type of blue print
for things we put in our game. The `Ball` is a name we give our class, you can
name yours something different, but letting yourself know the class is for the
tennis ball is good practice. Inside the parentheses we're telling python that
this class is based on the :class:`ppb.Sprite` class. This lets us share some
code and not write it ourselves.

Below that definition, you'll notice the indents, and we assigned some
variables. These variables are special and called class attributes. We can use
these as defaults for every object we make using this class. Combined with the
initialization code from ppb, it gives us a very powerful way to customize
objects.

The next step is to get our ball moving. To do this, we're going to use vectors
and integration. (Don't worry, you won't need to know how these work, ppb
handles much of the work for us.)

We use vectors in ppb for the position of our :class:`~ppb.Sprite <Sprites>` and
in this case will also use it for a velocity vector. To do so, we'll set a
default velocity of `ppb.Vector(0, 0)` (this would be a ball that isn't moving,
like the one we already have) and then we'll use the velocity vector to move the
position of the ball each time we step through the simulation.

.. code-block::
   :caption: main.py
   :linenos:

   class Ball(ppb.Sprite):
       image = ppb.Circle(255, 255, 255)
       size = 1
       velocity = ppb.Vector(0, 0)

This is a small change, and just like last time, doesn't change the behavior.
To change that, we're going to want to respond to events.

In ppb, events are what drive all the action. The most important event is the
:class:`~ppb.events.Update` event, which happens about sixty times per second
by default. To respond to any event, you need to write a method (a special kind
of function attached to a class) that looks like this:

.. code-block::

   def on_update(self, event, signal):
       self.do_the_thing()

All event handlers use this pattern. The name of these methods is important:
`ppb` always looks for a method named 'on' followed by an underscore and the
name of the event in snake case. In the case of `Update` this looks like
`on_update`, but for a longer name, like the `PreRender` event it would look
like `on_pre_render`.

So to get our ball moving, we'll write one of these handlers in our `Ball`
class.

.. code-block::
   :caption: main.py
   :linenos:
   :emphasize-lines: 6, 7

   class Ball(ppb.Sprite):
       image = ppb.Circle(255, 255, 255)
       size = 1
       velocity = ppb.Vector(0, 0)

       def on_update(self, event, signal):
           self.position += self.velocity * event.time_delta

   def setup(scene):

This function is called each time an update event happens, and the ball adds its
velocity (often a measurement of change in position per second) and multiplies
it by the update event's time_delta attribute so that we only apply as much
velocity as is relevant in that time period. If we just added velocity to
position our ball would move almost 60 times faster than intended.

If you run it again, you'll see we still haven't changed what the program does.

Let's finally make it happen:

.. code-block::
   :caption: main.py
   :linenos:
   :emphasize-lines: 3

   def setup(scene):
       scene.background_color = (0, 0, 0)
       scene.add(Ball(velocity=ppb.directions.Left))

And now our ball is moving on screen! This is very slow for now, that's
intentional, but this does demonstrate the ppb.directions module, which has a
bunch of length 1 vectors for you to use.