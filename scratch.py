# from copy import copy
# from timeit import timeit
#
# count = 10_000
# test_set = {str(x) for x in range(1_000)}
# test_objects = (lambda x: x, lambda x: object(), lambda x: str(x))
# test_sequences = (list, set, tuple)
#
#
# def build_sequence(collection, obj, number):
#     return collection(obj(x) for x in range(number))
#
#
# test_set = build_sequence(set, lambda x:x, 1_000)
#
# snippets = {
#     "list_comprehension": "[x for x in test_value]",
#     "generator": "list(x for x in test_value)",
#     "list": "list(test_value)",
#
#     "method intersection": "test_set.intersection(test_value)",
#     "binary and": "test_value & test_value",
#     "copy": "copy(test_value)",
#     "method copy": "test_value.copy()",
#
#     "frozenset": "frozenset(test_value)",
#     "set": "set(test_value)",
#
#     "splat set": "{*test_value}",
#     "splat list": "[*test_value]",
# }
#
# name_space = locals()
# name_space["test_value"] = test_set
# for name, snippet in snippets.items():
#     result = timeit(snippet, number=count, globals=name_space)
#     print(f"Result of {name}: {result / count}")
#
#
#
# import ppb
#
#
# class Ship(ppb.BaseSprite):
#     pass
#
#
# def setup(scene):
#     scene.add(Ship(pos=(0, 260)))
#
#
# ppb.run(scene_kwargs={"set_up": setup})
#
#




# import ppb
#
# ppb.run()


# import ppb
#
#
# class Ship(ppb.BaseSprite):
#     pass
#
#
# def setup(scene):
#     scene.add(Ship(pos=(0, 160)))
#
#
# ppb.run(resolution=(200, 400), scene_kwargs={"set_up": setup})


# import ppb
#
#
# class Ship(ppb.BaseSprite):
#
#     def on_update(self, update_event, signal):
#         self.position += 0, -(50 * update_event.time_delta)
#
#
# def setup(scene):
#     scene.add(Ship(pos=(0, 160)))
#
#
# ppb.run(resolution=(200, 400), scene_kwargs={"set_up": setup})

# import ppb
#
#
# class Ship(ppb.BaseSprite):
#
#     def on_update(self, update_event, signal):
#         self.position += 0, -(100 * update_event.time_delta)
#
#
# def setup(scene):
#     scene.add(Ship(pos=(0, 260)))
#
#
# ppb.run(scene_kwargs={"set_up": setup})

# from dataclasses import dataclass
#
#
# class Parent:
#
#     def __init__(self, name, *children):
#         self.name = name
#         self.children = children
#         for child in self.children:
#             child.__name = name
#             Child.__follow_my_lead = Parent.say_name
#
#     def say_name(self):
#         return self.name
#
#     def follow_my_lead(self):
#         for child in self.children:
#             print(child.__follow_my_lead())
#
#
# @dataclass
# class Child:
#     def __init__(self, name):
#         self.name = name
#
# p = Parent("Bob", Child("Dash"), Child("Violet"))
#
# p.follow_my_lead()

# from pygame import locals
# from ppb import keycodes
#
# ppb_codes = {kc.lower(): kc for kc in keycodes.__dict__ if isinstance(getattr(keycodes, kc), keycodes.KeyCode)}
# pygame_codes = [(v.split("_")[1].lower(), f"pygame.{v}") for v in locals.__dict__ if v.startswith("K_")]
#
# # print(ppb_codes)
# # print(pygame_codes)
#
# keycodes = {}
# rejected = set()
# name: str
# for name, value in pygame_codes:
#     if name in ppb_codes:
#         keycodes[value] = f"keys.{ppb_codes[name]}"
#     elif not name.startswith("KP"):
#         rejected.add(value)
#
# output = "{\n    "
#
# output += ",\n    ".join(f"{k}: {v}" for k, v in keycodes.items())
#
# output += "\n}"
#
# # print(output)
# print("\n".join(v for v in rejected))

# v: str
# for v in locals.__dict__:
#     if v.startswith("K_"):
#         pg_name = v.split("_")[1]
#         print(pg_name)

# import pygame as pg
#
# pg.init()
#
# running = True
#
# while running:
#     for event in pg.event.get():
#         if event.type == pg.QUIT:
#             running = False
#         elif event.type == pg.KEYDOWN:
#             print(event)
# my_int = 3
# [b == '1' for b in bin(my_int)[2:].rjust(4)[::-1]]

# from pygame import locals
#
# output = []
# for v in locals.__dict__:
#     if v.startswith("KMOD"):
#         output.append((v, getattr(locals, v)))
#
#
# print(sorted(output, key=lambda x: x[1]))

import timeit

class Cacher:
    _size = 2
    _offset_value = None

    def __init__(self):
        self.size = self.size

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
        self._offset_value = value / 2


class Calculator:
    size = 2

    @property
    def _offset_value(self):
        return self.size / 2


print(timeit.timeit('cache._offset_value', setup='cache = Cacher()', globals=globals()))
print(timeit.timeit('calc._offset_value', setup='calc = Calculator()', globals=globals()))


import ppb
from ppb import GameEngine
from ppb import BaseScene
from ppb.events import *
my_object = object()
my_object.event_extension = lambda : my_object
from ppb import *
class GameOverScene(BaseScene): pass
class Game(BaseScene): pass

class Enemy(BaseSprite): pass

class Tile(BaseSprite): pass

class Ship(BaseSprite):
    leader = None

    def on_update(self, update_event, signal):
        scene = update_event.scene
        for enemy in scene.get(kind=Enemy):
            self.respond_to_enemy(enemy)
        for trigger in scene.get(tag="triggers"):
            trigger.activate(self)
        for tile in scene.get(kind=Tile, tag="dangerous"):
            self.apply_terrain(tile)

    def respond_to_enemy(self, sprite): pass
    def apply_terrain(self, tile): pass
    def spawn_wingmen(self, scene):
        scene.add(Ship(leader=self))

    def leader_behavior(self, event, signal): pass

    def follower_behavior(self, event, signal): pass


class Thing:
    lives = 0
    score = 10000
    @staticmethod

    def on_unpaused(self, event, signal):
        signal(StopScene())

    def on_scene_paused(self, event, signal):
        self.stop_timers(event)

    def on_scene_continued(self, event, signal):
        self.start_timers(event)

    def on_scene_started(self, event, signal):
        self.initialize_timers(event)

    def on_player_life_lost(self, event, signal):
        if self.lives <= 0:
            signal(ReplaceScene(GameOverScene, kwargs={"score": self.score}))

    def on_scene_stopped(self, event, signal):
        self.unload_assets()

    def stop_timers(self, event):
        pass

    def start_timers(self, event):
        pass

    def initialize_timers(self, event):
        pass

    def unload_assets(self):
        pass