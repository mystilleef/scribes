from math import pi
from gtk import EventBox
from gtk.gdk import Color

class TriggerWidget(EventBox):

	def __init__(self):
		EventBox.__init__(self)
		self.__init_attributes()
		self.set_app_paintable(True)
		self.set_size_request(self.__size, self.__size)
		self.connect("size-allocate", self.__allocate_cb)
		self.connect("expose-event", self.__expose_cb)

	def __init_attributes(self):
		# position could be "top-left", "top-right", "bottom-left", "bottom-right"
		self.__position = "top-right"
		self.__size = 24
		self.__offset = 2
		self.__bcolor = "black"
		self.__fcolor = "blue"
		return

	def __set_size(self, size):
		self.__size = size
		self.set_size_request(size, size)
		from gtk.gdk import Rectangle
		rectangle = Rectangle(0, 0, size, size)
		self.size_allocate(rectangle)
		self.queue_draw()
		return

	def __set_position(self, position): self.__position = position
	def __set_border_color(self, color): self.__bcolor = color
	def __set_fill_color(self, color): self.__fcolor = color

	# Public API
	position = property(lambda self: self.__position, __set_position)
	size = property(lambda self: self.__size, __set_size)
	border_color = property(lambda self: self.__bcolor, __set_border_color)
	fill_color = property(lambda self: self.__fcolor, __set_fill_color)

	def __draw(self, cr, position="top-right"):
		offset = self.__offset
		size, radius = self.__size, self.__size - offset
		corner = {
			"top-right": ((size, 0), (size, radius), (offset, 0)),
			"top-left": ((0, 0), (0, radius), (radius, 0)),
			"bottom-left": ((0, size), (0, offset), (radius, size)),
			"bottom-right": ((size, size), (size, offset), (offset, size)),
		}
		origin, vline, hline = corner[position]
		cr.set_line_width(3)
		# draw vertical line
		cr.move_to(*origin)
		cr.line_to(*vline)
		# draw horizontal line
		cr.move_to(*origin)
		cr.line_to(*hline)
		cr.stroke()
		# draw arc
		cr.set_line_width(2)
		from cairo import ANTIALIAS_DEFAULT
		cr.set_antialias(ANTIALIAS_DEFAULT)
		x, y = origin
		cr.arc(x, y, radius, 0, 2*pi)
		cr.stroke_preserve()
		return False

	def __allocate_cb(self, win, allocation):
		from gtk.gdk import Pixmap
		bitmap = Pixmap(self.window, self.__size, self.__size, 1)
		cr = bitmap.cairo_create()
		from cairo import OPERATOR_SOURCE, OPERATOR_CLEAR, OPERATOR_OVER
		# Clear the bitmap
		cr.set_operator(OPERATOR_CLEAR)
		cr.paint()
		# Draw the arc
		cr.set_operator(OPERATOR_OVER)
		self.__draw(cr, self.__position)
		cr.fill()
		# Set the window shape
		self.window.shape_combine_mask(bitmap, 0, 0)
		return False

	def __paint(self):
		cr = self.window.cairo_create()
		# Draw arc
		bcolor = Color(self.__bcolor)
		cr.set_source_rgba(bcolor.red_float, bcolor.green_float, bcolor.blue_float, 0.5)
		self.__draw(cr, self.__position)
		fcolor = Color(self.__fcolor)
		cr.set_source_rgba(fcolor.red_float, fcolor.green_float, fcolor.blue_float, 0.25)
		cr.fill()
		return False

	def __expose_cb(self, *args):
#		try:
#			from gobject import idle_add, source_remove
#			source_remove(self.__timer)
#		except AttributeError:
#			pass
#		finally:
#			self.__timer = idle_add(self.__paint)
		self.__paint()
		return False