.. py:module:: ppb.assets

Assets
======

PursuedPyBear features a background, eager-loading asset system. The first time
an asset is referenced, PPB starts reading and parsing it in a background
thread.

The data is kept in memory for the lifetime of the :py:class:`Asset`. When
nothing is referencing it any more, the Python garbage collector will clean up
the object and its data.

:py:class:`Asset` instances are consolidated or "interned": if you ask for the
same asset twice, you'll get the same instance back. Note that this is a
performance optimization and should not be relied upon (do not do things like 
``asset1 is asset2``).


General Asset Interface
-----------------------

All assets inherit from :py:class:`Asset`. It handles the background loading
system and the data logistics.

.. autoclass:: ppb.assetlib.Asset
    :members:

    .. method:: file_missing()

        Called if the file could not be found, to produce a default value.

        Subclasses may want to define this.

        Called in the background thread.

    .. automethod:: free()

    .. automethod:: load(timeout: float = None)

    .. automethod:: is_loaded()



Subclassing
~~~~~~~~~~~

:py:class:`Asset` makes specific assumptions and is only suitable for loading
file-based assets. These make the consolidation, background-loading, and other
aspects of :py:class:`Asset` possible.

You should really only implement three methods:

* :py:meth:`background_parse()`: This is called with the loaded data and returns
  an object constructed from that data. This is called from a background thread
  and its return value is accessible from :py:meth:`load()`

  This is an excellent place for decompression, data parsing, and other tasks
  needed to turn a pile of bytes into a useful data structure.

* :py:meth:`file_missing()`: This is called if the asset is not found. Defining
  this method suppresses :py:meth:`load()` from raising a
  :py:exc:`FileNotFoundError` and will instead call this, and
  :py:meth:`load()` will return what this returns.

  For example, :py:class:`ppb.Image` uses this to produce the default square.

* :py:meth:`free()`: This is to clean up any resources that would not normally
  be cleaned up by Python's garbage collector. If you are integrating external
  libraries, you may need this.


Concrete Assets
---------------

While :py:class:`Asset` can load anything, it only produces bytes, limiting its
usefulness. Most likely, you want a concrete subclass that does something more
useful.

.. autoclass:: ppb.Image

    Loads an image file and parses it into a form usable by the renderer.

.. autoclass:: ppb.Sound
    :noindex:

    Loads and decodes an image file. A variety of formats are supported.



Asset Proxies and Virtual Assets
--------------------------------

Asset Proxies and Virtual Assets are assets that implement the interface but
either delegate to other Assets or are completely synthesized.

For example, :py:class:`ppb.features.animation.Animation` is an asset proxy that
delegates to actual :py:class:`ppb.Image` instances.

.. autoclass:: ppb.assetlib.AbstractAsset
    :members:

.. autoclass:: ppb.Rectangle


.. autoclass:: ppb.Ellipse


.. autoclass:: ppb.Triangle


.. autoclass:: ppb.Circle


.. autoclass:: ppb.Square
