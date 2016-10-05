# PPB Release Roadmap

World Maker Faire is a place where people who make get together and show off
and learn. It's a great place to really show off the goals of this project.
So with that, I've decided I am going to have a proper 1.0 release by World
Maker Faire 2017.

## Functioning Engine

This means I've built at least one game, preferably a handful of samples
using the engine and all it's release features. With that in mind: Event
driven top down games are going to be my primary focus. With time, I'll work
on adding side scrolling as well.

### Event System

There's already a functional event system in place, but I have some ideas for
improvement. The idea of an event is going to be abstracted further, and the
maps for the `Publisher` will change accordingly.

### Hardware Wrappers

I'm unhappy with the current implementation. It's too fragile and makes 
testing and building new wrappers unpleasant. In it's place, I'd like a lib
that produces a `Hardware` object based on provided inputs.

### Behavior Trees

They need to be there, and I think they're one of the keys to the whole system
working better.

## Editor

To really make this a teaching tool, it's going to require a visual editor.
Because this is Python and I can do it, I'd like to make the editor using the 
engine. As such, it's going to be built in in conjunction to the engine itself.

### Object editor

This is fairly critical: An easy visual way to create game objects. Also 
managing inside a particular scene.

#### Behavior Management

This will likely be important. Should include a code editor built into the 
system.

### Scene management

The primary workflow should give an idea of how scenes are being used.

Introduce a concept of a sub-scene (outside the context of code)

## Packagine System

This is the nice to have, but I'd like to make it possible for a person to 
build the entire game via the visual editor and output functional python that
can be run as-is. Bonus if it handles dependency checking.