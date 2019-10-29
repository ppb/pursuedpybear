Technical Values
=================

Technical values describe our processes and design principles. They are
important to guide the trajectory of ``ppb`` as a software tool with a
sustainable development lifetime.

Design Values
--------------

You'll find some echoes of the original values here. They never went away, but
we've refined their points to make them more clear.

Students First
+++++++++++++++

We are an education focused project. In *every* API decision that should be the
first consideration.

By student, we mean children in a classroom, self taught folks picking up via
books or the internet, or people following along to a live tutorial.

No Apologies
+++++++++++++

The goal of No Apologies is to minimize students asking questions like "why does
this work differently here versus there?" Our API should make sense both in
regards to itself, and also in connection to the larger Python community.

Open Endedness
++++++++++++++++

We believe in the creativity of people, students, hobbyists, and professionals. We want to limit that creativity as little as reasonably possible. Yes, ``ppb`` is a 2D sprite-based engine, and that is unlikely to change. But we want to make sure that no genre, no style, no skill level is favored over another.

Progressive Reveal of Complexity
+++++++++++++++++++++++++++++++++

One of the goals of ``ppb`` is to appeal both to students just learning, but
being flexible and powerful enough to satisfy hobbyists. To that end, a lot of
complexity in ``ppb`` is hidden at first. You only need to have a deep
understanding of a piece of the system when you're ready to work with that
piece specifically.

You can see this in changes like adding ``systems`` and ``basic_systems`` which
made it easier to add your own subsystems to the engine without rebuilding the
entire thing from scratch.

Fun to Use
++++++++++++++

Look, games are fun, and ``ppb`` should be as fun to build with as the games it
makes. Any time we find a part of ``ppb`` kind of feels like a chore, we throw
it back on the drawing board.

Accepting Radical Change
++++++++++++++++++++++++++

The previous values all demonstrate that occasionally we need to make changes
to ``ppb`` to help it better align with these goals. That process can be fraught
for many. We have many developers who care about this code base, and seeing
their work changed can often be difficult. Beyond that emotional cost, changes
that break existing code makes old tutorials stale and would break our "No
Apologies" value. So we work fairly hard to maintain old functionality for as
long as possible, but will eventually need to be removed.

We've chosen the Northern Hemisphere summer for the time we launch breaking
changes.
