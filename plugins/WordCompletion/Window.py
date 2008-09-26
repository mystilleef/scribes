# -*- coding: utf-8 -*-
# Copyright © 2007 Lateef Alabi-Oki
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
This module documents a class that creates the window for word
completion window.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import Window

class CompletionWindow(Window):
	"""
	This class creates the window object for word completion.
	"""

	def __init__(self, manager, editor):
		from gtk import WINDOW_POPUP
		Window.__init__(self, WINDOW_POPUP)
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("show-window", self.__show_window_cb)
		self.__sigid3 = manager.connect("hide-window", self.__generic_hide_cb)
		self.__sigid5 = editor.window.connect("key-press-event", self.__key_press_event_cb)
		self.__sigid6 = editor.textview.connect("focus-out-event", self.__generic_hide_cb)
		self.__sigid7 = editor.textbuffer.connect("delete-range", self.__generic_hide_cb)
		self.__sigid8 = manager.connect_after("no-match-found", self.__generic_hide_cb)
		self.__sigid9 = editor.textview.connect("button-press-event", self.__button_press_event_cb)
		self.__block_signals()

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		self.__is_visible = False
		self.__signals_are_blocked = True
		# Pressing any of these keys will hide the word completion
		# window.
		from gtk import keysyms
		self.__keys = [keysyms.Tab, keysyms.Right, keysyms.Left,
			keysyms.Home, keysyms.End, keysyms.Insert, keysyms.Delete,
			keysyms.Page_Up, keysyms.Page_Down, keysyms.Escape]
		return

	def __set_properties(self):
		from gtk.gdk import WINDOW_TYPE_HINT_MENU
		self.set_property("type-hint", WINDOW_TYPE_HINT_MENU)
		self.set_property("width-request", 200)
		self.set_property("height-request", 200)
		self.set_property("border-width", 3)
		return

########################################################################
#
#							Helper Methods
#
########################################################################

	def __show_window(self):
		self.__manager.emit("is-visible", True)
		if self.__is_visible: return False
		if self.__signals_are_blocked: self.__unblock_signals()
		self.show_all()
		self.__is_visible = True
		return False

	def __hide_window(self):
		self.__manager.emit("is-visible", False)
		if not self.__is_visible: return False
		if not self.__signals_are_blocked: self.__block_signals()
		self.hide_all()
		self.__is_visible = False
		return False

	def __get_cursor_window_coordinates(self):
		textview = self.__editor.textview
		# Get the cursor's buffer coordinates.
		rectangle = textview.get_iter_location(self.__editor.cursor)
		# Get the cursor's window coordinates.
		from gtk import TEXT_WINDOW_TEXT
		position = textview.buffer_to_window_coords(TEXT_WINDOW_TEXT, rectangle.x,
												rectangle.y)
		cursor_x = position[0]
		cursor_y = position[1]
		return cursor_x, cursor_y

	def __get_cursor_size(self):
		# Get the cursor's size via its buffer coordinates.
		textview = self.__editor.textview
		rectangle = textview.get_iter_location(self.__editor.cursor)
		cursor_width = rectangle.width
		cursor_height = rectangle.height
		return cursor_width, cursor_height

	def __position_window(self, width, height):
		# Get the cursor's coordinate and size.
		cursor_x, cursor_y = self.__get_cursor_window_coordinates()
		cursor_height = self.__get_cursor_size()[1]
		# Get the text editor's textview coordinate and size.
		from gtk import TEXT_WINDOW_TEXT
		window = self.__editor.textview.get_window(TEXT_WINDOW_TEXT)
		rectangle = self.__editor.textview.get_visible_rect()
		window_x, window_y = window.get_origin()
		window_width, window_height = rectangle.width, rectangle.height
		# Determine where to position the completion window.
		position_x = window_x + cursor_x
		position_y = window_y + cursor_y + cursor_height
		# If the completion window extends past the text editor's buffer,
		# reposition the completion window inside the text editor's buffer area.
		if (position_x + width) > (window_x + window_width):
			position_x = (window_x + window_width) - width
		if (position_y + height) > (window_y + window_height):
			position_y = (window_y + cursor_y) - height
		if not self.__signals_are_blocked:
			if position_y != self.get_position()[1]:
				position_x = self.get_position()[0]
				self.move(position_x, position_y)
			return
		# Set the window's new position.
		self.move(position_x, position_y)
		return

	def __calculate_window_width(self, width):
		if width < 200:
			width = 200
		else:
			width += 28
		return width

	def __calculate_window_height(self, height):
		if height > 200: height = 200
		return height

	def __block_signals(self):
		self.__manager.handler_block(self.__sigid1)
		self.__manager.handler_block(self.__sigid3)
		self.__editor.window.handler_block(self.__sigid5)
		self.__editor.textview.handler_block(self.__sigid6)
		self.__editor.textbuffer.handler_block(self.__sigid7)
		self.__manager.handler_block(self.__sigid8)
		self.__signals_are_blocked = True
		return

	def __unblock_signals(self):
		self.__manager.handler_unblock(self.__sigid1)
		self.__manager.handler_unblock(self.__sigid3)
		self.__editor.window.handler_unblock(self.__sigid5)
		self.__editor.textview.handler_unblock(self.__sigid6)
		self.__editor.textbuffer.handler_unblock(self.__sigid7)
		self.__manager.handler_unblock(self.__sigid8)
		self.__signals_are_blocked = False
		return

########################################################################
#
#					Signal and Event Handlers
#
########################################################################

	def __destroy_cb(self, manager):
		self.__editor.disconnect_signal(self.__sigid1, manager)
		self.__editor.disconnect_signal(self.__sigid2, manager)
		self.__editor.disconnect_signal(self.__sigid3, manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__editor)
		self.__editor.disconnect_signal(self.__sigid6, self.__editor)
		self.__editor.disconnect_signal(self.__sigid7, self.__editor)
		self.__editor.disconnect_signal(self.__sigid8, manager)
		self.__editor.disconnect_signal(self.__sigid9, self.__editor)
		self.destroy()
		del self
		self = None
		return

	def __generic_hide_cb(self, *args):
		self.__hide_window()
		return False

	def __show_window_cb(self, manager, view):
		width, height = view.size_request()
		width = self.__calculate_window_width(width) + 3
		height = self.__calculate_window_height(height) + 3
		self.resize(width, height)
		self.set_property("width-request", width)
		self.set_property("height-request", height)
		self.__position_window(width, height)
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__show_window, priority=9999)
#		self.__show_window()
		return

	def __key_press_event_cb(self, window, event):
		if event.keyval in self.__keys: self.__hide_window()
		return False

	def __button_press_event_cb(self, *args):
		self.__hide_window()
		return False
