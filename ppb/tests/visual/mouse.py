"""
Mouse visual test module.

On Tick:
    Print "Mouse position {vector}"
    Print "Mouse movement delta {vector}"
    Print "Mouse button {number} held"

On Mouse Button Down:
    Print "Mouse button {number} pressed at position {x}, {y}"

On Mouse Button Up:
    Print "Mouse button {number} released at position {x}, {y}"
"""
from ppb.event import MouseButtonDown, MouseButtonUp, Tick
from ppb.tests.visual import Runner
import ppb.hw as hardware


message = "Mouse button {number} {action} at position {x}, {y}"
delta_message = " and moved {x}, {y}"


def mouse_button_down(mouse_event):
    print(message.format(number=mouse_event.id,
                         x=mouse_event.pos.x,
                         y=mouse_event.pos.y,
                         action="pressed"))


def mouse_button_up(mouse_event):
    print(message.format(number=mouse_event.id,
                         x=mouse_event.pos.x,
                         y=mouse_event.pos.y,
                         action="released"))


def tick(tick_event):
    for identification, button in enumerate(hardware.mouse['pressed']):
        if button:
            m1 = message.format(number=identification,
                                 x=hardware.mouse['pos'].x,
                                 y=hardware.mouse['pos'].y,
                                 action="held")
            m2 = delta_message.format(x=hardware.mouse['move'].x,
                                      y=hardware.mouse['move'].y)
            print(m1 + m2)


test_runner = Runner("sdl2")
test_runner.set_events([(MouseButtonDown, mouse_button_down),
                        (MouseButtonUp, mouse_button_up),
                        (Tick, tick)])
test_runner.run()