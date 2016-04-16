"""
An event driven application engine.
"""

from collections import Iterable
import time

from ppb.utilities import Queue
import ppb.event as event

event_queue = Queue()
scenes = []

last_tick = time.time()
run_time = 0

running = True


def run(first_scene):
    """
    Start and manage application.

    :param first_scene: Publisher
    :return:
    """
    push(first_scene)
    callbacks = {event.PushScene: push,
                 event.PopScene: pop,
                 event.ReplaceScene: replace,
                 event.Quit: game_quit}
    while running:
        try:
            cur_event = event_queue.pop()
        except IndexError:
            cur_event = tick()
        event_type = type(cur_event)
        if event_type in callbacks:
            callbacks[event_type](cur_event)
        scenes[-1].publish(cur_event)
    return 0


def tick():
    """
    Raise a new Tick
    :param _: Tick
    :return:
    """
    global last_tick
    global run_time
    current_tick = time.time()
    sec = current_tick - last_tick
    run_time += sec
    last_tick = current_tick
    return event.Tick(sec, run_time)


def game_quit(*_):
    """
    Stop running the engine.

    :param _: Event
    :return:
    """
    global running
    running = False


def push(e):
    """
    Push a scene to the stack.

    :param e: Event or Publisher
    :return:
    """
    try:
        scene = e.scene
    except AttributeError:
        scene = e
    scenes.append(scene)


def pop(*_):
    """
    Pop a scene from the stack.

    :param _: Event
    :return:
    """
    scenes.pop()


def replace(e):
    """
    Pop a scene from the stack then push a scene to the stack.

    :param e: Event
    :return:
    """
    pop()
    push(e)


def message(e):
    """
    Push an Event to the queue.

    :param e: Event
    :return:
    """
    if isinstance(e, Iterable):
        event_queue.extend(e)
    else:
        event_queue.push(e)
