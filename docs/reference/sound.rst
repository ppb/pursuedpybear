=============
Sound Effects
=============

Sound effects can be triggered by sending an event:

.. code-block:: python

    def on_button_pressed(self, event, signal):
        signal(PlaySound(sound=ppb.Sound('toot.ogg')))

The following sound formats are supported:

* `OGG <https://en.wikipedia.org/wiki/Ogg>`_ (with both `Vorbis <https://en.wikipedia.org/wiki/Vorbis>`_ and `Opus <https://en.wikipedia.org/wiki/Opus_(audio_format)>`_)
* `FLAC <https://en.wikipedia.org/wiki/FLAC>`_
* `MP3 <https://en.wikipedia.org/wiki/MP3>`_
* `WAV <https://en.wikipedia.org/wiki/WAV>`_
* `AIFF <https://en.wikipedia.org/wiki/Audio_Interchange_File_Format>`_
* `MOD <https://en.wikipedia.org/wiki/MOD_(file_format)>`_
* VOC

Additionally, MIDI *may* be supported.

.. note::
    As is usual with assets, you should instantiate your :py:class:`ppb.Sound`
    as soon as possible, such as at the class level.

Reference
---------
.. autoclass:: ppb.events.PlaySound
   :members:
   :noindex:

.. autoclass:: ppb.Sound
   
   The asset to use for sounds. A variety of file formats are supported.
