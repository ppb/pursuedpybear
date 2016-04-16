import logging

import ppb.engine as engine
from ppb.event import Tick, ObjectCreated
from ppb.vmath import Vector2 as Vec


class Controller(object):
    """
    A basic controller interface.

    Requires a hardware middleware that provides access to a keys, mouse, and
    events function.
    """

    def __init__(self, scene, hardware):
        """
        Attributes: keys: A dictionary of the hardware keys
                    mouse: An object definition of a mouse

        :param scene: Publisher
        :param hardware: An object with a keys, mouse and events functions.
                         keys should return a dictionary of the key state.
                         mouse should return an object representation of the
                             mouse.
                         events should return hardware events translated into
                             ppb events.
        :return:
        """
        self.keys = hardware.keys()
        self.mouse = hardware.mouse()
        self.hardware = hardware
        engine.message(ObjectCreated(self, ((Tick, self.tick),)))

    def __getitem__(self, item):
        if item in ['key', 'keys']:
            return self.keys
        if item in ['mouse']:
            return self.mouse['pressed']
        if item in ['mouse_pos']:
            return self.mouse['pos']
        if item in ['delta', 'move']:
            return self.mouse['move']
        raise KeyError

    def get(self, value, default=None):
        try:
            return self[value]
        except KeyError:
            return default

    def tick(self, event):
        """
        Update the key and mouse state. Push hardware events to the queue.

        :param event: ppb.Event
        :return:
        """
        # Due to a pygame problem, must get the events before key and button
        # states.
        events = self.hardware.events()
        engine.message(events)
        self.keys = self.hardware.keys()
        self.mouse = self.hardware.mouse()

    def key(self, key_id):
        try:
            return self.keys[key_id]
        except TypeError:
            return False

    def __repr__(self):
        return "Controller[keys: {}, mouse: {}]".format(self.keys, self.mouse)


def control_move(controller, up=0, down=1, right=2, left=3, speed=None):
    """
    Bind to an object as a Tick event callback to update player velocity
    based on key presses.

    :param controller: Controller
    :param up: integer key_id
    :param down: integer key_id
    :param right: integer key_id
    :param left: integer key_id
    :param speed: Optional magnitude. If the object manages its own simulation
                  speed, this is unnecessary.
    :return func
    """
    def callback(self, _):
        direction = Vec(controller.key(right) - controller.key(left),
                        controller.key(down) - controller.key(up))
        if speed is not None:
            result = direction * speed
        else:
            result = direction * self.speed
        self.velocity = result
    return callback


def emit_object(game_object, parameters, button=None, initial_speed=1.):
    """
    Create an emitter callback function.

    Bind to a game object as a callback for a MouseButtonDown event to emit
    other game objects.

    :param game_object: Type
    :param parameters: dict to be passed to game_object
    :param button: int A specific mouse button to respond to.
    :param initial_speed: float game unit magnitude. Cannot be zero.
    """
    if initial_speed == 0:
        raise ValueError("Initial speed must not be 0.")

    def callback(self, event):
        if button is not None and event.id != button:
                return

        try:
            start_offset = self.radius
        except AttributeError:
            start_offset = 0

        direction = Vec(event.pos.x - self.pos.x,
                        event.pos.y - self.pos.y).normalize()
        offset = direction.scale(start_offset)
        direction *= initial_speed
        position = self.pos + offset
        game_object(pos=position, velocity=direction, **parameters)
    return callback
