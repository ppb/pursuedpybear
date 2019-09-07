"""
The loadingscene feature provides base classes for loading screens.
:py:class:`BaseLoadingScene` and its children all work by listening to the asset
system and when all known assets are loaded, continuing on.
"""
import ppb


__all__ = 'BaseLoadingScene', 'ProgressBarLoadingScene'


class BaseLoadingScene(ppb.BaseScene):
    """
    Handles the basics of a loading screen.
    """
    #: The scene to transition to when loading is complete. May be a type or an instance.
    next_scene: "ppb.BaseScene"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._finished = False

        for s in self.get_progress_sprites():
            self.add(s, tags=['progress'])

        # Need this instantiated to maximize asset referencing coverage.
        if isinstance(self.next_scene, type):
            self.next_scene = self.next_scene()

        self.update_progress(0)

    def get_progress_sprites(self):
        """
        Initialize the sprites in the scene, yielding the ones that should be
        tagged with ``progress``.

        Override me.
        """
        yield from ()

    def on_asset_loaded(self, event, signal):
        # Ok, event.total_loaded should always be > 0, but we're being paranoid
        if event.total_loaded == event.total_queued == 0:
            progress = 0
        else:
            progress = event.total_loaded / (event.total_loaded + event.total_queued)
        self.update_progress(progress)

        # No more assets waiting to be loaded
        self._finished = bool(event.total_loaded and event.total_queued == 0)

    def on_idle(self, event, signal):
        if self._finished:
            signal(ppb.events.ReplaceScene(new_scene=self.next_scene))

    def update_progress(self, progress):
        """
        Updates the scene with the load progress (0->1).

        Override me.
        """


class ProgressBarLoadingScene(BaseLoadingScene):
    """
    Assumes that a simple left-to-right progress bar composed of individual
    sprites is used.

    Users should still override :py:meth:`get_progress_sprites()`.
    """
    #: Image to use for sprites in the "loaded" state (left side)
    loaded_image: "ppb.Image"
    #: Image to use for sprites in the "unloaded" state (right side)
    unloaded_image: "ppb.Image" = ppb.flags.DoNotRender

    def update_progress(self, progress):
        """
        Looks for sprites tagged ``progress`` and sets them to "loaded" or
        "unloaded" based on the progress.

        The "progress bar" is assumed to be horizontal going from left to right.
        """
        bar = sorted(self.get(tag='progress'), key=lambda s: s.position.x)

        progress_index = progress * len(bar)

        for i, sprite in enumerate(bar):
            if i <= progress_index:
                sprite.image = self.loaded_image
            else:
                sprite.image = self.unloaded_image
