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
This module documents a class that creates the advanced configuration
window.

@author: Lateef Alabi-Oki
@organization: Scribes
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

class Window(object):
	"""
	This class implements the advanced configuration window.
	"""

	def __init__(self, editor, manager):
		"""
		Initialize object.

		@param self: Reference to the Window instance.
		@type self: A Window object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param manager: Object that manages all components.
		@type manager: A Manager object.
		"""
		self.__init_attributes(editor, manager)
		self.__set_properties()
		self.__sig_id1 = manager.connect("show-window", self.__show_window_cb)
		self.__sig_id2 = manager.connect("destroy", self.__destroy_cb)
		self.__sig_id3 = self.__window.connect("delete-event", self.__delete_event_cb)
		self.__sig_id4 = self.__window.connect("key-press-event", self.__key_press_event_cb)

	def __init_attributes(self, editor, manager):
		"""
		Initialize object attributes.
		"""
		self.__editor = editor
		self.__manager = manager
		self.__window = manager.glade.get_widget("Window")
		self.__sig_id1 = self.__sig_id2 = self.__sig_id3 = None
		self.__sig_id4 = None
		return

	def __set_properties(self):
#		self.__window.set_transient_for_window(self.__editor)
		return 

	def __show(self):
		self.__window.show_all()
		return

	def __hide(self):
		self.__window.hide()
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sig_id1, self.__manager)
		self.__editor.disconnect_signal(self.__sig_id2, self.__manager)
		self.__editor.disconnect_signal(self.__sig_id3, self.__window)
		self.__editor.disconnect_signal(self.__sig_id4, self.__window)
		self.__window.destroy()
		del self
		self = None
		return

	def __show_window_cb(self, *args):
		self.__show()
		return False

	def __key_press_event_cb(self, window, event):
		"""
		Handles callback when the "key-press-event" signal is emitted.
		"""
		from gtk import keysyms
		if event.keyval != keysyms.Escape: return False
		self.__hide()
		return True

	def __delete_event_cb(self, *args):
		self.__hide()
		return True

	def __destroy_cb(self, *args):
		self.__hide()
		self.__destroy()
		return
