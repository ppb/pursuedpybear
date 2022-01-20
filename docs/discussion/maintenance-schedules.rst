.. _maintenance-schedules:

Maintenance Schedules
===========================================================

This is a record of the intended maintenance schedules for various releases
and dependency support.

Python Version Support
-----------------------------------------------------------

PursuedPyBear supports all `CPython <https://www.python.org/downloads/>`_
versions supported by the PSF at any level.

We tend to start testing new versions of cPython when they reach the release
candidate stage, but don't guarantee compatibility until at least one ppb
release after the formal release of a Python version.

We drop old versions of Python during the breaking release each year (see next
section) to prevent breaking mid year for school environments.

Release Schedules
------------------------------------------------------------

PursuedPyBear targets four releases a year, based on the solstices and
equinoxes:

* Around the northward equinox, which is about March 20th.
* Around the northern solstice, which is about June 20th.
  (This will always be a x.0 release.)
* Around the southward equinox, which is about September 20th.
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

On Versioning
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

You may recognized from the note on the Northern Solstice release that ``ppb``
uses a form of Calendar Versions or calver. Given a release version like
``y.m.p``:

The ``y`` is a year tag. Version 1.0 is the June 2021 release of ``ppb``.

The ``m`` is a minor version. We will bump this during the three other releases
of the year. It starts at 0 and should never be higher than 3.

The ``p`` is a patch. For the most part this will be excluded from the
version string. If it is present, it represents a bug fix release outside of the
above release cadence.

Deprecations and API Breakages
-----------------------------------------------------------

PursuedPyBear as a project seeks to minimize how much we break existing users
experiences. While we want to be able to continue to experiment and evolve the
APIs for performance, we need strict rules about how we implement and deliver
them.

When an API change becomes necessary we will follow the following steps:

1. In the next ppb release the existing behavior and name will throw a
   DeprecationWarning.
2. We will continue to support the existing behavior for at least one calendar
   year.
3. Following this period, the deprecated behavior and name will be removed or
   replaced in the next major (x.0) release. These releases take place in the
   Northern Solstice release each year.

Some examples:

If a feature gets deprecated during a major release like 1.0, it will need to
be deprecated for the next three releases: 1.1, 1.2, and 1.3. It could then be
removed in 2.0

Alternatively, if a feature is deprecated in 1.1, it will stay deprecated in
1.2, 1.3, and 2.0. This meets the deprecated for one year step, but we cannot
remove the feature in 2.1, 2.2, or 2.3. It would need to be removed in 3.0.

Regarding DeprecationWarnings
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

A :py:class:`~builtins.DeprecationWarning` is considered a minor change in ppb.
This means they can happen in any release where the minor version (The x in 1.x)
is changed.

We will do our best to include instructions in the warning on how to update your
code to avoid the DeprecationWarning going forward.
