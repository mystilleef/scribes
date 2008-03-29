# -*- coding: utf-8 -*-
# Copyright © 2006 Lateef Alabi-Oki
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
This module documents a class that creates the window for the document
browser.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2006 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class Window(object):
	"""
	This class creates the window for the document browser window.
	"""

	def __init__(self, editor, manager):
		"""
		Initialize an instance of this class.

		@param self: Reference to the BrowserWindow instance.
		@type self: A BrowserWindow object.

		@param manager: Reference to the Manager instance
		@type manager: A Manager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(editor, manager)
		self.__set_properties()
		self.__sig_id1 = self.__manager.connect("destroy", self.__destroy_cb)
		self.__sig_id2 = self.__manager.connect("show-chooser-window", self.__show_window_cb)
		self.__sig_id3 = self.__manager.connect("hide-chooser-window", self.__hide_window_cb)
		self.__sig_id4 = self.__window.connect("delete-event", self.__delete_event_cb)
		self.__sig_id5 = self.__window.connect("key-press-event", self.__key_press_event_cb)
		self.__window.set_property("sensitive", True)

	def __init_attributes(self, editor, manager):
		"""
		Initialize data attributes.

		@param self: Reference to the Window instance.
		@type self: A Window object.

		@param manager: Reference to the Manager instance
		@type manager: A Manager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__manager = manager
		self.__editor = editor
		self.__window = manager.filechooser_glade.get_widget("Window")
		self.__sig_id1 = self.__status_id = None
		return

	def __set_properties(self):
		"""
		Define the default behavior of the dialog.

		@param self: Reference to the Window instance.
		@type self: A Window object.
		"""
		#width, height = self.__editor.calculate_resolution_independence(self.__editor.window, 1.6, 2.5)
		#self.__window.set_property("default-width", 640)
		#self.__window.set_property("default-height", 480)
		self.__window.set_transient_for(self.__editor.window)
		return

	def __show(self):
		"""
		Show the document browser.

		@param self: Reference to the Window instance.
		@type self: A Window object.
		"""
#		self.__editor.emit("show-dialog", self.__window)
#		from i18n import msg0001
#		self.__status_id = self.__editor.feedback.set_modal_message(msg0001, "open")
		self.__window.show_all()
		return False

	def __hide(self):
		"""
		Hide the document browser.

		@param self: Reference to the Window instance.
		@type self: A Window object.
		"""
#		self.__editor.emit("hide-dialog", self.__window)
#		self.__editor.feedback.unset_modal_message(self.__status_id)
		self.__window.hide()
		return False

	def __destroy(self):
		"""
		Destroy object.

		@param self: Reference to the Window instance.
		@type self: A Window object.
		"""
		self.__editor.disconnect_signal(self.__sig_id1, self.__manager)
		self.__editor.disconnect_signal(self.__sig_id2, self.__manager)
		self.__editor.disconnect_signal(self.__sig_id3, self.__manager)
		self.__editor.disconnect_signal(self.__sig_id4, self.__window)
		self.__editor.disconnect_signal(self.__sig_id5, self.__window)
		self.__window.destroy()
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		"""
		Handles callback when "destroy" signal is emitted.

		@param self: Reference to the Window instance.
		@type self: An Window object.
		"""
		self.__destroy()
		return

	def __hide_window_cb(self, *args):
		"""
		Handles callback when "destroy" signal is emitted.

		@param self: Reference to the Window instance.
		@type self: An Window object.
		"""
		self.__hide()
		return

	def __show_window_cb(self, *args):
		"""
		Handles callback when "destroy" signal is emitted.

		@param self: Reference to the Window instance.
		@type self: An Window object.
		"""
		from gobject import idle_add
		idle_add(self.__show)
		return

	def __delete_event_cb(self, *args):
		"""
		Handles callback when "destroy" signal is emitted.

		@param self: Reference to the Window instance.
		@type self: An Window object.
		"""
		self.__hide()
		return True

	def __key_press_event_cb(self, window, event):
		"""
		Handles callback when "destroy" signal is emitted.

		@param self: Reference to the Window instance.
		@type self: An Window object.
		"""
		from gtk import keysyms
		if event.keyval != keysyms.Escape: return False
		self.__hide()
		return True
