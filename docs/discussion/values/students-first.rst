Student First
====================

PursuedPyBear is, above all other usages, a tool for learning. We continually
find ways to reduce the amount of previous knowledge is required to get to your
first functioning video game. The greatest example of this is the evolution of
ppb start up throughout time:

Originally, ppb was a strict MVC framework with required dependency injection
and little concept of sensible defaults. You had to know what each part of the
system was, instantiate it, and then pass it to the next component.

We kept the dependency injection but rebuilt the engine to have strong opinions
and defaults at every level of the system. However, you had to know what a
context manager was, and how to use one.

Today, we can make a functional game in 15 lines of code, and you never need to
see the underlying context manager.

Progressive Revealing of Complexity
--------------------------------------------

We want to encourage exploration and flexibility of the underlying tool, and one
of the ways we achieve this is through only revealing the complexity of the tool
at the point you must understand it to do something. Our "Hello World!" example
requires only understanding how to invoke functions and how to write your own:
the fundamental building blocks of Python programming. In the next hour of
exploration, it's possible to learn what objects are, how classes are defined
and using them yourself. And from there, you can begin to learn more complex
features of Python.

Whenever possible, we prefer to provide powerful and sensible defaults, but with
as many options for advanced users as possible.

No Apologies
-------------------------

Every language and tool ends up with a number of quirks known as "wats". In
``ppb`` we tend to call them "warts": they're places where the knowledge you
have of how a system works is thrown a curve ball that requires reassessing what
you know. There are popular wat talks for both Python and Javascript to get a
feel for what we mean.

One way this bears out is that no matter what level your knowledge of ``ppb``,
learning something new should only add to that knowledge, not require
reassessment.

We also try to reduce the number of times a user is forced to ask "why is it
like this and not like that?" Things that are like messages should use the event
queue. State should be contained by objects at the right level of abstraction.
Things should fit the model.
