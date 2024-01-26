"""
A system for two phase updates: Update, and Commit.
"""
from dataclasses import dataclass
from ppb.systemslib import System

__all__ = 'Commit',


@dataclass
class Commit:
    """
    Fired after Update.
    """


class TwoPhaseSystem(System):
    """
    Produces the Commit event.
    """

    def on_update(self, event, signal):
        signal(Commit())


class TwoPhaseMixin:
    """
    Mixin to apply to objects to handle two phase updates.
    """

    __staged_changes = None

    def stage_changes(self, **kwargs):
        """
        Stage changes for the next commit.

        These are just properties on the current object to update.
        """
        if self.__staged_changes is None:
            self.__staged_changes = {}
        self.__staged_changes.update(kwargs)

    def on_commit(self, event, signal):
        """
        Commit changes previously staged.
        """
        changes, self.__staged_changes = self.__staged_changes, {}
        if changes:
            for name, value in changes.items():
                setattr(self, name, value)
