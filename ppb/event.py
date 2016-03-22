class Event(object):

    def __repr__(self):
        return "{}()".format(self.__class__.__name__)


class Tick(Event):
    """
    An event representing a loop through the system.
    """

    def __init__(self, sec=0):
        self.sec = sec

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.sec)


class Quit(Event):
    """
    An event calling for ending the program.
    """

    pass


class PushScene(Event):
    """
    Add a new scene to the stack.
    """

    def __init__(self, scene):
        self.scene = scene

    def __repr__(self):
        return "{}({})".format(self.__class__.__name__, self.scene)


class PopScene(Event):
    """
    Remove current scene from the stack.
    """

    pass


class ReplaceScene(PushScene):
    """
    Replace current scene on the stack.
    """

    pass
