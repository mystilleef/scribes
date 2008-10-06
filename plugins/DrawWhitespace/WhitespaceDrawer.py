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
This is a port of Gedit's whitespace plugin. All credit goes to

Copyright (C) 2006 - Paolo Borelli
Copyright (C) 2007 - Steve Frécinaux

@author: Lateef Alabi-Oki, Paolo Borelli, Steve Frécinaux
@organization: The Scribes Project
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

class Drawer(object):
	"""
	This class draws white spaces in the buffer.
	"""

	def __init__(self, editor, manager):
		"""
		Initialize object.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(editor, manager)
		self.__sig_id1 = self.__textview.connect('event-after', self.__event_after_cb)
		self.__sig_id2 = manager.connect("destroy", self.__destroy_cb)
		self.__sig_id3 = manager.connect("color", self.__color_cb)
		self.__sig_id4 = manager.connect("show", self.__show_cb)
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=9999)

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		self.__textview = editor.textview
		from gtk.gdk import color_parse
		self.__color = color_parse("orange")
		self.__show = False
		self.__blocked = False
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
		try:
			from cairo import Error
			cr.stroke()
		except Error:
			pass
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
		x, y = self.__textview.buffer_to_window_coords(TEXT_WINDOW_TEXT, rect.x, rect.y + rect.height / 2)
		cr.save()
		cr.move_to(x + 2, y - 2)
		cr.rel_line_to(+7,0)
		cr.rel_line_to(-3.5,+6.06)
		cr.rel_line_to(-3.5,-6.06)
		cr.restore()
		return False

	def __block_event_after_signal(self):
		if self.__blocked: return
		self.__textview.handler_block(self.__sig_id1)
		self.__blocked = True
		return

	def __unblock_event_after_signal(self):
		if self.__blocked is False: return
		self.__textview.handler_unblock(self.__sig_id1)
		self.__blocked = False
		return

	def __check_event_signal(self):
		if self.__show:
			self.__unblock_event_after_signal()
		else:
			self.__block_event_after_signal()
		self.__textview.queue_draw()
		return

	def __precompile_methods(self):
		methods = (self.__event_after_cb, self.__draw_whitespaces,
			self.__draw_tab, self.__draw_space)
		self.__editor.optimize(methods)
		return False

	def __event_after_cb(self, textview, event):
		if self.__show is False: return False
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

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __color_cb(self, manager, color):
		from gtk.gdk import color_parse
		self.__color = color_parse(color)
		return False

	def __show_cb(self, manager, show):
		self.__show = show
		self.__check_event_signal()
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sig_id1, self.__textview)
		self.__editor.disconnect_signal(self.__sig_id2, self.__manager)
		self.__editor.disconnect_signal(self.__sig_id3, self.__manager)
		self.__editor.disconnect_signal(self.__sig_id4, self.__manager)
		del self
		self = None
		return
