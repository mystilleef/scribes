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

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = self.__chooser.connect("file-activated", self.__file_activated_cb)
		self.__sigid3 = self.__chooser.connect("selection-changed", self.__selection_changed_cb)
		self.__sigid4 = manager.connect("import-button-clicked", self.__file_activated_cb)
		self.__chooser.set_property("sensitive", True)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__chooser = manager.iglade.get_widget("FileChooser")
		return

	def __set_properties(self):
		from gtk import FileFilter
		filter_ = FileFilter()
		filter_.set_name("Template Files")
		filter_.add_mime_type("text/xml")
		self.__chooser.add_filter(filter_)
		self.__set_folder()
		return

	def __set_folder(self):
		from os.path import exists
		if exists(self.__editor.desktop_folder):
			self.__chooser.set_current_folder(self.__editor.desktop_folder)
		else:
			self.__chooser.set_current_folder(self.__editor.home_folder)
		self.__chooser.grab_focus()
		return

	def __import_templates(self):
		filenames = self.__chooser.get_filenames()
		self.__manager.emit("hide-import-window")
		self.__manager.emit("process-imported-files", filenames)
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__chooser)
		self.__editor.disconnect_signal(self.__sigid3, self.__chooser)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__chooser.destroy()
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return

	def __file_activated_cb(self, *args):
		self.__import_templates()
		return True

	def __selection_changed_cb(self, *args):
		filenames = self.__chooser.get_filenames()
		if not filenames: return False
		from os.path import isdir
		is_a_folder = lambda _file: isdir(_file)
		folders = filter(is_a_folder, filenames)
		selected_file = False if folders else True
		self.__manager.emit("import-selected-file", selected_file)
		return False
