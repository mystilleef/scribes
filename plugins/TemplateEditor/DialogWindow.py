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
	This class creates the window for the template editor to add or edit
	templates.
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
		self.__sigid2 = manager.connect("show-add-dialog", self.__show_add_dialog_cb)
		self.__sigid3 = manager.connect("show-edit-dialog", self.__show_edit_dialog_cb)
		self.__sigid4 = manager.connect("dialog-hide-window", self.__hide_cb)
		self.__sigid5 = self.__window.connect("delete-event", self.__delete_event_cb)
		self.__sigid6 = self.__window.connect("key-press-event", self.__key_press_event_cb)
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
		self.__window = manager.dglade.get_widget("Window")
		return

	def __set_properties(self):
		window = self.__manager.glade.get_widget("Window")
		self.__window.set_transient_for(window)
		return

	def __show_window(self):
		"""
		Show window.

		@param self: Reference to the Window instance.
		@type self: A Window object.
		"""
		self.__window.show_all()
		self.__window.present()
		return

	def __hide_window(self):
		"""
		Hide window.

		@param self: Reference to the Window instance.
		@type self: A Window object.
		"""
		self.__window.hide()
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
		self.__editor.disconnect_signal(self.__sigid4, manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__window)
		self.__editor.disconnect_signal(self.__sigid6, self.__window)
		self.__window.destroy()
		self = None
		del self
		return

	def __show_add_dialog_cb(self, *args):
		"""
		Handles callback when the "show-window" signal is emitted.
		"""
		self.__window.set_title("Add Template")
		self.__show_window()
		return False

	def __show_edit_dialog_cb(self, *args):
		"""
		Handles callback when the "show-window" signal is emitted.
		"""
		self.__window.set_title("Edit Template")
		self.__show_window()
		return False

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
		self.__manager.emit("dialog-hide-window")
		return True

	def __key_press_event_cb(self, window, event):
		"""
		Handles callback when the "key-press-event" signal is emitted.
		"""
		from gtk import keysyms
		if event.keyval != keysyms.Escape: return False
		self.__manager.emit("dialog-hide-window")
		return True
