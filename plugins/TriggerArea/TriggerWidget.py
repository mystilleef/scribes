from gtk import EventBox
from math import pi

import math

import cairo
import gtk
from gtk import gdk

SIZE = 24
RADIUS_LENGTH = SIZE - 3

class TriggerWidget(EventBox):

	def __init__(self):
		EventBox.__init__(self)
		self.set_size_request(SIZE, SIZE)
		self.connect("size-allocate", self.__allocate_cb)
		self.connect("expose-event", self.__expose_cb)
		self.set_app_paintable(True)

	def __allocate_cb(self, win, allocation):
		w, h = SIZE, SIZE
		bitmap = gtk.gdk.Pixmap(self.window, SIZE, SIZE, 1)
		cr = bitmap.cairo_create()
		# Clear the bitmap
		cr.set_source_rgb(0.0, 0.0, 0.0)
		cr.set_operator(cairo.OPERATOR_CLEAR)
		cr.paint()
		# Draw the arc
		cr.set_operator(cairo.OPERATOR_SOURCE)
		cr.move_to(SIZE, 0)
		cr.line_to(SIZE, RADIUS_LENGTH)
		cr.move_to(SIZE, 0)
		cr.line_to(SIZE-RADIUS_LENGTH, 0)
		cr.stroke()
		cr.arc(SIZE, 0, RADIUS_LENGTH, 0, 2*pi)
		cr.stroke_preserve()
		cr.fill()
		# Set the window shape
		self.window.shape_combine_mask(bitmap, 0, 0)
		return False

	def __expose_cb(self, *args):
		cr = self.window.cairo_create()
		cr.set_source_rgba(0.0, 0.0, 0.0, 0.4)
		cr.set_line_width(3)
		cr.move_to(SIZE, 0)
		cr.line_to(SIZE, RADIUS_LENGTH)
		cr.move_to(SIZE, 0)
		cr.line_to(SIZE-RADIUS_LENGTH, 0)
		cr.stroke()
		cr.set_line_width(2)
		cr.arc(SIZE, 0, RADIUS_LENGTH, 0, 2*pi)
		cr.stroke_preserve()
		cr.set_source_rgba(0.0, 0.0, 0.0, 0.2)
		cr.fill()
		return False
