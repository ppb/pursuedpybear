.. py:currentmodule:: ppb.camera

Camera
=============

.. automodule:: ppb.camera


.. autoclass:: Camera
   :members:


.. warning::
   Setting the game unit dimensions of a camera (whether via
   :attr:`Camera.width`, :attr:`Camera.height`, or the
   ``target_game_unit_width`` of the :class:`Camera` constructor) will
   affect both :attr:`Camera.width` and :attr:`Camera.height`. Their ratio
   is determined by the defined window.