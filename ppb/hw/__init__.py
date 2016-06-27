from functools import wraps
import logging
import warnings

import ppb.engine

current_hardware = None
keys = None
mouse = None


def import_pygame():
    import ppb.hw.pygame_wrapper as pygame_wrapper
    return pygame_wrapper


def import_sdl2():
    import ppb.hw.sdl2_wrapper as sdl2_wrapper
    return sdl2_wrapper

hardware_options = {"pygame": import_pygame,
                    "sdl2": import_sdl2}


@wraps
def check_hardware_status(func):
    def wrapped(*args, **kwargs):
        if current_hardware is not None:
            return func(*args, **kwargs)
        else:
            raise RuntimeError("No hardware library chosen.")
    return wrapped


@wraps
def catch_missing(func):
    def wrapped(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except AttributeError:
            raw_message = "Wrapper {} has not implemented {}"
            m = raw_message.format(current_hardware.name, func.__name__)
            raise NotImplementedError(m)
    return wrapped


def choose(lib):
    """
    Convenience function to initialize the hardware package for use.

    :param lib str of key in hardware_options

    An import function should be named import_* where * is the name of the
    hardware library being wrapped. It should perform the module import and
    return the module.

    It must also be added to the hardware options dict.
    """
    try:
        global current_hardware
        global current_hardware_name
        current_hardware = hardware_options[lib]()
        current_hardware_name = lib
    except KeyError:
        lib_error_msg = "Hardware library {} not recognized.".format(lib)
        raw_help_msg = "Please select one of the following options:\n {}"
        help_msg = raw_help_msg.format(hardware_options.keys())
        raise AttributeError("{}\n{}".format(lib_error_msg, help_msg))


@check_hardware_status
@catch_missing
def init(*args, **kwargs):
    """
    Delegates init to the current_hardware.

    A hardware wrapper should initialize its libraries and modules, set up a
    display with a proper title, and have the canvas to draw to.
    """
    current_hardware.init(*args, **kwargs)
    global keys
    keys = current_hardware.keys()
    global mouse
    mouse = current_hardware.mouse()


@check_hardware_status
@catch_missing
def quit(*args, **kwargs):
    """
    Delegate quit to the current_hardware.

    A hardware wrapper should manage graceful shutdown of its modules.
    """
    current_hardware.quit(*args, **kwargs)


@check_hardware_status
@catch_missing
def update_input(*_):
    global keys
    keys = current_hardware.keys()
    global mouse
    mouse = current_hardware.mouse()
    ppb.engine.message(current_hardware.events())


@check_hardware_status
@catch_missing
def View(*args, **kwargs):
    warnings.warn(DeprecationWarning())
    return current_hardware.View(*args, **kwargs)


@check_hardware_status
@catch_missing
def display():
    return current_hardware.display


@check_hardware_status
@catch_missing
def image_primitive(*args, **kwargs):
    return current_hardware.image_primitive(*args, **kwargs)