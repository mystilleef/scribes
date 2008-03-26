# -*- coding: utf-8 -*-
# Copyright © 2005 Lateef Alabi-Oki
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
This module documents a class that implements a combobox to select where
"unsaved" documents will be placed. The combobox is part of the
Advanced Configuration Window.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class ComboBox(object):
	"""
	This class implements the default properties and behavior of the
	"unsaved documents folder" combobox. The combobox is used to choose
	where "unsaved documents" will be placed.
	"""

	def __init__(self, editor, manager):
		"""
		Initialize object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param manager: Reference to manager object.
		@type manager: A Manager object.
		"""
		self.__init_attributes(editor, manager)
		self.__set_properties()
		self.__sig_id1 = self.__combobox.connect("changed", self.__changed_cb)
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__populate_model, priority=PRIORITY_LOW)

	def __init_attributes(self, editor, manager):
		"""
		Initialize attributes.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param manager: Reference to manager object.
		@type manager: A Manager object.
		"""
		self.__editor = editor
		self.__manager = manager
		self.__combobox = manager.glade.get_widget("ComboBox")
		self.__model = self.__create_model()
		return

	def __set_properties(self):
		from gtk import CellRendererText, CellRendererPixbuf
		text_renderer = CellRendererText()
		pixbuf_renderer = CellRendererPixbuf()
		self.__combobox.pack_start(pixbuf_renderer, False)
		self.__combobox.pack_start(text_renderer, True)
		self.__combobox.set_attributes(text_renderer, text=1)
		self.__combobox.set_attributes(pixbuf_renderer, icon_name=0)
		sepfunc = lambda model, iter_: True if model.get_value(iter_, 1) == "Separator" else False
		self.__combobox.set_row_separator_func(sepfunc)
		return

	def __create_model(self):
		"""
		Create model for the combobox.

		@param self: Reference to the ComboBox instance.
		@type self: A ComboBox object.

		@return: A model for the combobox
		@rtype: A gtk.ListStore object.
		"""
		from gtk import ListStore
		model = ListStore(str, str)
		return model

	def __populate_model(self):
		"""
		Populate the model and thus the combobox.

		@param self: Reference to the ComboBox instance.
		@type self: A ComboBox object.
		"""
		self.__combobox.set_property("sensitive", False)
		self.__combobox.handler_block(self.__sig_id1)
		self.__combobox.set_model(None)
		from UnsavedFolderMetadata import get_value
		uri = get_value()
		icon_name, folder_name = self.__format_uri_for_display(uri)
		self.__model.clear()
		self.__model.append([icon_name, folder_name])
		self.__model.append(["empty", "Separator"])
		self.__model.append(["folder", "other..."])
		self.__combobox.set_model(self.__model)
		self.__combobox.set_active(0)
		self.__combobox.handler_unblock(self.__sig_id1)
		self.__combobox.set_property("sensitive", True)
		return False

	def __format_uri_for_display(self, uri):
		from gnomevfs import get_local_path_from_uri
		local_path = get_local_path_from_uri(uri)
		from os.path import basename
		folder_name = basename(local_path)
		icon_name = "desktop" if folder_name == "Desktop" else "folder"
		return icon_name, folder_name

	def __changed_cb(self, *args):
		iterator = self.__combobox.get_active_iter()
		active_text = self.__model.get_value(iterator, 1)
		self.__combobox.handler_block(self.__sig_id1)
		self.__combobox.set_active(0)
		self.__combobox.handler_unblock(self.__sig_id1)
		if active_text != "other...": return
		print "show file chooser"
		return
