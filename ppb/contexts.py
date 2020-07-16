from dataclasses import dataclass
from typing import Any, Optional, Type

from ppb.flags import BlendMode, BlendModeBlend
from ppb.utils import Color



@dataclass
class RenderInfo:
    """
    A context class for holding information relevant to rendering.
    """
    #: The image asset.
    image: Any = ...
    #: The blend mode to use for opacity.
    blend_mode: Type[BlendMode] = BlendModeBlend  # This is apparently the appropriate way to type hint our flags?
    #:
    opacity: int = 255
    tint: Optional[Color] = None
