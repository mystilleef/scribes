# -*- coding: utf-8 -*-
# Copyright © 2007 Lateef Alabi-Oki
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
This module documents a class that implements the behavior for the
template editor's description treeview.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class TreeView(object):
	"""
	This class implements the behavior for the description treeview.
	"""

	def __init__(self, manager, editor):
		"""
		Initialize object.

		@param self: Reference to the DescriptionTreeView instance.
		@type self: A DescriptionTreeView object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("language-selected", self.__language_selected_cb)
		self.__sigid3 = self.__treeview.connect("cursor-changed", self.__cursor_changed_cb)
		self.__sigid4 = manager.connect_after("select-description-view", self.__select_description_view_cb)

	def __init_attributes(self, manager, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the DescriptionTreeView instance.
		@type self: A DescriptionTreeView object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__manager = manager
		self.__editor = editor
		self.__language = None
		self.__model = self.__create_model()
		self.__name_renderer = self.__create_renderer()
		self.__name_column = self.__create_name_column()
		self.__description_renderer = self.__create_renderer()
		self.__description_column = self.__create_description_column()
		self.__treeview = manager.glade.get_widget("TemplateTreeView")
		return

	def __set_properties(self):
		"""
		Set the description view's default properties.

		@param self: Reference to the TemplateEditorLanguageView instance.
		@type self: A TemplateEditorLanguageView object.
		"""
		from gtk import SELECTION_MULTIPLE
		selection = self.__treeview.get_selection()
		selection.set_mode(SELECTION_MULTIPLE)
		from gtk.gdk import BUTTON1_MASK, ACTION_COPY, ACTION_DEFAULT
		targets = [("text/plain", 0, 123), ("STRING", 0, 123)]
		self.__treeview.enable_model_drag_source(BUTTON1_MASK, targets, ACTION_COPY|ACTION_DEFAULT)
		self.__treeview.set_property("model", self.__model)
		self.__treeview.append_column(self.__name_column)
		self.__treeview.append_column(self.__description_column)
		self.__treeview.notify("sensitive")
		self.__name_column.clicked()
		return

	def __create_model(self):
		"""
		Create the model for the template editor's description view.

		@param self: Reference to the TreeView instance.
		@type self: A TreeView object.

		@return: A model for the description view.
		@rtype: A gtk.ListStore object.
		"""
		from gtk import ListStore
		model = ListStore(str, str, str)
		return model

	def __create_renderer(self):
		"""
		Create the renderer for the description view's column

		@param self: Reference to the TreeView instance.
		@type self: A TreeView object.
		"""
		from gtk import CellRendererText
		renderer = CellRendererText()
		return renderer

	def __create_name_column(self):
		"""
		Create the column for the template editor's description view.

		@param self: Reference to the TreeView instance.
		@type self: A TreeView object.

		@return: A column for the description view.
		@rtype: A gtk.TreeViewColumn object.
		"""
		from gtk import TreeViewColumn, TREE_VIEW_COLUMN_GROW_ONLY
		from gtk import SORT_ASCENDING
		from i18n import msg0002
		column = TreeViewColumn(msg0002, self.__name_renderer, text=0)
		column.set_property("expand", False)
		column.set_property("sizing", TREE_VIEW_COLUMN_GROW_ONLY)
		column.set_property("clickable", True)
		column.set_sort_column_id(0)
		column.set_property("sort-indicator", True)
		column.set_property("sort-order", SORT_ASCENDING)
		return column

	def __create_description_column(self):
		"""
		Create the column for the template editor's description view.

		@param self: Reference to the TreeView instance.
		@type self: A TreeView object.

		@return: A column for the description view.
		@rtype: A gtk.TreeViewColumn object.
		"""
		from gtk import TreeViewColumn, TREE_VIEW_COLUMN_GROW_ONLY
		from gtk import SORT_ASCENDING
		from i18n import msg0003
		column = TreeViewColumn(msg0003, self.__description_renderer, text=1)
		column.set_property("expand", True)
		column.set_property("sizing", TREE_VIEW_COLUMN_GROW_ONLY)
		return column

	def __populate_model(self, data):
		"""
		Populate the treeview.

		@param self: Reference to the DescriptionTreeView instance.
		@type self: A DescriptionTreeView object.

		@param language: An object representing a language.
		@type language: A gtksourceview.SourceLanguage object.
		"""
		self.__model.clear()
		self.__treeview.set_property("sensitive", False)
		self.__manager.emit("description-view-sensitivity", False)
		if not data: return False
		self.__treeview.set_model(None)
		for info in data:
			self.__model.append([info[0], info[1], info[3]])
		self.__treeview.set_model(self.__model)
		self.__treeview.set_property("sensitive", True)
		self.__manager.emit("description-view-sensitivity", True)
		self.__select_row()
		return False

	def __select_row(self):
		"""
		Select the first row in the treeview.

		@param self: Reference to the DescriptionTreeView instance.
		@type self: A DescriptionTreeView object.
		"""
		try:
			selection = self.__treeview.get_selection()
			selection.select_path(0)
			iterator = self.__model.get_iter_first()
			path = self.__model.get_path(iterator)
			self.__treeview.scroll_to_cell(path, self.__treeview.get_column(0), True, 0.5, 0.0)
			self.__treeview.set_cursor(path, self.__treeview.get_column(0))
			self.__treeview.columns_autosize()
#			self.__treeview.grab_focus()
		except TypeError:
			pass
		return

	def __process_language(self, language):
		self.__language = language
		from Metadata import get_template_data
		data = get_template_data(language)
		self.__populate_model(data)
		return False

	def __destroy_cb(self, manager):
		"""
		Destroy instance of this class.

		@param self: Reference to the DescriptionTreeView instance.
		@type self: A DescriptionTreeView object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.
		"""
		self.__editor.disconnect_signal(self.__sigid1, manager)
		self.__editor.disconnect_signal(self.__sigid2, manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__treeview)
		self.__editor.disconnect_signal(self.__sigid4, manager)
		self.__treeview.destroy()
		del self
		self = None
		return

	def __language_selected_cb(self, manager, language):
		"""
		Handles callback when the "language-selected" signal is emitted.

		@param self: Reference to the DescriptionTreeView instance.
		@type self: A DescriptionTreeView object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param language: An object representing a language object.
		@type language: A gtksourceview.SourceLanguage object.
		"""
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__id)
		except AttributeError:
			pass
		finally:
			self.__id = idle_add(self.__process_language, language, priority=3000)
		return

	def __cursor_changed_cb(self, treeview):
		"""
		Handles callback when the "cursor-changed" signal is emitted.

		@param self: Reference to the DescriptionTreeView instance.
		@type self: A DescriptionTreeView object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		selection = treeview.get_selection()
		model, paths = selection.get_selected_rows()
		if not paths: return
		iterator = model.get_iter(paths[-1])
		database_key = model.get_value(iterator, 2)
		self.__manager.emit("template-selected", (self.__language, database_key))
		return

	def __select_description_view_cb(self, *args):
		if self.__treeview.get_property("sensitive") is False: return False
		self.__treeview.grab_focus()
		return False
