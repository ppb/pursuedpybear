import logging
import time

from ppb.utilities import Queue
import ppb.event as event

event_queue = Queue()
scenes = []
last_tick = time.time()
running = True


def run(first_scene):
    push(first_scene)
    while running:
        try:
            cur_event = event_queue.pop()
        except IndexError:
            tick()
            cur_event = None
        scenes[-1].publish(cur_event)
    return 0


def tick(*_):
    global last_tick

    current_tick = time.time()
    value = current_tick - last_tick
    event_queue.push(event.Tick(value))
    last_tick = current_tick


def game_quit(*_):
    global running
    running = False


def push(e):
    try:
        scene = e.scene
    except AttributeError:
        scene = e
    scene.subscribe(event.Tick, "engine", tick)
    scene.subscribe(event.Quit, "engine", game_quit)
    scene.subscribe(event.PushScene, "engine", push)
    scene.subscribe(event.PopScene, "engine", pop)
    scene.subscribe(event.ReplaceScene, "engine", replace)
    scenes.append(scene)


def pop(*_):
    scenes.pop()


def replace(e):
    pop()
    push(e)
