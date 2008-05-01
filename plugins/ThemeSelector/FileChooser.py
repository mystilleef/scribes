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
		self.__set_properties()
		self.__sigid1 = self.__manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = self.__chooser.connect("file-activated", self.__file_activated_cb)
		self.__sigid3 = self.__chooser.connect("selection-changed", self.__selection_changed_cb)
		self.__sigid4 = self.__manager.connect("load-schemes", self.__load_schemes_cb)
		self.__chooser.set_property("sensitive", True)

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
		self.__sigid1 = self.__status_id = None
		return

	def __set_properties(self):
		"""
		Set file chooser properties.

		@param self: Reference to the FileChooser instance.
		@type self: A FileChooser object.
		"""
		from gtk import FileFilter
		filefilter = FileFilter()
		filefilter.set_name("Color Scheme Files")
#		filefilter.add_mime_type("text/xml")
		filefilter.add_pattern("*.xml")
		self.__chooser.add_filter(filefilter)
		self.__set_folder()
		return

	def __set_folder(self):
		"""
		Select folder and file.

		@param self: Reference to the FileChooser instance.
		@type self: A FileChooser object.
		"""
		from os.path import exists
		if exists(self.__editor.desktop_folder):
			self.__chooser.set_current_folder(self.__editor.desktop_folder)
		else:
			self.__chooser.set_current_folder(self.__editor.home_folder)
		return False

	def __load_schemes(self):
		"""
		Load selected file(s)

		@param self: Reference to the FileChooser instance.
		@type self: A FileChooser object.
		"""
		try:
			filenames = self.__chooser.get_filenames()
			from Utils import load_schemes, get_schemes, get_scheme_id
			from Utils import change_theme
			schemes = get_schemes(filenames)
			from os.path import join, exists
			from os import makedirs
			folder = join(self.__editor.home_folder, ".gnome2/scribes/styles")
			if not exists(folder): makedirs(folder)
			load_schemes(schemes, folder)
			scheme_id = get_scheme_id(schemes[-1])
			change_theme(scheme_id)
			self.__manager.emit("hide")
		except ValueError:
			print "Invalid color theme."
		return False

	def __destroy(self):
		"""
		Destroy object.

		@param self: Reference to the FileChooser instance.
		@type self: A FileChooser object.
		"""
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__chooser)
		self.__editor.disconnect_signal(self.__sigid3, self.__chooser)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
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

	def __file_activated_cb(self, *args):
		"""
		Handles callback when the "file-activated" signal is emitted.

		@param self: Reference to the FileChooser instance.
		@type self: A FileChooser object.
		"""
		from gobject import idle_add
		idle_add(self.__load_schemes)
		return False

	def __load_schemes_cb(self, *args):
		"""
		Handles callback when the "load-files" signal is emitted.

		@param self: Reference to the FileChooser instance.
		@type self: A FileChooser object.
		"""
		from gobject import idle_add
		idle_add(self.__load_schemes)
		return

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
		selected_file = False if folders else True
		self.__manager.emit("selected-file", selected_file)
		return False
