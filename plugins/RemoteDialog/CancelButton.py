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
This module documents a class that implements the open button for the
file chooser

@author: Lateef Alabi-Oki
@organization: Scribes
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

class Button(object):
	"""
	This class defines the properties and behavior of the open button on
	the file chooser.
	"""

	def __init__(self, editor, manager):
		"""
		Initialize object.

		@param self: Reference to the Button instance.
		@type self: A Button object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param manager: Object that manages file chooser components.
		@type manager: A Manager object.
		"""
		self.__init_attributes(editor, manager)
		self.__sig_id1 = manager.connect("destroy", self.__destroy_cb)
		self.__sig_id2 = self.__button.connect("clicked", self.__clicked_cb)
		self.__button.set_property("sensitive", True)

	def __init_attributes(self, editor, manager):
		"""
		Initialize object.

		@param self: Reference to the Button instance.
		@type self: A Button object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param manager: Object that manages file chooser components.
		@type manager: A Manager object.
		"""
		self.__editor = editor
		self.__manager = manager
		self.__button = manager.glade.get_widget("CancelButton")
		return

	def __destroy(self):
		"""
		Destroy object.

		@param self: Reference to the Button instance.
		@type self: A Button object.
		"""
		self.__editor.disconnect_signal(self.__sig_id1, self.__manager)
		self.__editor.disconnect_signal(self.__sig_id2, self.__button)
		self.__button.destroy()
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		"""
		Handles callback when this object needs to be destroyed.

		@param self: Reference to the Button instance.
		@type self: A Button object.
		"""
		self.__destroy()
		return

	def __clicked_cb(self, *args):
		"""
		Handles callback when the button is clicked.

		@param self: Reference to the But instance.
		@type self: A_or_An class object.
		"""
		self.__manager.emit("hide-window")
		return