from time import time as systemtime

from Xlib import XK, X
from Xlib.display import Display
from Xlib.protocol.event import KeyPress, KeyRelease

# Translations:
# https://github.com/python-xlib/python-xlib/blob/master/Xlib/keysymdef/latin1.py

__all__ = ('send_character', 'message_to_x11')


def send_character(display, root, win, time, character):
    # aao = XK.string_to_keysym('diaeresis')
    keysym = XK.string_to_keysym(character.replace(' ', 'space'))
    keycode = display.keysym_to_keycode(keysym)

    settings = dict(
        time=time,
        root=root,
        window=win,
        same_screen=1,
        child=X.NONE,
        root_x=0,
        root_y=0,
        event_x=0,
        event_y=0,
        state=0,
        detail=keycode
    )

    for key in (KeyPress, KeyRelease):
        event = key(**settings)
        display.send_event(win, event, propagate=True)
        display.sync()


def message_to_x11(text):
    display = Display()
    data = dict(
        time=int(systemtime()),
        display=display,
        win=display.get_input_focus().focus,
        root=display.screen().root,
    )

    for character in text:
        send_character(**data | dict(character=character))


if __name__ == '__main__':
    message_to_x11('Hello World')  # replace for testing purpose with symbols
    input()  # x11 keypresses gets here
