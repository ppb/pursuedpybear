import logging
import time

from ppb.utilities import Queue, Publisher
import ppb.event as event

publisher = Publisher()
event_queue = Queue()
scenes = []
last_tick = time.time()
running = True


def run(first_scene):
    scenes.append(first_scene)
    publisher.subscribe(event.Tick, "engine", tick)
    publisher.subscribe(event.Quit, "engine", game_quit)
    publisher.subscribe(event.PushScene, "engine", push)
    publisher.subscribe(event.PopScene, "engine", pop)
    publisher.subscribe(event.ReplaceScene, "engine", replace)
    while running:
        try:
            cur_event = event_queue.pop()
        except IndexError:
            tick()
        publisher.publish(cur_event)
        scenes[-1].publish(cur_event)
    return 0


def tick(*_):
    global last_tick

    current_tick = time.time()
    value = current_tick - last_tick
    logging.debug("Current time delta: {}".format(value))
    event_queue.push(event.Tick(value))
    last_tick = current_tick


def game_quit(*_):
    global running
    running = False


def push(e):
    scenes.append(e.scene)


def pop(*_):
    scenes.pop()


def replace(e):
    scenes.pop()
    scenes.append(e.scene)
