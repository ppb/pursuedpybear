Passing keyword arguments as configuration flags
===========================================================

Using run function and configuration examples. You can pass extra data
to the keyword arguments of the run function and these get passed automatically 
to the engine and the systems. 

Code sample (resolution)

.. code-block::
   :linenos:
   
   import ppb

   RESOLUTION = (1200, 900)

   ppb.run(resolution=RESOLUTION, difficulty_level=10)
