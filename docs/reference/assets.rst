.. py:currentmodule:: ppb.assets

Assets
======

PursuedPyBear features a background, eager-loading asset system. The first time
an asset is referenced, PPB starts reading and parsing it in a background
thread.

The data is kept in memory for the lifetime of the :py:class:`Asset`. When
nothing is referencing it any more, the Python garbage collector will clean up
the object and its data.


General Asset Interface
-----------------------

All assets inherit from :py:class:`Asset`. It handles the background loading
system and the data logistics.

.. autoclass:: ppb.assets.Asset
    :members:

    .. method:: file_missing()

        Called if the file could not be found, to produce a default value.

        Subclasses may want to define this.

        Called in the background thread.


Concrete Assets
---------------

While :py:class:`Asset` can load anything, it only produces bytes, limiting its
usefulness. Most likely, you want a concrete subclass that does something more
useful.

.. autoclass:: ppb.Image

    Loads an image file and parses it into a form usable by the renderer.

.. autoclass:: ppb.Sound

    Loads and decodes an image file. Wave and Ogg Vorbis are supported.



Asset Proxies
-------------

Asset Proxies are virtual assets that implement the interface but either
delegate to other Assets or are completely virtual, such as
:py:class:`ppb.features.animation.Animation`.

.. class:: Asset Proxy

    .. method:: load()

        Gets the parsed data from wherever this proxy gets its data.
