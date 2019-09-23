=============
Sound Effects
=============

Sound effects can be triggered by sending an event:

.. code-block:: python

    def on_button_pressed(self, event, signal):
        signal(PlaySound(sound=ppb.Sound('toot.ogg')))

Both Ogg/Vorbis and WAV are supported audio formats.

.. note::
    As is usual with assets, you should instantiate your :py:class:`ppb.Sound`
    as soon as possible, such as at the class level.

.. note::
    PyGame has fairly limited codec support. "Complex WAVE files" are not
    supported. Ogg/Opus appears to be unsupported. Additional formats and codecs
    might be supported but undocumented.

Reference
---------
.. autoclass:: ppb.events.PlaySound
   :members:

.. autoclass:: ppb.Sound
   
   The asset to use for sounds. WAV and Ogg/Vorbis are supported.
