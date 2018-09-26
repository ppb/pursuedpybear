import logging


class LoggingMixin:
    """
    A simple mixin to provide a `logger` attribute to instances, based on their
    fully qualified name.
    """
    _logger = None

    @property
    def logger(self):
        if self._logger is None:
            fqn = f"{self.__class__.__module__}.{self.__class__.__qualname__}"
            self._logger = logging.getLogger(fqn)
        return self._logger
    