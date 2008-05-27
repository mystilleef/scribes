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
This module documents a class that creates the template editor's window.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class Window(object):
	"""
	This class creates the window for the template editor.
	"""

	def __init__(self, manager, editor):
		"""
		Initialize object.

		@param self: Reference to the Window instance.
		@type self: A Window object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("show-window", self.__show_cb)
		self.__sigid3 = manager.connect("hide-window", self.__hide_cb)
		self.__sigid4 = self.__window.connect("delete-event", self.__delete_event_cb)
		self.__sigid5 = self.__window.connect("key-press-event", self.__key_press_event_cb)
		self.__sigid6 = self.__window.connect("drag-data-received", self.__drag_data_received_cb)
		self.__window.set_property("sensitive", True)

	def __init_attributes(self, manager, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the Window instance.
		@type self: A Window object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__manager = manager
		self.__editor = editor
		self.__is_visible = False
		self.__window = manager.glade.get_widget("Window")
		return

	def __set_properties(self):
		"""
		Set default properties.

		@param self: Reference to the Window instance.
		@type self: A Window object.
		"""
#		width, height = self.__editor.calculate_resolution_independence(self.__editor.window, 1.6, 1.6)
#		self.__window.set_property("default-width", width)
#		self.__window.set_property("default-height", height)
		from gtk import DEST_DEFAULT_ALL
#		self.__window.set_property("window-position", WIN_POS_CENTER)
#		self.__window.set_property("destroy-with-parent", True)
		self.__window.set_transient_for(self.__editor.window)
		targets = [("text/uri-list", 0, 111)]
		from gtk.gdk import ACTION_COPY
		self.__window.drag_dest_set(DEST_DEFAULT_ALL, targets, ACTION_COPY)
		return

	def __show_window(self):
		"""
		Show window.

		@param self: Reference to the Window instance.
		@type self: A Window object.
		"""
		self.__window.show_all()
		self.__is_visible = True
		self.__window.present()
		return

	def __hide_window(self):
		"""
		Hide window.

		@param self: Reference to the Window instance.
		@type self: A Window object.
		"""
		self.__window.hide()
		self.__is_visible = False
		return

	def __destroy_cb(self, manager):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the Window instance.
		@type self: A Window object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.
		"""
		self.__editor.disconnect_signal(self.__sigid1, manager)
		self.__editor.disconnect_signal(self.__sigid2, manager)
		self.__editor.disconnect_signal(self.__sigid3, manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__window)
		self.__editor.disconnect_signal(self.__sigid5, self.__window)
		self.__editor.disconnect_signal(self.__sigid6, self.__window)
		self.__window.destroy()
		self = None
		del self
		return

	def __show_cb(self, *args):
		"""
		Handles callback when the "show-window" signal is emitted.
		"""
		self.__show_window()
		return

	def __hide_cb(self, *args):
		"""
		Handles callback when the "hide-window" signal is emitted.
		"""
		self.__hide_window()
		return

	def __delete_event_cb(self, *args):
		"""
		Handles callback when the "delete-event" signal is emitted.
		"""
		self.__manager.emit("hide-window")
		return True

	def __key_press_event_cb(self, window, event):
		"""
		Handles callback when the "key-press-event" signal is emitted.
		"""
		if self.__is_visible is False: return False
		from gtk import keysyms
		if event.keyval != keysyms.Escape: return False
		self.__manager.emit("hide-window")
		return True

	def __drag_data_received_cb(self, *args):
		return False
