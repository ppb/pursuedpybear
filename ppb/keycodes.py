"""
Key Codes used by the keyboard system.

Note that only base (unshifted) symbols and keys have keycodes.

There is significant variation between layouts of different countries; keys are
given by their semantic meaning and not by their position. But these are also
not suitable for text input.
"""
import ppb.flags


class KeyCode(ppb.flags.Flag, abstract=True):
    """
    A raw keyboard scan code.
    """


class A(KeyCode):
    ""


class B(KeyCode):
    ""


class C(KeyCode):
    ""


class D(KeyCode):
    ""


class E(KeyCode):
    ""


class F(KeyCode):
    ""


class G(KeyCode):
    ""


class H(KeyCode):
    ""


class I(KeyCode):
    ""


class J(KeyCode):
    ""


class K(KeyCode):
    ""


class L(KeyCode):
    ""


class M(KeyCode):
    ""


class N(KeyCode):
    ""


class O(KeyCode):
    ""


class P(KeyCode):
    ""


class Q(KeyCode):
    ""


class R(KeyCode):
    ""


class S(KeyCode):
    ""


class T(KeyCode):
    ""


class U(KeyCode):
    ""


class V(KeyCode):
    ""


class W(KeyCode):
    ""


class X(KeyCode):
    ""


class Y(KeyCode):
    ""


class Z(KeyCode):
    ""


class One(KeyCode):
    """
    1

    Shift+1 is ! on american keyboards
    """


class Two(KeyCode):
    """
    2

    Shift+2 is @ on american keyboards
    """


class Three(KeyCode):
    """
    3

    Shift+3 is # on american keyboards
    """


class Four(KeyCode):
    """
    4

    Shift+4 is $ on american keyboards
    """


class Five(KeyCode):
    """
    5

    Shift+5 is % on american keyboards
    """


class Six(KeyCode):
    """
    6

    Shift+6 is ^ on american keyboards
    """


class Seven(KeyCode):
    """
    7

    Shift+7 is & on american keyboards
    """


class Eight(KeyCode):
    """
    8

    Shift+8 is * on american keyboards
    """


class Nine(KeyCode):
    """
    9

    Shift+9 is ( on american keyboards
    """


class Zero(KeyCode):
    """
    0

    Shift+0 is ) on american keyboards
    """


class F1(KeyCode):
    ""


class F2(KeyCode):
    ""


class F3(KeyCode):
    ""


class F4(KeyCode):
    ""


class F5(KeyCode):
    ""


class F6(KeyCode):
    ""


class F7(KeyCode):
    ""


class F8(KeyCode):
    ""


class F9(KeyCode):
    ""


class F10(KeyCode):
    ""


class F11(KeyCode):
    ""


class F12(KeyCode):
    ""


class F13(KeyCode):
    ""


class F14(KeyCode):
    ""


class F15(KeyCode):
    ""


class F16(KeyCode):
    ""


class F17(KeyCode):
    ""


class F18(KeyCode):
    ""


class F19(KeyCode):
    ""


class F20(KeyCode):
    ""


class AltRight(KeyCode):
    "Right Alt modifier, called Option on mac"


class AltLeft(KeyCode):
    "Left Alt modifier, called Option on mac"


class Backslash(KeyCode):
    """
    \\
    
    Shift+\\ is | on american keyboards
    """


class Backspace(KeyCode):
    ""


class BracketLeft(KeyCode):
    """
    [
    
    Shift+[ is { on american keyboards
    """


class BracketRight(KeyCode):
    """
    ]
    
    Shift+] is } on american keyboards
    """


class CapsLock(KeyCode):
    ""


class Comma(KeyCode):
    """
    ,
    
    Shift+, is < on american keyboards
    """


class CtrlLeft(KeyCode):
    "Left Control modifier"


class CtrlRight(KeyCode):
    "Right Control modifier"


class Delete(KeyCode):
    ""


class Down(KeyCode):
    "Down navigation arrow"


class End(KeyCode):
    ""


class Enter(KeyCode):
    "Enter, return, newline"


class Equals(KeyCode):
    """
    =

    Shift+= is + on american keyboards
    """


class Escape(KeyCode):
    ""


class Function(KeyCode):
    "Fn, if reported by your keyboard"


class Grave(KeyCode):
    """
    `, usually to the left of 1 or F1 on american keyboards.

    Shift+` is ~ on american keyboards
    """


class Home(KeyCode):
    ""


class Insert(KeyCode):
    ""


class Left(KeyCode):
    "Left navigation arrow"


class Menu(KeyCode):
    ""


class Minus(KeyCode):
    """
    -
    
    Shift+- is _ on american keyboards
    """


class NumLock(KeyCode):
    ""


class PageDown(KeyCode):
    ""


class PageUp(KeyCode):
    ""


class Pause(KeyCode):
    """
    Pause, generally lives next to Print Screen and Scroll Lock.
    
    Also Break.
    """


class Period(KeyCode):
    """
    .
    
    Shift+. is > on american keyboards
    """


class PrintScreen(KeyCode):
    """
    PrtSc, PrtScrn, etc

    Also System Request/SysReq/SysRq/etc.
    """


class Quote(KeyCode):
    """
    ', the single quote

    Shift+' is " on american keyboards
    """


class Right(KeyCode):
    "Right navigation arrow"


class ScrollLock(KeyCode):
    ""


class Semicolon(KeyCode):
    """
    ;

    Shift+; is : on american keyboards
    """


class ShiftLeft(KeyCode):
    "Left shift modifier"


class ShiftRight(KeyCode):
    "Right shift modifier"


class Slash(KeyCode):
    """
    /

    Shift+/ is ? on american keyboards
    """


class Space(KeyCode):
    ""


class SuperLeft(KeyCode):
    "Left Super modifier, also called Windows or Command"


class SuperRight(KeyCode):
    "Right Super modifier, also called Windows or Command"


class Tab(KeyCode):
    ""


class Up(KeyCode):
    "Up navigation arrow"


# Numpad codes (unified between pygame and pyglet)
# 0 1 2 3 4 5 6 7 8 9 add begin decimal delete divide down end enter equals
# f1 f2 f3 f4 home insert left minus multiply next page down page up period plus
# prior right separator space subtract tab up 
