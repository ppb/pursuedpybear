==================
Starting Your Game
==================

There are two major patterns for starting a game

.. code-block:: python

    import ppb

    def setup(scene):
        ...
   
    ppb.run(setup=setup)


.. code-block:: python

   import ppb

   class MyScene(ppb.BaseScene):
       ...
   
   ppb.run(starting_scene=MyScene)
