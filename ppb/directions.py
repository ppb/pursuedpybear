"""
The ordinal directions.

A collection of normalized vectors to be referenced by name.

Best used for the positions or facings of :class:`Sprites <ppb.Sprite>`.
"""
from ppb_vector import Vector

UP = Vector(0, 1).normalize()  #: Unit vector to the top of the screen from center.
DOWN = Vector(0, -1).normalize()  #: Unit vector to the bottom of the screen from center.
LEFT = Vector(-1, 0).normalize()  #: Unit vector to the left of the screen from center.
RIGHT = Vector(1, 0).normalize()  #: Unit vector to the right of the screen from center.
UP_AND_LEFT = (UP + LEFT).normalize()  #: Unit vector diagonally up and to the left of the screen from center.
UP_AND_RIGHT = (UP + RIGHT).normalize()  #: Unit vector diagonally up and to the right of the screen from center.
DOWN_AND_LEFT = (DOWN + LEFT).normalize()  #: Unit vector diagonally down and to the left of the screen from center.
DOWN_AND_RIGHT = (DOWN + RIGHT).normalize()  #: Unit vector diagonally down and to the right of the screen from center.
