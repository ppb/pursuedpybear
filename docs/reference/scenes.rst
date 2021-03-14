.. py:currentmodule:: ppb.scenes

================
All About Scenes
================

Scenes are the terrain where sprites act. Each game has multiple scenes and may
transition at any time.

.. autoclass:: ppb.Scene
    :members:
    :exclude-members: container_class

    .. autoattribute:: background_color
       
       An RGB triple of the background, eg ``(0, 127, 255)``

    .. autoattribute:: main_camera
       
       An object representing the view of the scene that's rendered

