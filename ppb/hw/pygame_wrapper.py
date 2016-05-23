from __future__ import division

import logging

import pygame
from pygame.sprite import DirtySprite

import ppb.components.view
from ppb.event import KeyDown, KeyUp, MouseButtonDown, MouseButtonUp, Quit
from ppb.vmath import Vector2 as Vector
from ppb.components.models import Renderable


display = None


def init(resolution, title):
    """
    Initialize pygame modules

    :param: resolution: tuple of pixel resolution
    :return:
    """
    global display

    pygame.init()
    display = pygame.display.set_mode(resolution)
    pygame.display.set_caption(title)


def quit(*_):
    """
    Quit pygame

    :return:
    """
    pygame.quit()


def keys():
    """
    Get the dictionary of key state.

    :return:
    """
    return pygame.key.get_pressed()


def mouse():
    """
    Get mouse position and key state.

    :return: dictionary with pos and pressed keys and move keys.
             pos and move are vectors.
             pressed is an iterable of booleans
    """
    pressed = pygame.mouse.get_pressed()
    pos = Vector(*pygame.mouse.get_pos())
    move = Vector(*pygame.mouse.get_rel())
    return {"pos": pos,
            "pressed": pressed,
            "move": move}


def events():
    """
    Translate pygame events into ppb events.

    Must be called before mouse

    :return:
    """
    rv = []

    key_events = {pygame.KEYDOWN: KeyDown,
                  pygame.KEYUP: KeyUp}

    mouse_events = {pygame.MOUSEBUTTONDOWN: MouseButtonDown,
                    pygame.MOUSEBUTTONUP: MouseButtonUp}

    for e in pygame.event.get():
        new_event = None
        if e.type in key_events.keys():
            try:
                name = chr(e.key)
            except ValueError:
                name = ""

            new_event = key_events[e.type](e.key, name)
        elif e.type in mouse_events.keys():
            new_event = mouse_events[e.type](e.button, "", Vector(*e.pos))
        elif e.type == pygame.QUIT:
            new_event = Quit()
        if new_event:
            rv.append(new_event)
    return rv


def render(group):
    try:
        group.draw(display)
    except AttributeError:
        logging.exception("Incompatible drawing group.")


def update_screen(*_):
    pygame.display.flip()


class View(ppb.components.view.View):

    def __init__(self, scene, screen, fps, hardware, background):
        super(View, self).__init__(scene, screen, fps, hardware)
        self.layers = pygame.sprite.LayeredDirty()
        self.background = background

    def render(self):
        self.layers.update()
        updates = self.layers.draw(display, self.background)
        pygame.display.update(updates)

    def add(self, sprite, layer=0):
        self.layers.add(sprite, layer=layer)

    def remove(self, sprite):
        self.layers.remove(sprite)

    def change_layer(self, sprite, layer):
        self.layers.change_layer(sprite, layer)

    def object_created(self, obj):
        obj = obj.obj
        if isinstance(obj, Renderable):
            self.add(Sprite(obj))

    @property
    def sprites(self):
        return self.layers.sprites()


class Sprite(DirtySprite, ppb.components.view.Sprite):

    def __init__(self, model, *groups):
        super(Sprite, self).__init__(*groups)
        self.image = model.image
        self.rect = self.image.get_rect()
        x_offset = self.rect.width / 2
        y_offset = self.rect.height / 2
        self.offset = Vector(x_offset, y_offset)
        self.model = model
        self.update()

    def update(self):
        offset_position = self.model.pos - self.offset
        new_pos = tuple(int(x) for x in offset_position)
        if new_pos != self.rect.topleft:
            self.rect.topleft = new_pos
            self.dirty = 1


def image_primitive(color, size):
    try:
        image = pygame.Surface(size)
    except ValueError:
        image = pygame.Surface((size, size))

    image.fill(color)
    return image
