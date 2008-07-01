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
		self.__sigid2 = manager.connect_after("show-export-window", self.__show_cb)
		self.__sigid3 = manager.connect("language-selected", self.__language_selected_cb)
		self.__sigid4 = manager.connect("export-button-clicked", self.__export_button_clicked_cb)
		self.__chooser.set_property("sensitive", True)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__chooser = manager.eglade.get_widget("FileChooser")
		self.__language = None
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

	def __emit_export_signal(self, *args):
		try:
			filename = self.__chooser.get_filename().strip(" \t")
			if filename.endswith("/"): raise AttributeError
			self.__manager.emit("hide-export-window")
			self.__manager.emit("export-template-filename", filename)
			self.__manager.emit("get-selected-templates")
		except AttributeError:
			pass
		return False

	def __set_name_entry(self):
		self.__chooser.grab_focus()
		name = self.__language + "-template.xml"
		self.__chooser.set_current_name(name)
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__chooser.destroy()
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return

	def __show_cb(self, *args):
		self.__set_name_entry()
		return False

	def __export_button_clicked_cb(self, *args):
		self.__emit_export_signal()
		return False

	def __language_selected_cb(self, manager, language):
		self.__language = language
		return False
