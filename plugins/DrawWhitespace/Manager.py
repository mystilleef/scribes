# -*- coding: utf-8 -*-
# Copyright © 2008 Lateef Alabi-Oki
#
# This file is part of Scribes.
#
# Scribes is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Scribes is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Scribes; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

"""
This module documents a class that draws white spaces in the Scribes.
This is a port of the Gedit

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

class Manager(object):
	"""
	This class shows white spaces in the buffer.
	"""

	def __init__(self, editor):
		"""
		Initialize object.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(editor)
		self.__sig_id1 = self.__textview.connect('event-after', self.__event_after_cb)

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__textview = editor.textview
		from gtk.gdk import color_parse
		self.__color = color_parse("orange")
		return

	def __draw_whitespaces(self, event, start, end):
		cr = event.window.cairo_create()
		cr.set_source_color(self.__color)
		cr.set_line_width(0.8)
		while start.compare(end) <= 0:
			c = start.get_char()
			if c == '\t':
				self.__draw_tab(cr, start)
			elif c == '\040':
				self.__draw_space(cr, start)
			elif c == '\302\240':
				self.__draw_nbsp(cr, start)
			if not start.forward_char(): break
		cr.stroke()
		return False

	def __draw_tab(self, cr, iterator):
		rect = self.__textview.get_iter_location(iterator)
		from gtk import TEXT_WINDOW_TEXT
		x, y = self.__textview.buffer_to_window_coords(TEXT_WINDOW_TEXT,
												rect.x,
												rect.y + rect.height * 2 / 3)
		cr.save()
		cr.move_to(x + 4, y)
		cr.rel_line_to(rect.width - 8, 0)
		cr.rel_line_to(-3,-3)
		cr.rel_move_to(+3,+3)
		cr.rel_line_to(-3,+3)
		cr.restore()
		return False

	def __draw_space(self, cr, iterator):
		rect = self.__textview.get_iter_location(iterator)
		from gtk import TEXT_WINDOW_TEXT
		x, y = self.__textview.buffer_to_window_coords(TEXT_WINDOW_TEXT,
												rect.x + rect.width / 2,
												rect.y + rect.height * 2 / 3)
		cr.save()
		cr.move_to(x, y)
		from math import pi
		cr.arc(x, y, 0.8, 0, 2 * pi)
		cr.restore()
		return False

	def __draw_nbsp(self, cr, iterator):
		rect = self.__textview.get_iter_location(iterator)
		from gtk import TEXT_WINDOW_TEXT
		x, y = self.__textview.buffer_to_window_coords(TEXT_WINDOW_TEXT,
												rect.x,
												rect.y + rect.height / 2)
		cr.save()
		cr.move_to(x + 2, y - 2)
		cr.rel_line_to(+7,0)
		cr.rel_line_to(-3.5,+6.06)
		cr.rel_line_to(-3.5,-6.06)
		cr.restore()
		return False

	def __event_after_cb(self, textview, event):
		from gtk.gdk import EXPOSE
		from gtk import TEXT_WINDOW_TEXT
		if event.type != EXPOSE or \
			event.window != textview.get_window(TEXT_WINDOW_TEXT):
			return False
		y = textview.window_to_buffer_coords(TEXT_WINDOW_TEXT, event.area.x, event.area.y)[1]
		start = textview.get_line_at_y(y)[0]
		end = textview.get_line_at_y(y + event.area.height)[0]
		end.forward_to_line_end()
		self.__draw_whitespaces(event, start, end)
		return False

	def destroy(self):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		del self
		self = None
		return
