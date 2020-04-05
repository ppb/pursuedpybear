The Asset System
================

The asset system (:py:mod:`ppb.assetlib`) is probably one of the more involved parts of the PPB engine, most likely because it is one of the very few places where multithreading takes place.

It was made to help give a handle on the problems surrounding loading data into games and the management of said data.

To that end, we had several goals when we built the asset system:

* Allow declaring resources at a fairly abstract level
* Optimistically load resources in the background as soon as possible
* Provide a barrier of abstraction between how data is loaded and the use of that data

As part of this, we also built the VFS library (:py:mod:`ppb.vfs`), which treats the Python module import system as a filesystem and allows loading data from it, to make it clear where and how resource files should be added to a project, and provide all the flexibility of the Python module system.


Concepts
--------

Our of this, we define a few high-level concepts:

* Asset: Some kind of way data is loaded & parsed. Usually the result is some internal engine data type.
* Real or File Asset: Loads data from the VFS (such as :py:class:`ppb.Image`)
* Virtual Asset: Synthesizes data from nothing (such as :py:class:`ppb.assets.Circle`)
* Proxy Asset: Wraps other asset types (such as :py:class:`ppb.features.animation.Animation`)

The idea is that the place where the asset is used does not care what kind of asset is used, only that it produces the right kind of data--nothing in the world can make the renderer accept a :py:class:`ppb.Sound`.