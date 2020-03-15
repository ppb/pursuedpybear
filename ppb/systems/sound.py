import io

from sdl2 import (
    AUDIO_S16SYS, rw_from_object,
)

from sdl2.sdlmixer import (
    # Errors
    Mix_GetError, Mix_SetError,
    # Support library loading
    Mix_Init, Mix_Quit, MIX_INIT_FLAC, MIX_INIT_MOD, MIX_INIT_MP3, MIX_INIT_OGG,
    # Mixer init
    Mix_OpenAudio, Mix_CloseAudio,
    # Samples
    Mix_LoadWAV_RW, Mix_FreeChunk, Mix_VolumeChunk,
    # Channels
    Mix_AllocateChannels, Mix_PlayChannel, Mix_ChannelFinished, channel_finished,
    # Other
    MIX_MAX_VOLUME,
)

from ppb.systemslib import System
from ppb import assetlib

__all__ = ('SoundController', 'Sound', 'SdlMixerError')


class SdlMixerError(Exception):
    """
    SDL_mixer raised an error
    """


def _call(func, *pargs, _check_error=None, **kwargs):
    """
    Wrapper for calling SDL_mixer functions for handling errors.

    If _check_error is given, called with the return value to check for errors.
    If _check_error returns truthy, an error occurred.

    If _check_error is not given, it is assumed that a non-empty error from
    Mix_GetError indicates error.
    """
    Mix_SetError(b"")
    rv = func(*pargs, **kwargs)
    err = Mix_GetError()
    if (_check_error(rv) if _check_error else err):
        raise SdlMixerError(f"Error calling {func.__name__}: {err.decode('utf-8')}")
    else:
        return rv


class Sound(assetlib.Asset):
    # This is wrapping a ctypes.POINTER(Mix_Chunk)

    def background_parse(self, data):
        file = rw_from_object(io.BytesIO(data))
        # ^^^^ is a pure-python emulation, does not need cleanup.
        return _call(
            Mix_LoadWAV_RW, file, False,
            _check_error=lambda rv: not rv
        )

    def free(self, object, _Mix_FreeChunk=Mix_FreeChunk):
        # ^^^ is a way to keep required functions during interpreter cleanup

        # "It's a bad idea to free a chunk that is still being played..."
        # This should only be called when all references are dropped.
        # (This means that SoundController needs to keep a reference while playing.)
        if object:  # Check that the pointer isn't null
            _Mix_FreeChunk(object)  # Can't fail
            # object.contents = None
            # Can't actually nullify the pointer. Good thing this is __del__.

    @property
    def volume(self):
        """
        The volume setting of this chunk, from 0.0 to 1.0
        """
        return _call(Mix_VolumeChunk, self.load(), -1) / MIX_MAX_VOLUME

    @volume.setter
    def volume(self, value):
        _call(Mix_VolumeChunk, self.load(), value * MIX_MAX_VOLUME)


@channel_finished
def _filler_channel_finished(channel):
    pass


class SoundController(System):
    _finished_callback = None

    def __init__(self, **kw):
        super().__init__(**kw)
        self.channels = {}  # Track sound assets so they don't get freed early

    def __enter__(self):
        _call(Mix_Init, MIX_INIT_FLAC | MIX_INIT_MOD | MIX_INIT_MP3 | MIX_INIT_OGG)
        _call(
            Mix_OpenAudio,
            44100,  # Sample frequency, 44.1 kHz is CD quality
            AUDIO_S16SYS,  # Audio, 16-bit, system byte order. IDK is signed makes a difference
            2,  # Number of output channels, 2=stereo
            4096,  # Chunk size. TBH, this is a magic knob number.
            # ^^^^ Smaller is more CPU, larger is less responsive.
            # A lot of the performance-related recommendations are so dated I'm
            # not sure how much difference it makes.
            _check_error=lambda rv: rv == -1
        )

        _call(Mix_AllocateChannels, 16)  # TODO: Do something more interesting

        # Register callback, keeping reference for later cleanup
        self._finished_callback = channel_finished(self._on_channel_finished)
        _call(Mix_ChannelFinished, self._finished_callback)

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Unregister callback and release reference
        _call(Mix_ChannelFinished, _filler_channel_finished)
        self._finished_callback = None
        # Cleanup SDL_mixer
        _call(Mix_CloseAudio)
        _call(Mix_Quit)

    def on_play_sound(self, event, signal):
        sound = event.sound
        chunk = event.sound.load()

        channel = _call(
            Mix_PlayChannel,
            -1,  # Auto-pick channel
            chunk,
            0,  # Do not repeat
            _check_error=lambda rv: rv == -1
        )
        self.channels[channel] = sound  # Keep reference of playing asset

    def _on_channel_finished(self, channel_num):
        # "NEVER call SDL_Mixer functions, nor SDL_LockAudio, from a callback function."
        self.channels[channel_num] = None  # Release the asset that was playing
