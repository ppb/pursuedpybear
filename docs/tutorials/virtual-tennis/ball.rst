============================================
A Ball That Bounces
============================================

Our next major step is to create a ball. The ball should move a little each
frame, bounce off the edges of the screen, and look like a ball. In order to do
that we'll need to create a :class:`~ppb.Sprite``, then put a copy of that
sprite into the game :class:`~ppb.Scene`.

Right now, we don't need to define our own scene, ppb provides one for us when
we call :func:`~ppb.run`. The run function does accept a function argument that
lets us initialize this first scene.

.. code-block::
   :caption: main.py
   :lineno-start: 3
   :emphasize-lines: 4-8

   RESOLUTION = (1200, 900)


   def setup(scene):
       scene.background_color = (0, 0, 0)


   ppb.run(setup, resolution=RESOLUTION, title="Hello Window!")

In this step, we will set the background color of our scene object to pure
black. This better matches our example game, and demonstrates writing a
function.

Additionally, we've added the setup function as an argument to the call of the
ppb.run function. With that in place, let's explore :class:`~ppb.Sprite`.

Let's start by using the default sprite class directly:

.. code-block::
   :caption: main.py
   :lineno-start: 6
   :emphasize-lines: 3

   def setup(scene):
       scene.background_color = (0, 0, 0)
       scene.add(ppb.Sprite(image=ppb.Circle(255, 255, 255), size=1))


   ppb.run(setup, resolution=RESOLUTION, title="Hellow Window!")

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
   :lineno-start: 3
   :emphasize-lines: 4-6, 11

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
   :lineno-start: 6
   :emphasize-lines: 4

   class Ball(ppb.Sprite):
       image = ppb.Circle(255, 255, 255)
       size = 1
       velocity = ppb.Vector(0, 0)


   def setup(scene):

This is a small change, and just like last time, doesn't change the behavior.
To change that, we're going to want to respond to events.

.. note::
   So vectors can be complicated if you've never used them before, but ppb
   does a lot so you can ignore the specifics of the math. Just know that the
   first number in the vector (called the x component) represents a change from
   left-to-right or right-to-left. The second number (the y component)
   represents up and down. Additionally, you can perform some useful
   mathematical operations on them.

In ppb, events are what drive all the action. The most important event is the
:class:`~ppb.events.Update` event, which happens about sixty times per second
by default. To respond to any event, you need to write a method (a special kind
of function attached to a class) that looks like this (don't write this in
your file!):

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
   :lineno-start: 6
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
   :lineno-start: 15
   :emphasize-lines: 3

   def setup(scene):
       scene.background_color = (0, 0, 0)
       scene.add(Ball(velocity=ppb.directions.Left))

And now our ball is moving on screen! This is very slow for now, that's
intentional, but this does demonstrate the ppb.directions module, which has a
bunch of length 1 vectors for you to use.

If you watch for a bit, the ball will wander right off the left hand side of
the screen. This is pong, though, so we're going to want to bounce off the
walls and ceiling. To do that, we're going to add a check to make sure the ball
is still inside the camera.

.. admonition:: Camera?

   I know, the camera is a new concept, but all you need to know is the camera
   helps ppb figure out what in your scene needs to get drawn to the screen
   and it has sides we can use to measure where the ball is.

Before we move our ball each frame, we're going to check if any side of the
square around our ball (this is called an axis aligned bounding box and ppb
gives us this for free) is beyond the same wall of the camera's view. So
top-to-top, left-to-left and so on.

.. code-block::
   :caption: main.py
   :lineno-start: 11
   :emphasize-lines: 2-18

   def on_update(self, event, signal):
       camera = event.scene.main_camera
       reflect = ppb.Vector(0, 0)

       if self.left < camera.left:
           reflect += ppb.directions.Right

       if self.right > camera.right:
           reflect += ppb.directions.Left

       if self.top > camera.top:
           reflect += ppb.directions.Down

       if self.bottom < camera.bottom:
           reflect += ppb.directions.Up

       if reflect:
           self.velocity = self.velocity.reflect(reflect.normalize())
       self.position += self.velocity * event.time_delta

This was a lot of code in one shot, but don't worry, I'll explain.
First, we get the scene's camera. Inside of an event handler, you can
always access the current scene with `event.scene`. All scenes get a
camera, which you can get with `scene.main_camera`. Here, we store that camera
in a variable called camera. This makes it easier to type the rest of this
routine.

Next, we set up a reflect vector. What we're trying to create is something
called a surface normal. You can think of it as an arrow pointing straight
away from an object. For example a tabletop has a surface normal that points
straight up.

In our case, there are four surfaces we care about: the four walls of the
camera. (They're not actually walls, and you saw previously!) When the
camera reaches any edge, measured when the side of the ball goes past the value
for that wall, the surface normal is pointing the opposite way.

We add all of the relevant normals together, and then check if they're greater
than 0. If they are, we set our velocity to our velocity vector reflected
across our reflect vector normalized.

.. note::
   A vector with no length (specifically ``ppb.Vector(0, 0)``) is called the
   zero vector. We can use this property to our advantage and only do a
   reflection when we have a vector to work with.

With this in place, you have a bouncing ball, the first major component of our
virtual tennis game! Before moving on, go ahead and try changing the initial
velocity vector (inside the setup function) by using different directions and
multiplying it by different values. You can also experiment with changing the
size of the ball and changing the colors.
