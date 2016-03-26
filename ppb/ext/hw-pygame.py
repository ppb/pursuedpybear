import pygame
import logging

from ppb.event import KeyDown, KeyUp, MouseButtonDown, MouseButtonUp


display = None


def init(resolution):
    """
    Initialize pygame modules

    :return:
    """
    global display

    pygame.init()

    display = pygame.display.set_mode(resolution)


def quit():
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

    :return: dictionary with pos and pressed keys.
    """
    logging.debug("This function is a stub. Return value is zeroed.")
    return {"pos": None, "pressed": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}}


def events():
    """
    Translate pygame events into ppb events.

    :return:
    """
    logging.debug("This function is a stub. Expect changes.")
    rv = []
    for e in pygame.event.get():
        # TODO: Replace if/else tree with a dict of pygame event type to ppb event type.
        # May need helper functions to handle varied structure.

        if e.type == pygame.KEYDOWN:  # TODO: Check how pygame delineates events.
            rv.append(KeyDown(e.key, ""))  # TODO: Map of key_id to value.
            # Consider replacing identity with a map to engine specific names.
        elif e.type == pygame.KEYUP:
            rv.append(KeyUp(e.key, ""))
        elif e.type == pygame.MOUSEBUTTONDOWN:
            rv.append(MouseButtonDown(e.button, ""))
        elif e.type == pygame.MOUSEBUTTONUP:
            rv.append(MouseButtonUp(e.button, ""))
    return rv


def render(group):
    group.draw(display)
