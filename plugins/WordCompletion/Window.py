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
		"""
		Initialize object.

		@param self: Reference to the CompletionWindow instance.
		@type self: A CompletionWindow object.

		@param manager: Reference to the CompletionManager instance.
		@type manager: A CompletionManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		from gtk import WINDOW_POPUP
		Window.__init__(self, WINDOW_POPUP)
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__signal_id_1 = manager.connect("destroy", self.__destroy_cb)
		self.__signal_id_2 = manager.connect("show-window", self.__show_window_cb)
		self.__signal_id_3 = manager.connect("hide-window", self.__generic_hide_cb)
		self.__signal_id_5 = editor.window.connect("key-press-event", self.__key_press_event_cb)
		self.__signal_id_6 = editor.textview.connect("focus-out-event", self.__generic_hide_cb)
		self.__signal_id_7 = editor.textbuffer.connect("delete-range", self.__generic_hide_cb)
		self.__signal_id_8 = manager.connect("no-match-found", self.__generic_hide_cb)
		self.__signal_id_9 = editor.textview.connect("button-press-event", self.__button_press_event_cb)
		self.__block_signals()
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__precompile_methods, priority=PRIORITY_LOW)

	def __init_attributes(self, manager, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the CompletionWindow instance.
		@type self: A CompletionWindow object.

		@param manager: Reference to the CompletionManager instance.
		@type manager: A CompletionManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param completion: Reference to the WordCompletionManager instance.
		@type completion: A WordCompletionManager object.
		"""
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
		"""
		Define the completion window's default properties.

		@param self: Reference to the CompletionWindow instance.
		@type self: A CompletionWindow object.
		"""
		from gtk.gdk import WINDOW_TYPE_HINT_MENU
		self.set_property("type-hint", WINDOW_TYPE_HINT_MENU)
		self.set_property("width-request", 200)
		self.set_property("height-request", 200)
		return

########################################################################
#
#							Helper Methods
#
########################################################################

	def __show_window(self):
		"""
		Show the completion window.

		@param self: Reference to the CompletionWindow instance.
		@type self: A CompletionWindow object.
		"""
		self.__manager.emit("is-visible", True)
		if self.__is_visible: return False
		if self.__signals_are_blocked: self.__unblock_signals()
		self.show_all()
		self.__is_visible = True
		return False

	def __hide_window(self):
		"""
		Hide the completion window.

		@param self: Reference to the CompletionWindow instance.
		@type self: A CompletionWindow object.
		"""
		self.__manager.emit("is-visible", False)
		if not self.__is_visible: return False
		if not self.__signals_are_blocked: self.__block_signals()
		self.hide_all()
		self.__is_visible = False
		return False

	def __position_window(self, width, height):
		"""
		Position the completion window in the text editor's buffer.

		@param width: The completion window's width.
		@type width: An Integer object.

		@param height: The completion window's height.
		@type height: An Integer object.
		"""
		# Get the cursor's coordinate and size.
		cursor_x, cursor_y = self.__editor.get_cursor_window_coordinates()
		cursor_height = self.__editor.get_cursor_size()[1]
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
		"""
		Calculate the completion window's height.

		@param self: Reference to the CompletionWindow instance.
		@type self: A CompletionWindow object.

		@param height: The completion window's view's height.
		@type height: An Integer object.

		@return: The height of the completion window.
		@rtype: An Integer object.
		"""
		if width < 200:
			width = 200
		else:
			width += 28
		return width

	def __calculate_window_height(self, height):
		"""
		Calculate the completion window's height.

		@param self: Reference to the CompletionWindow instance.
		@type self: A CompletionWindow object.

		@param height: The completion window's view's height.
		@type height: An Integer object.

		@return: The height of the completion window.
		@rtype: An Integer object.
		"""
		if height > 200: height = 200
		return height

	def __block_signals(self):
		"""
		Block some signals when the window is hidden.

		@param self: Reference to the CompletionWindow instance.
		@type self: A CompletionWindow object.
		"""
		self.__manager.handler_block(self.__signal_id_1)
		self.__manager.handler_block(self.__signal_id_3)
		self.__editor.window.handler_block(self.__signal_id_5)
		self.__editor.textview.handler_block(self.__signal_id_6)
		self.__editor.textbuffer.handler_block(self.__signal_id_7)
		self.__manager.handler_block(self.__signal_id_8)
		self.__signals_are_blocked = True
		return

	def __unblock_signals(self):
		"""
		Unblock signals when window is shown.

		@param self: Reference to the CompletionWindow instance.
		@type self: A CompletionWindow object.
		"""
		self.__manager.handler_unblock(self.__signal_id_1)
		self.__manager.handler_unblock(self.__signal_id_3)
		self.__editor.window.handler_unblock(self.__signal_id_5)
		self.__editor.textview.handler_unblock(self.__signal_id_6)
		self.__editor.textbuffer.handler_unblock(self.__signal_id_7)
		self.__manager.handler_unblock(self.__signal_id_8)
		self.__signals_are_blocked = False
		return

########################################################################
#
#					Signal and Event Handlers
#
########################################################################

	def __destroy_cb(self, manager):
		"""
		Destroy instance of this object.

		@param self: Reference to the CompletionTreeView instance.
		@type self: A CompletionTreeView object.

		@param manager: Reference to the CompletionManager instance.
		@type manager: A CompletionManager object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, manager)
		self.__editor.disconnect_signal(self.__signal_id_2, manager)
		self.__editor.disconnect_signal(self.__signal_id_3, manager)
		self.__editor.disconnect_signal(self.__signal_id_5, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_6, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_7, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_8, manager)
		self.__editor.disconnect_signal(self.__signal_id_9, self.__editor)
		self.destroy()
		del self
		self = None
		return

	def __generic_hide_cb(self, *args):
		"""
		Generic callback handler to hide the window.

		@param self: Reference to the CompletionWindow instance.
		@type self: A CompletionWindow object.

		@param args: Irrelevant arguments.
		@type args: A List object.
		"""
		self.__hide_window()
		return False

	def __show_window_cb(self, manager, view):
		"""
		Handles callback when the "show-window" signal is shown.

		@param self: Reference to the CompletionWindow instance.
		@type self: A CompletionWindow object.

		@param manager: Reference to the CompletionManager instance.
		@type manager: A CompletionManager object.

		@param view: Reference to the CompletionTreeView instance.
		@type view: A CompletionTreeView object.
		"""
		width, height = view.size_request()
		width = self.__calculate_window_width(width) + 3
		height = self.__calculate_window_height(height) + 3
		self.resize(width, height)
		self.set_property("width-request", width)
		self.set_property("height-request", height)
		self.__position_window(width, height)
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__show_window, priority=5000)
		return

	def __key_press_event_cb(self, window, event):
		"""
		Handles callback when the "key-press-event" signal is emitted.

		@param self: Reference to the CompletionWindow instance.
		@type self: A CompletionWindow object.

		@param window: Reference to the CompletionWindow instance.
		@type window: A CompletionWindow object.
		"""
		from gobject import idle_add, PRIORITY_LOW
		if event.keyval in self.__keys: self.__hide_window()
		return False

	def __button_press_event_cb(self, *args):
		"""
		Handles callback when the "button-press-event" signal is emitted.

		@param self: Reference to the ScribesTextView instance.
		@type self: A ScribesTextView object.
		"""
		self.__hide_window()
		return False

	def __precompile_methods(self):
		try:
			from psyco import bind
			bind(self.__key_press_event_cb)
			bind(self.__show_window_cb)
			bind(self.__generic_hide_cb)
		except ImportError:
			pass
		return False
