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
This module documents a class that implements the file chooser for the
file chooser window.

@author: Lateef Alabi-Oki
@organization: Scribes
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

class FileChooser(object):
	"""
	This class defines the behavior and properties of an save file
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
		self.__set_properties()
		self.__chooser.set_property("sensitive", True)
		self.__sig_id1 = self.__manager.connect_after("show-window", self.__show_window_cb)
		self.__sig_id2 = self.__manager.connect("destroy", self.__destroy_cb)
		self.__sig_id3 = self.__entry.connect("activate", self.__file_activated_cb)
		self.__sig_id4 = self.__entry.connect("changed", self.__changed_cb)
		self.__sig_id5 = self.__manager.connect("rename", self.__rename_file_cb)
		self.__sig_id6 = self.__chooser.connect("confirm-overwrite", self.__confirm_overwrite_cb)

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
		self.__chooser = manager.glade.get_widget("FileChooser")
		self.__entry = self.__chooser.get_children()[0].get_children()[0].get_children()[0].get_children()[2]
		self.__sig_id1 = self.__status_id = None
		return

	def __set_properties(self):
		"""
		Set file chooser properties.

		@param self: Reference to the FileChooser instance.
		@type self: A FileChooser object.
		"""
		from SCRIBES.dialogfilter import create_filter_list
		for filter_ in create_filter_list():
			self.__chooser.add_filter(filter_)
		self.__set_folder()
		return

	def __set_folder(self):
		"""
		Select folder and file.

		@param self: Reference to the FileChooser instance.
		@type self: A FileChooser object.
		"""
		if self.__editor.uri:
			from gnomevfs import URI, get_local_path_from_uri
			folder_uri = str(URI(self.__editor.uri).parent)
			current_name = str(URI(self.__editor.uri).short_name)
			if folder_uri != self.__chooser.get_current_folder_uri():
				self.__chooser.set_current_folder_uri(folder_uri)
			self.__chooser.set_current_name(current_name)
		else:
			from i18n import msg0003
			self.__chooser.set_current_name(msg0003)
			try:
				self.__chooser.set_current_folder(self.__editor.desktop_folder)
			except:
				self.__chooser.set_current_folder(self.__editor.home_folder)
		self.__entry.grab_focus()
		from gobject import idle_add
		idle_add(self.__emit_error)
		return False

	def __rename_file(self):
		"""
		Load selected file(s)

		@param self: Reference to the FileChooser instance.
		@type self: A FileChooser object.
		"""
		self.__manager.emit("hide-window")
		encoding = self.__manager.encoding
		uri = self.__chooser.get_uri()
		self.__editor.emit("rename-document", uri, encoding)
		return False

	def __emit_error(self):
		value = True if self.__entry.get_text() else False
		self.__manager.emit("error", value)
		return False

	def __destroy(self):
		"""
		Destroy object.

		@param self: Reference to the FileChooser instance.
		@type self: A FileChooser object.
		"""
		self.__editor.disconnect_signal(self.__sig_id1, self.__manager)
		self.__editor.disconnect_signal(self.__sig_id2, self.__manager)
		self.__editor.disconnect_signal(self.__sig_id3, self.__entry)
		self.__editor.disconnect_signal(self.__sig_id4, self.__entry)
		self.__editor.disconnect_signal(self.__sig_id5, self.__manager)
		self.__chooser.destroy()
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		"""
		Handles callback when the "destroy" signal is emitted.

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
#		self.__entry.grab_focus()
		return

	def __file_activated_cb(self, *args):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the FileChooser instance.
		@type self: A FileChooser object.
		"""
		from gobject import idle_add
		idle_add(self.__rename_file)
		return False

	def __rename_file_cb(self, *args):
		"""
		Handles callback when the "rename" signal is emitted.

		@param self: Reference to the FileChooser instance.
		@type self: A FileChooser object.
		"""
		from gobject import idle_add
		idle_add(self.__rename_file)
		return

	def __changed_cb(self, *args):
		"""
		Handles callback when selection changes in file chooser.

		@param self: Reference to the FileChooser instance.
		@type self: A FileChooser object.
		"""
		from gobject import idle_add
		idle_add(self.__emit_error)
		return False

	def __confirm_overwrite_cb(self, *args):
		from gtk import FILE_CHOOSER_CONFIRMATION_CONFIRM
		return FILE_CHOOSER_CONFIRMATION_CONFIRM
