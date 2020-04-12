Creativity Without Limits
==============================

Our focus on creativity without limits is about supporting users at all
skill levels, and to help guide them from their first lines of code through
contributing to open source.

From a game perspective, we don't want to discourage any genre of game
against any other. We don't want to discourage any given scale.

That isn't to mean we don't have some limitations: ``ppb`` is a 2d
sprite-based engine, it's built in Python, and it is code first.

Code First
-----------------

The primary reason we want ``ppb`` to be code first is because it allows the
primary long term limitations set on users is the limitations of the Python
language itself.

Code first also means that learning ``ppb`` means learning patterns that can be
applied to other kinds of software. A student who learns with ``ppb``
shouldn't need to ask "what comes next", the answer should apparent:
Whatever the next project is that interests them.

No Early Optimization
------------------------

This is one of those general rules of software development, but it's
something that creates limitations. If we over optimize our toolset for one
genre of video game, it adds friction to others. New features should be
generally applicable or explicitly optional.

The primary example of this is in the basic setup for ppb as a simple event loop
with the update pattern at its core. This is because it's the most generally
applicable pattern we have available. We provide a multi-phase update system in
features for games that need the ability to stage updates instead of
immediately shifting the state.

Support All Users
----------------------

We're Students First, but students aren't students forever, and we want
``ppb`` to grow with them. From their first tutorials through to their first
shipped video game, and hopefully: to their first open source contribution.
This is about making sure the resources and community are there to help
develop ``ppb`` users.

From the user perspective, clear tutorials and example code. Open
discussions about the design of the system. Type hinting to allow the tools to
help guide. Progressive revelation of complexity. All of this is meant to guide
a user from student to pro.

Once they're ready to contribute we care about well defined processes and
guidelines. A strong description of how documentation is laid out. Where
code lives and why.
