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
This module documents a class that implements a treeview for the
document browser.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2006 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class TreeView(object):
	"""
	This class creates a treeview for the bookmark browser.
	"""

	def __init__(self, editor, manager):
		"""
		Intialize an instance of this class.

		@param self: Reference to the BrowserTreeView instance.
		@type self: A BrowserTreeView object.

		@param manager: Reference to the BookmarkManager instance.
		@type manager: A BookmarkManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(editor, manager)
		self.__set_properties()
		self.__signal_id_1 = self.__manager.connect("destroy", self.__destroy_cb)
		self.__signal_id_2 = self.__manager.connect("update", self.__update_cb)
		self.__signal_id_3 = self.__treeview.connect("row-activated", self.__row_activated_cb)
		self.__signal_id_4 = self.__treeview.connect("key-press-event", self.__key_press_event_cb)
		self.__populate_model()
		self.__treeview.set_property("sensitive", True)

	def __init_attributes(self, editor, manager):
		"""
		Initialize data attributes.

		@param self: Reference to the BrowserTreeView instance.
		@type self: A BrowserTreeView object.

		@param manager: Reference to the BookmarkManager instance.
		@type manager: A BookmarkManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__manager = manager
		self.__editor = editor
		self.__treeview = manager.glade.get_widget("TreeView")
		self.__uri_list = []
		self.__model = self.__create_model()
		self.__name_renderer = self.__create_renderer()
		self.__type_renderer = self.__create_renderer()
		self.__path_renderer = self.__create_renderer()
		from i18n import msg0003, msg0004, msg0005
		self.__name_column = self.__create_column(msg0004, self.__name_renderer, 0, False, True)
		self.__type_column = self.__create_column(msg0003, self.__type_renderer, 1, False, True)
		self.__path_column = self.__create_column(msg0005, self.__path_renderer, 2, False, True)
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		return

	def __set_properties(self):
		"""
		Define the treeview's properties.

		@param self: Reference to the BrowserTreeView instance.
		@type self: A BrowserTreeView object.
		"""
		self.__treeview.set_property("model", self.__model)
		self.__treeview.set_property("rules-hint", True)
		self.__treeview.set_property("search-column", 0)
		self.__treeview.set_property("headers-clickable", True)
		self.__treeview.append_column(self.__name_column)
		self.__treeview.append_column(self.__type_column)
		self.__treeview.append_column(self.__path_column)
		self.__name_column.clicked()
		return

	def __create_model(self):
		"""
		Create model for the treeview.

		@param self: Reference to the BrowserTreeView instance.
		@type self: An BrowserTreeView object.

		@return: Return a model for the treeview.
		@rtype: A gtk.ListStore object.
		"""
		# The model has four columns. One for the file type.
		# Another for the file name. Yet another for the full path name.
		# And the last for the file URI. Only the firt tree columns are
		# visible to users.
		from gtk import ListStore
		model = ListStore(str, str, str, str)
		return model

	def __create_renderer(self):
		"""
		Create the renderer for the treeview's columns.

		@param self: Reference to the BrowserTreeView instance.
		@type self: A BrowserTreeView object.

		@return: A renderer for treeview's columns.
		@rtype: A gtk.CellRendererText object.
		"""
		from gtk import CellRendererText
		renderer = CellRendererText()
		return renderer

	def __create_column(self, title, renderer, text=0, expand=False, indicator=False):
		"""
		Create column for the treeview.

		@param self: Reference to the BrowserTreeView instance.
		@type self: A BrowserTreeView object.

		@return: A column for the treeview.
		@rtype: A gtk.TreeViewColumn object.
		"""
		from gtk import TREE_VIEW_COLUMN_AUTOSIZE, SORT_DESCENDING
		from gtk import TreeViewColumn
		column = TreeViewColumn(title, renderer, text=text)
		column.set_expand(expand)
		column.set_sizing(TREE_VIEW_COLUMN_AUTOSIZE)
		column.set_sort_indicator(indicator)
		column.set_sort_order(SORT_DESCENDING)
		column.set_sort_column_id(text)
		return column

	def __destroy_cb(self, manager):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the BrowserTreeView instance.
		@type self: A BrowserTreeView object.

		@param manager: Reference to the BookmarkManager instance.
		@type manager: A BookmarkManager object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self.__manager)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__manager)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__treeview)
		self.__treeview.destroy()
		del self
		self = None
		return

	def __update_cb(self, manager):
		"""
		Handles callback when the "update" signal is emitted.

		@param self: Reference to the BrowserTreeView instance.
		@type self: A BrowserTreeView object.

		@param manager: Reference to the BookmarkManager instance.
		@type manager: A BookmarkManager object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__populate_model, priority=PRIORITY_LOW)
		self.__manager.emit("show-window")
		return False

	def __populate_model(self):
		"""
		Populate the model.

		@param self: Reference to the BrowserTreeView instance.
		@type self: A BrowserTreeView object.
		"""
		uris = self.__editor.instance_manager.get_uris()
		if not (uris):
			from i18n import msg0006
			self.__editor.feedback.update_status_message(msg0006, "warning")
			return	False
		uris.sort()
		self.__uri_list.sort()
		if uris == self.__uri_list: return
		self.__treeview.set_property("sensitive", False)
		self.__uri_list = uris
		self.__treeview.set_model(None)
		self.__model.clear()
		for uri in self.__uri_list:
			file_type, filename, pathname, fileuri= self.__process_uri(uri)
			self.__model.append([filename, file_type, pathname, fileuri])
		self.__treeview.set_model(self.__model)
		self.__editor.select_row(self.__treeview)
		self.__treeview.set_property("sensitive", True)
		self.__treeview.grab_focus()
		return

	def __process_uri(self, uri):
		"""
		Split the uri into type, name and pathname.

		@param self: Reference to the BrowserTreeView instance.
		@type self: A BrowserTreeView object.

		@param uri: Reference to a document.
		@type uri: A String object.
		"""
		value = ("", "", "", "")
		language = self.__editor.language
		if language:
			file_type = language.get_name()
		else:
			file_type = "Plain Text"
		from gnomevfs import URI, format_uri_for_display
		uri_object = URI(format_uri_for_display(uri))
		filename = uri_object.short_name
		pathname = uri_object.path.replace(self.__editor.home_folder, "~")
		fileuri = uri
		return file_type, filename, pathname, fileuri

	def __row_activated_cb(self, treeview, path, column):
		"""
		Handles callback when the "row-activated" signal is emitted.

		@param treeview: The bookmark browser's treeview.
		@type treeview: A BookmarkBrowserView object.

		@param path: A row in a treeview.
		@type path: A row object.

		@param column: A column in a treeview.
		@type column: A gtk.TreeViewColumn object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		iterator = self.__model.get_iter(path)
		uri = self.__model.get_value(iterator, 3)
		self.__manager.emit("hide-window")
		self.__editor.instance_manager.focus_file(uri)
		return True

	def __key_press_event_cb(self, treeview, event):
		from gtk import keysyms
		if event.keyval != keysyms.Delete: return False
		selection = treeview.get_selection()
		model, iterator = selection.get_selected()
		if not iterator: return False
		uri = model.get_value(iterator, 3)
		model.remove(iterator)
		self.__editor.select_row(self.__treeview)
		self.__editor.instance_manager.close_files([uri])
		return False
