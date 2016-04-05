class Event(object):
    "A generic event."
    def __repr__(self):
        return "{}()".format(self.__class__.__name__)


class Tick(Event):
    """
    An event representing a loop through the system.
    """

    def __init__(self, sec=0, run_time=0):
        self.sec = sec
        self.run_time = run_time

    def __repr__(self):
        return "{}({}, {})".format(self.__class__.__name__,
                                   self.sec, self.run_time)


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


class Key(Event):
    """
    Events related to keys.
    """

    def __init__(self, identifier, name):
        """

        :param identifier: Key ID
        :param name: A human readable keyname.
        :return:
        """
        self.key = identifier
        self.name = name

    def __repr__(self):
        return '{}({}, "{}")'.format(self.__class__.__name__,
                                     self.key, self.name)


class KeyUp(Key):
    pass


class KeyDown(Key):
    pass


class MouseButtonUp(Key):
    pass


class MouseButtonDown(Key):
    pass


class Message(Event):
    """
    A generic event for sending messages between objects.
    """
    def __init__(self, sender, receiver, payload=None):
        """

        :param sender: object that sent the message
        :param receiver: object that should listen for the message
        :param payload: object expected by the receiver
        :return:
        """

        self.sender = sender
        self.receiver = receiver
        self.payload = payload

    def __repr__(self):
        return "{}({}, {}, {})".format(self.__class__.__name__,
                                       self.sender,
                                       self.receiver,
                                       self.payload)
