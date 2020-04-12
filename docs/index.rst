Welcome to PursuedPyBear's documentation!
=========================================

PursuedPyBear, also known as ``ppb``, exists to be an educational resource. Most
obviously used to teach computer science, it can be a useful tool for any topic
that a simulation can be helpful.

A Game Engine
-------------

At its core, ``ppb`` provides a number of features that make it perfect
for video games. The ``GameEngine`` itself provides a pluggable
subsystem architecture where adding new features is as simple as
subclassing and extending ``System``. Additionally, it contains a state
stack of ``Scenes`` simple containers that let you organize game scenes
and UI screens in a simple way.

The entire system uses an event system which is as extensible as the
rest of the system. Register new values to existing event types, and
even overwrite the defaults. Adding a new event system is as simple as
calling ``Engine.signal`` with a new datatype. Instead of a publisher
system the engine knows everything in its own scope and only calls
objects with appropriate callbacks. The most basic event is ``Update``
and your handlers should match the signature
``on_update(self, update_event, signal)``.

Guiding Principles
------------------

Because ``ppb`` started to be a game framework great for learning with,
the project has a few longterm goals:

Education Friendly
~~~~~~~~~~~~~~~~~~

Non-technical educators should feel comfortable after very little
training. While some programming knowledge is required, the ability to
think in objects and responses to events allows educators to only focus
on their lessons.

Idiomatic Python
~~~~~~~~~~~~~~~~

A project built on ``ppb`` should look like idiomatic Python. It also
should look like modern Python. As such, we often add new language
features as soon as they’re available, letting a new user always know
ppb runs on the latest Python.

Object Oriented and Event Driven
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``ppb`` games are built out of instances of objects. Each object only has
enough information to respond to the event provided, which always includes the
current ``BaseScene``. Because ``ppb`` doesn’t have a master list of events,
you can provide new ones simply to add more granular control over your game.

Hardware Library Agnostic
~~~~~~~~~~~~~~~~~~~~~~~~~

Because ``ppb`` strongly tries to be extensible and pluggable, each
hardware extension can provide its own hooks to ``ppb``, and you can
nearly seamlessly switch between various Python libraries.

Fun
~~~

One of the maintainers put it best:

   If it’s not fun to use, we should redo it

ppb is about filing off the rough edges so that the joy of creation and
discovery are both emphasized. A new user should be able to build their
first game in a few hours, and continue exploring beyond that.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   getting-started
   tutorials/index
   howto/index
   reference/index
   discussion/index
