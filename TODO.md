# TODO List

A project wide todo list for keeping note of changes that need to be made to
other parts of the project. Kept here to be available in the project and not 
tucked into working code.

## Priority

Tasks that need to happen ASAP. Generally broken systems. Also the next project
goal.

* Physics Engine
    * Collisions

## Other

General tasks. Includes ideas and reasoning for planned future development.

* Make a scene class that inherits from Publisher and includes a view. Intended 
to clean up parameters in the project.
    * Also the controller
* Formalize objects from zombies into ppb
    * Emitter
    * Particle
* Animation
* Instead of subclassing View, abstract the layering system like with 
    Controller.
* Style guide.
    * Setting
* Mouse
* Create event type that the publisher can listen for to automatically subscribe
  necessary callbacks when an object is created.