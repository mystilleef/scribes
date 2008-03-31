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
This module documents a class that implements the file chooser for the file chooser window.

@author: Lateef Alabi-Oki
@organization: Scribes
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

class FileChooser(object):
	"""
	This class defines the behavior and properties of an open file
	chooser.
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
		self.__chooser.set_property("sensitive", True)
		self.__sig_id1 = self.__manager.connect_after("show-window", self.__show_window_cb)
		self.__sig_id2 = self.__manager.connect("destroy", self.__destroy_cb)
		self.__sig_id3 = self.__chooser.connect("file-activated", self.__file_activated_cb)
		self.__sig_id4 = self.__chooser.connect("selection-changed", self.__selection_changed_cb)

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
		self.__chooser = manager.filechooser_glade.get_widget("FileChooser")
		self.__sig_id1 = self.__status_id = None
		return

	def __set_folder(self):
		"""
		Select folder and file.

		@param self: Reference to the FileChooser instance.
		@type self: A FileChooser object.
		"""
#		if not (self.__editor.uri): return False
#		self.__chooser.set_uri(self.__editor.uri)
		self.__chooser.set_current_folder(self.__editor.home_folder)
		return False

	def __destroy(self):
		"""
		Destroy object.

		@param self: Reference to the FileChooser instance.
		@type self: A FileChooser object.
		"""
		self.__editor.disconnect_signal(self.__sig_id1, self.__manager)
		self.__editor.disconnect_signal(self.__sig_id2, self.__manager)
		self.__editor.disconnect_signal(self.__sig_id3, self.__chooser)
		self.__editor.disconnect_signal(self.__sig_id4, self.__chooser)
		self.__chooser.destroy()
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		"""
		Handles callback when the destroy signal is emitted.

		@param self: Reference to the FileChooser instance.
		@type self: A FileChooser object.
		"""
		self.__destroy()
		return

	def __show_window_cb(self, *args):
		"""
		Handles callback when the "show-window" signal is emitted.

		@param self: Reference to the FileChooser instance.
		@type self: A FileChooser object.
		"""
		from gobject import idle_add
		idle_add(self.__set_folder)
#		self.__set_folder()
		return

	def __file_activated_cb(self, *args):
		"""
		Handles callback when the "file-activated" signal is emitted.

		@param self: Reference to the FileChooser instance.
		@type self: A FileChooser object.
		"""
		self.__manager.emit("new-folder", self.__chooser.get_current_folder())
		return False

	def __selection_changed_cb(self, *args):
		"""
		Handles callback when selection changes in file chooser.

		@param self: Reference to the FileChooser instance.
		@type self: A FileChooser object.
		"""
		filenames = self.__chooser.get_filenames()
		if not filenames: return False
		from os.path import isdir
		is_a_folder = lambda _file: isdir(_file)
		folders = filter(is_a_folder, filenames)
		selected_file = True if folders else False
		self.__manager.emit("selected-file", selected_file)
		return False
