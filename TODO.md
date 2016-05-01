# TODO List

A project wide todo list for keeping note of changes that need to be made to
other parts of the project. Kept here to be available in the project and not 
tucked into working code.

## Priority

Tasks that need to happen ASAP. Generally broken systems. Also the next project
goal.

* Abstract Hardware using the hardware package to defer function calls. 
    * This should allow differing input systems to be translated on a per
      library basis.

## Other

General tasks. Includes ideas and reasoning for planned future development.

* Because objects no longer need to know about the view, abstract input 
  into the hardware library.
* Animation
* Instead of subclassing View, abstract the layering system like with 
    Controller.
* Style guide.
* Improve logging