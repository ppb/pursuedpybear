from .flags import Flag


class MouseButton(Flag, abstract=True):
    """
    A mouse button
    """


class Primary(MouseButton):
    """
    Primary mouse button (commonly left)
    """


class Secondary(MouseButton):
    """
    Secondary mouse button (commonly right)
    """


class Tertiary(MouseButton):
    """
    Third mouse button (commonly middle)
    """
