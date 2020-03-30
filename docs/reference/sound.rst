=============
Sound Effects
=============

Sound effects can be triggered by sending an event:

.. code-block:: python

    def on_button_pressed(self, event, signal):
        signal(PlaySound(sound=ppb.Sound('toot.ogg')))

The following sound formats are supported:
* Wave
* AIFF
* VOC
* MOD
* MIDI
* OGG (with both Vorbis and Opus)
* MP3
* FLAC

Additionally, MIDI _may_ be supported.

.. note::
    As is usual with assets, you should instantiate your :py:class:`ppb.Sound`
    as soon as possible, such as at the class level.

Reference
---------
.. autoclass:: ppb.events.PlaySound
   :members:

.. autoclass:: ppb.Sound
   
   The asset to use for sounds. WAV and Ogg/Vorbis are supported.
