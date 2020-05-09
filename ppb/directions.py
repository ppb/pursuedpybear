"""
The ordinal directions.

A collection of normalized vectors to be referenced by name.

Best used for the positions or facings of :class:`Sprites <ppb.Sprite>`.
"""
from ppb_vector import Vector

Up = Vector(0, 1).normalize()  #: Unit vector to the top of the screen from center.
Down = Vector(0, -1).normalize()  #: Unit vector to the bottom of the screen from center.
Left = Vector(-1, 0).normalize()  #: Unit vector to the left of the screen from center.
Right = Vector(1, 0).normalize()  #: Unit vector to the right of the screen from center.
UpAndLeft = (Up + Left).normalize()  #: Unit vector diagonally up and to the left of the screen from center.
UpAndRight = (Up + Right).normalize()  #: Unit vector diagonally up and to the right of the screen from center.
DownAndLeft = (Down + Left).normalize()  #: Unit vector diagonally down and to the left of the screen from center.
DownAndRight = (Down + Right).normalize()  #: Unit vector diagonally down and to the right of the screen from center.
