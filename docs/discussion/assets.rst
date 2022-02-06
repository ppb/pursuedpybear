.. py:currentmodule:: ppb.assetlib

The Asset System
================

The asset system (:py:mod:`ppb.assetlib`) is probably one of the more involved parts of the PPB engine, most likely because it is one of the very few places where multithreading takes place.

It was made to help give a handle on the problems surrounding loading data into games and the management of said data.

To that end, we had several goals when we built the asset system:

* Allow declaring resources at a fairly abstract level
* Optimistically load resources in the background as soon as possible
* Provide a layer of abstraction between how data is loaded and the use of that data

As part of this, we also built the VFS library (:py:mod:`ppb.vfs`), which treats the Python module import system as a filesystem and allows loading data from it, to make it clear where and how resource files should be added to a project, and provide all the flexibility of the Python module system.


Concepts
--------

Out of this, we define a few high-level concepts:

* Asset: Some kind of way data is loaded & parsed. Usually the result is some internal engine data type.
* Real or File Asset: Loads data from the VFS (such as :py:class:`ppb.Image`)
* Virtual Asset: Synthesizes data from nothing (such as :py:class:`ppb.Ellipse`)
* Proxy Asset: Wraps other asset types (such as :py:class:`ppb.features.animation.Animation`)

The idea is that the place where the asset is used does not care what kind of asset is used, only that it produces the right kind of data--nothing in the world can make the renderer accept a :py:class:`ppb.Sound`.


Implementation
--------------

So how did we do this?

A lot of the heavy lifting is provided by the :py:mod:`concurrent.futures` package from the standard library. On top of this, :py:class:`AssetLoadingSystem` and :py:class:`Asset` cooperate to implement background file reading. After the data is read, it is handed to the instance and processed into its final form.

Effort is taken to deduplicate assets: If two places refer to the same asset, it is normalized to the same instance. This reduces both load times and memory usage.

A minor wrinkle in this is that assets are defined before the engine starts. The asset system does not actually begin loading data until the engine and :py:class:`AssetLoadingSystem` are initialized. This means that there's no problems delivering events and asset implementations know that initialization has happened.


Usage
-----

None of this explains how you use the asset system for yourself.

Defining Assets
~~~~~~~~~~~~~~~

First of all, you have to define for yourself what kind of data the asset will produce. This is usually some kind of data object to be consumed.

Then, you make an :py:class:`Asset` subclass. There's a few methods of note for overriding:

* :py:meth:`Asset.background_parse()`: Do the actual parsing. Accepts the bytes loaded from the file, and returns the data object that the asset is wrapping.
* :py:meth:`Asset.file_missing()`: If defined, this will be called if the file is not found, and is expected to return a synthesized stand-in object. If not defined, :py:meth:`Asset.load()` will raise an error.
* :py:meth:`Asset.free()`: Handles cleanup in the case where resources need to be explicitly cleaned. Note that because this is called in the context of :py:meth:`__del__() <object.__del__>`, care must be taken around referring to globals or other modules.

At the point of use, all you need to do is call :py:meth:`Asset.load()` and you will get the object created by the asset. This will block if the background processing is incomplete.

Proxy Assets
~~~~~~~~~~~~

Proxy assets are simply assets that wrap other, more concrete assets. One example of this is :py:mod:`ppb.features.animation`, where :py:class:`Animation <ppb.features.animation>` wraps multiple :py:class:`Image <ppb.Image>` instances.

Writing your own proxy asset just means returning the results of your inner asset's :py:meth:`Asset.load()` from your own.
