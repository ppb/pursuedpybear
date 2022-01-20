import ctypes
import io
import logging
import time

from sdl2 import (
    AUDIO_S16SYS, rw_from_object,
)

from sdl2.sdlmixer import (
    # Errors, https://www.libsdl.org/projects/SDL_mixer/docs/SDL_mixer_7.html#SEC7
    Mix_GetError,
    # Support library loading https://www.libsdl.org/projects/SDL_mixer/docs/SDL_mixer_7.html#SEC7
    Mix_Init, Mix_Quit, MIX_INIT_FLAC, MIX_INIT_MOD, MIX_INIT_MP3, MIX_INIT_OGG,
    # Mixer init https://www.libsdl.org/projects/SDL_mixer/docs/SDL_mixer_7.html#SEC7
    Mix_OpenAudio, Mix_CloseAudio, Mix_QuerySpec,
    # Samples https://www.libsdl.org/projects/SDL_mixer/docs/SDL_mixer_16.html#SEC16
    Mix_LoadWAV_RW, Mix_FreeChunk, Mix_VolumeChunk,
    # Channels https://www.libsdl.org/projects/SDL_mixer/docs/SDL_mixer_25.html#SEC25
    Mix_AllocateChannels, Mix_PlayChannel, Mix_ChannelFinished, channel_finished,
    # Other
    MIX_MAX_VOLUME,
)

from ppb import assetlib
from ppb.systems.sdl_utils import SdlSubSystem, mix_call, SdlMixerError
from ppb.utils import LoggingMixin

__all__ = ('SoundController', 'Sound')

logger = logging.getLogger(__name__)


def query_spec():
    """
    Helpful wrapper around Mix_QuerySpec()
    """
    frequency = ctypes.c_int()
    format = ctypes.c_uint16()
    channels = ctypes.c_int()
    count = mix_call(
        Mix_QuerySpec,
        ctypes.byref(frequency),
        ctypes.byref(format),
        ctypes.byref(channels),
        _check_error=lambda rv: rv == 0 and Mix_GetError(),
    )
    return count, frequency, format, channels


class Sound(assetlib.Asset):
    # This is wrapping a ctypes.POINTER(Mix_Chunk)

    def background_parse(self, data):
        # Band-aid over some synchronization issues
        # https://github.com/ppb/pursuedpybear/issues/619
        while not any(query_spec()):
            time.sleep(0)
        file = rw_from_object(io.BytesIO(data))
        # ^^^^ is a pure-python emulation, does not need cleanup.
        return mix_call(
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
        return mix_call(Mix_VolumeChunk, self.load(), -1) / MIX_MAX_VOLUME

    @volume.setter
    def volume(self, value):
        mix_call(Mix_VolumeChunk, self.load(), int(value * MIX_MAX_VOLUME))


@channel_finished
def _filler_channel_finished(channel):
    pass


class SoundController(SdlSubSystem, LoggingMixin):
    _finished_callback = None

    def __init__(self, **kw):
        super().__init__(**kw)
        self._currently_playing = {}  # Track sound assets so they don't get freed early

    @property
    def allocated_channels(self):
        """
        The number of channels currently allocated by SDL_mixer.

        Seems to default to 8.
        """
        return mix_call(Mix_AllocateChannels, -1)

    @allocated_channels.setter
    def allocated_channels(self, value):
        mix_call(Mix_AllocateChannels, value)

    def __enter__(self):
        super().__enter__()
        mix_call(
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
        mix_call(Mix_Init, MIX_INIT_FLAC | MIX_INIT_MOD | MIX_INIT_MP3 | MIX_INIT_OGG)

        logger.debug("SoundController")
        logger.debug(query_spec())

        self.allocated_channels = 16

        # Register callback, keeping reference for later cleanup
        self._finished_callback = channel_finished(self._on_channel_finished)
        mix_call(Mix_ChannelFinished, self._finished_callback)

    def __exit__(self, *exc):
        # Unregister callback and release reference
        mix_call(Mix_ChannelFinished, _filler_channel_finished)
        self._finished_callback = None
        # Cleanup SDL_mixer
        mix_call(Mix_CloseAudio)
        mix_call(Mix_Quit)
        super().__exit__(*exc)

    def on_play_sound(self, event, signal):
        sound = event.sound
        chunk = event.sound.load()

        try:
            channel = mix_call(
                Mix_PlayChannel,
                -1,  # Auto-pick channel
                chunk,
                0,  # Do not repeat
                _check_error=lambda rv: rv == -1
            )
        except SdlMixerError as e:
            if not str(e).endswith("No free channels available"):
                raise
            self.logger.warn("Attempted to play sound, but there were no available channels.")
        else:
            self._currently_playing[channel] = sound  # Keep reference of playing asset

    def _on_channel_finished(self, channel_num):
        # "NEVER call SDL_Mixer functions, nor SDL_LockAudio, from a callback function."
        self._currently_playing[channel_num] = None  # Release the asset that was playing
