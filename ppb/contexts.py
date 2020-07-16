from dataclasses import dataclass
from typing import Optional, Type, Union

from ppb.flags import BlendMode, BlendModeBlend
from ppb.assets import Shape
from ppb.systems.renderer import Image
from ppb.utils import Color


KnownImages = Union[Ellipsis, Shape, Image]

@dataclass
class RenderInfo:
    """
    A context class for holding information relevant to rendering.
    """
    #: The image asset.
    image: Optional[KnownImages] = None
    #: The blend mode to use for opacity.
    blend_mode: Type[BlendMode] = BlendModeBlend  # This is apparently the appropriate way to type hint our flags?
    #:
    opacity: int = 255
    color: Optional[Color] = None
