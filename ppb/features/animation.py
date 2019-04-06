"""
A system for producing animated sprites.

Only supports frame-by-frame, not gif, apng, or full motion video.
"""
import time
import re

FILE_PATTERN = re.compile(r'\{(\d+)\.\.(\d+)\}')


class Animation:
    """
    An "image" that actually rotates through numbered files at the specified rate.
    """
    clock = time.monotonic

    def __init__(self, filename, frames_per_second):
        self._filename = filename
        self.frames_per_second = frames_per_second

        self._paused_frame = None
        self._pause_level = 0
        self._frames = []

        self._offset = -self._clock()
        self._compile_filename()

    def _clock(self):
        return type(self).clock()

    def _compile_filename(self):
        match = FILE_PATTERN.search(self._filename)
        start, end = match.groups()
        numdigits = min(len(start), len(end))
        start = int(start)
        end = int(end)
        template = FILE_PATTERN.sub(
            '{:0%dd}' % numdigits,
            self._filename,
        )
        self._frames = [
            template.format(n)
            for n in range(start, end + 1)
        ]

    def pause(self):
        if not self._pause_level:
            self._paused_time = self._clock()
            self._paused_frame = self.current_frame
        self._pause_level += 1

    def unpause(self):
        self._pause_level -= 1
        if not self._pause_level:
            self._offset = self._paused_time - self._clock()

    def _current_frame(self, time):
        if not self._pause_level:
            return (
                int((time + self._offset) * self.frames_per_second)
                % len(self._frames)
            )
        else:
            return self._paused_frame

    @property
    def current_frame(self):
        if not self._pause_level:
            return (
                int((self._clock() + self._offset) * self.frames_per_second)
                % len(self._frames)
            )
        else:
            return self._paused_frame

    def __str__(self):
        return self._frames[self.current_frame]
