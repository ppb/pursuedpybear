Maintenance Schedules
===========================================================

This is a record of the intended maintenance schedules for various releases
and dependency support.

Python Version Support
-----------------------------------------------------------

PursuedPyBear projects will support at least the latest version of
`pypy <https://www.pypy.org/download.html>`_ and the latest two versions of
`C Python <https://www.python.org/downloads/>`_

We tend to start testing new versions of cPython when they reach the release
candidate stage, but don't guarantee compatibility until at least one ppb
release after the latest Python release.

We drop older versions of Python when we begin using features from a newer
version of Python. A future example of this would be dropping Python 3.7
when we start using
`assignment operators <https://www.python.org/dev/peps/pep-0572/>`_. This
means the oldest version of Python ppb supports may be older than the two
versions we promise to support.

Release Schedules
------------------------------------------------------------

PursuedPyBear targets four releases a year, based on the solstices and
equinoxes:

* Around the northward equinox, which is about March 20.
* Around the northern solstice, which is about June 20.
* Around the southward equinox, which is about September 20.
* Around the southern solstice, which is about December 21st.

We prefer to use the directional names of the solstices and equinoxes as we
support a global community. Naming them after their seasons would leave out
portions of the world.

About four weeks before the target release date, we freeze any new feature
merges. This means any PR that is a feature or enhancement (not a bug fix,
documentation change, or examples) may be approved, but held until after the
release.

At the same time as freeze, we try to release the first beta of the new
version. If there has been any changes, we like to release a new beta the
next week, and one more the week after if bug fixes are still being
submitted.

If the beta has been stable, at 2 weeks before the release, we like to cut
a release candidate. At this point the majority of accepted PRs are
documentation and bug fix related. We will cut as many release candidates as
we see fit over the following two weeks.

On or around the expected release date, we will cut a final release.

Deprecations and API Breakages
-----------------------------------------------------------

PursuedPyBear is currently in a pre-release state. Many of its APIs have
proven effective and long lasting. Other portions are still highly
experimental as we find the correct developer experience.

Because of this, we have come to support deprecating APIs as best we can.
Some APIs cannot be deprecated cleanly, and we will make note that in
change logs.

In general, we seek to provide a deprecation warning under an existing name
for at least two releases. For example, if we deprecate or
significantly change an API in v0.10 it will also be available under a
deprecation warning in v0.11 and is likely to be, but not guaranteed to be,
available in v0.12.

After freeze, we will reexamine this deprecation policy in light of major
version changes.

While it is not true now, it has been requested by a number of educators to
limit major version changes to the Northern Solstice release. If you have an
opinion on this, please join one of the discussion channels to add to this
understanding.
