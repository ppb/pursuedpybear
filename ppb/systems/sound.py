import io

from sdl2 import (
    AUDIO_S16SYS, rw_from_object,
)

from sdl2.sdlmixer import (
    # Support library loading https://www.libsdl.org/projects/SDL_mixer/docs/SDL_mixer_7.html#SEC7
    Mix_Init, Mix_Quit, MIX_INIT_FLAC, MIX_INIT_MOD, MIX_INIT_MP3, MIX_INIT_OGG,
    # Mixer init https://www.libsdl.org/projects/SDL_mixer/docs/SDL_mixer_7.html#SEC7
    Mix_OpenAudio, Mix_CloseAudio,
    # Samples https://www.libsdl.org/projects/SDL_mixer/docs/SDL_mixer_16.html#SEC16
    Mix_LoadWAV_RW, Mix_FreeChunk, Mix_VolumeChunk,
    # Channels https://www.libsdl.org/projects/SDL_mixer/docs/SDL_mixer_25.html#SEC25
    Mix_AllocateChannels, Mix_PlayChannel, Mix_ChannelFinished, channel_finished,
    Mix_Volume, Mix_HaltChannel, Mix_Pause, Mix_Resume,
    # Other
    MIX_MAX_VOLUME,
)

from ppb import assetlib
from ppb.gomlib import GameObject
from ppb.systems.sdl_utils import SdlSubSystem, mix_call, SdlMixerError
from ppb.utils import LoggingMixin

__all__ = ('SoundController', 'Sound', 'SoundManager')


class Sound(assetlib.Asset):
    # This is wrapping a ctypes.POINTER(Mix_Chunk)

    def background_parse(self, data):
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


class SoundManager(GameObject):
    """
    Allows dynamic manipulation of a sound
    """
    __channel = None

    def _set_channel(self, channel_num):
        """
        Called by SoundController to give the manager the SDL mixer channel
        number, or None if this manager is no longer managing a channel
        """
        if channel_num is None:
            del self.__channel
        else:
            self.__channel = channel_num

    @property
    def volume(self):
        """
        How load to play the sound, from 0 to 1
        """
        if self.__channel is not None:
            raw_value = mix_call(Mix_Volume, self.__channel, -1)
            return raw_value / MIX_MAX_VOLUME

    @volume.setter
    def volume(self, value):
        if self.__channel is not None:
            raw_value = int(value * MIX_MAX_VOLUME)
            mix_call(Mix_Volume, self.__channel, raw_value)

    def stop(self):
        """
        Stop playback completely, as if the sound had ended.

        Does nothing if already stopped.
        """
        if self.__channel is not None:
            mix_call(Mix_HaltChannel, self.__channel)

    def pause(self):
        """
        Pause playback to be continued later.

        If already paused, does nothing.
        """
        if self.__channel is not None:
            mix_call(Mix_Pause, self.__channel)

    def resume(self):
        """
        Continue playback.

        If already playing, does nothing.
        """
        if self.__channel is not None:
            mix_call(Mix_Pause, self.__channel)

    def on_finished(self, event, signal):
        """
        Called when this sound has finished playing. The event is empty.

        Override me.
        """


class Finished:
    """
    An empty event bag
    """


class SoundController(SdlSubSystem, LoggingMixin):
    _finished_callback = None

    def __init__(self, **kw):
        super().__init__(**kw)
        self._currently_playing = {}  # Track sound assets so they don't get freed early
        self._managers = {}  # The managers for the various tracks
        self._managers_to_evict = []  # Keeps managers around

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
            AUDIO_S16SYS,  # Audio, 16-bit, system byte order. IDK if signed makes a difference
            2,  # Number of output channels, 2=stereo
            4096,  # Chunk size. TBH, this is a magic knob number.
            # ^^^^ Smaller is more CPU, larger is less responsive.
            # A lot of the performance-related recommendations are so dated I'm
            # not sure how much difference it makes.
            _check_error=lambda rv: rv == -1
        )
        mix_call(Mix_Init, MIX_INIT_FLAC | MIX_INIT_MOD | MIX_INIT_MP3 | MIX_INIT_OGG)
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
        manager = event.manager

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
            self._managers[channel] = manager
            self.children.add(manager)
            if manager is not None:
                manager._set_channel(channel)

    def _on_channel_finished(self, channel_num):
        # "NEVER call SDL_Mixer functions, nor SDL_LockAudio, from a callback function."
        self._currently_playing[channel_num] = None  # Release the asset that was playing
        if self._managers[channel_num]:
            manager = self._managers[channel_num]
            if manager is not None:
                manager._set_channel(None)
            self._managers[channel_num] = None
            self._managers_to_evict.append(manager)
            self.children.remove(manager)
            self.engine.signal(Finished(), targets=[manager])

    def on_idle(self, event, signal):
        # Any previously triggered Finished events should have been dispatched,
        # so we're free to discard these managers
        if self._managers_to_evict:
            self._managers_to_evict = []
            # Well, that was easy
