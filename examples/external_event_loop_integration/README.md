# External Event Loop Integration

This example demonstrates embedding ppb in an external event loop, in this
case Twisted.

In order to run this example, you'll need to install the requirements.txt in
this directory. Otherwise, it's behavior is similar to the
keyboard_and_mouse_controls example:

A space ship in the center of the screen facing down can be controlled with
the arrows or "WASD". You can fire a laser beam with your primary mouse button
or the space bar.

When a laser hits one of the enemy ships (round), the laser and the ship are
removed from play.

Additionally, if you navigate to localhost:8080 in your browser, you will see
the number of enemies still in play. This is the demonstration of interaction
between ppb and a webserver.
