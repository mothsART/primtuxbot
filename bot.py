#!/usr/bin/env python3

import sys

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import cairo


supports_alpha = False
img = Gtk.Image()

def print_d(message, debug=True):
    if not debug:
        return
    print(message)

def screen_changed(widget, debug=False):
    global supports_alpha

    screen = widget.get_screen()
    visual = screen.get_rgba_visual()

    if visual is None:
        print_d("Your screen does not support alpha channels!", debug)
        visual = screen.get_system_visual()
        supports_alpha = False
    else:
        print_d("Your screen supports alpha channels!", debug)
        supports_alpha = True

    width = screen.get_width()
    height = screen.get_height()
    widget.move(width - 500, height - 500)
    widget.set_visual(visual)


def expose_draw(widget, event, data=None, debug=False):
    global supports_alpha

    cr = Gdk.cairo_create(widget.get_window())

    if supports_alpha:
        print_d("setting transparent window", debug)
        cr.set_source_rgba(1.0, 1.0, 1.0, 0.0) 
    else:
        print_d("setting opaque window", debug)
        cr.set_source_rgb(1.0, 1.0, 1.0)

    cr.set_operator(cairo.OPERATOR_SOURCE)
    cr.paint()

    return False

def clicked(window, event, userdata=None):
    img.set_from_file('tux_salut.png')


class PrimtuxBot(Gtk.Window):

    def __init__(self, title, debug=False):
        Gtk.Window.__init__(self, title = title)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        self.set_default_size(400, 400)
        self.connect("delete-event", Gtk.main_quit)
        
        self.set_app_paintable(True)
        self.connect("draw", expose_draw, self, debug)
        self.connect("screen-changed", screen_changed)

        self.set_decorated(False)
        self.add_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.connect("button-press-event", clicked)

        fixed_container = Gtk.Fixed()
        self.add(fixed_container)

        img.set_from_file('tux.png')
        fixed_container.add(img)

        screen_changed(self, debug)
        self.show_all()
        Gtk.main()


if __name__ == "__main__":
    debug = False
    if (
        len(sys.argv) > 1
        and '-d' == sys.argv[1] in ['-d', '--debug']
    ):
        debug = True
    PrimtuxBot('Primtux Store', debug)
