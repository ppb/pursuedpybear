Radical Acceptance
===============================

While we do think the greater idea of radical acceptance is important, with
regard to ppb, radical acceptance is about inclusion, experimentation, and
willingness to question our assumptions.


Accept Significant Change
-------------------------------

We don't want to be afraid of change. PursuedPyBear is a project about the API,
and how humans interact with computers changes over times. We shouldn't be
afraid to abandon API decisions if they stop proving useful.

The "back end" of ``ppb`` has changed significantly on four ocassions so far,
changing when some limitation was reached. Originally strictly powered by
dependency injection, we learned that sensible defaults are incredibly
important. That shifted to a single monolithic API that ran all code directly
in line. Then we peeled out the first few subsystems. They were still called
directly, but you could work on them separately from the engine itself. Then we
moved to the ``Idle`` event and messaging as the way to interact between
subsystems and the engine itself. In time, even this pattern may prove limiting
and be changed.


Inclusion
------------------

PursuedPyBear started as the solo project of a trans woman with a non-standard
education background. As it's grown, we have sought out and encouraged
contributors from diverse backgrounds. We have a
`code of conduct <https://ppb.dev/coc.html>`_ that covers all participation in
the project.

We like being a diverse project, and we will protect the environment that let's
it be that way.

Education
++++++++++++++++

While we are a tool for education, we acknowledge that not all learners learn
the same way. The author was home schooled and self taught software after
college. Many of the teachers who advise the project come from more traditional
education backgrounds.

We seek to support learners no matter their education path.

Race
+++++++++++

Similar to education, race should not be an obstacle to using or contributing to
``ppb``. The maintainers recognize that while that might be a thing we can
obtain in the project, society is racist and we must work to be anti-racist in
how we manage the project and community.

Gender
+++++++++++++

The current team of maintainers are all trans feminine. We seek out women and
gender minorities to contribute to the project. We embrace all genders and hope
to keep ``ppb`` the kind of community where it is safe to be who you are.


Be Willing To Try
---------------------

When someone is willing to do the work for an idea the rest of the team isn't
sure about, let them take a chance at it. Usage will tell us if the solution is
appropriate, not our personal biases.
