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
This module documents a class that creates a treeview for the color
editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import TreeView

class ColorEditorTreeView(TreeView):
	"""
	This class creates the treeview for the color editor. It defines
	the default behavior and property of the color editor.
	"""

	def __init__(self, manager, editor):
		"""
		Initialize the treeview.

		@param self: Reference to the ColorEditorTreeView instance.
		@type self: A ColorEditorTreeView object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		TreeView.__init__(self)
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__signal_id_1 = self.__manager.connect("populate", self.__populate_cb)
		self.__signal_id_2 = self.__editor.connect("loaded-document", self.__reset_flag)
		self.__signal_id_3 = self.__editor.connect("renamed-document", self.__reset_flag)
		self.__signal_id_4 = self.__manager.connect("destroy", self.__destroy_cb)
		from thread import start_new_thread
		start_new_thread(self.__populate_model, ())
		#self.__populate_model()
		try:
			from psyco import bind
			bind(self.__populate_model)
			bind(self.__fill_language_and_elements)
			bind(self.__fill_elements)
		except ImportError:
			pass

	def __init_attributes(self, manager, editor):
		"""
		Initialize the treeview's data attributes.

		@param self: Reference to the ColorEditorTreeView instance.
		@type self: A ColorEditorTreeView object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__is_first_map = True
		self.__manager = manager
		self.__client = editor.gconf_client
		from gtksourceview import SourceLanguagesManager
		self.__language_list = SourceLanguagesManager().get_available_languages()
		self.__model = self.__create_model()
		self.__renderer = self.__create_renderer()
		self.__column = self.__create_column()
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		self.__signal_id_4 = None
		return

	def __set_properties(self):
		"""
		Defines the default property and behavior of the editor.

		@param self: Reference to the ColorEditorTreeView instance.
		@type self: A ColorEditorTreeView object.
		"""
		self.append_column(self.__column)
		self.set_model(self.__model)
		self.columns_autosize()
		self.set_enable_search(True)
		self.set_search_column(0)
		self.set_property("rules-hint", True)
		self.__column.clicked()
		return

	def __create_model(self):
		"""
		Create the model for the treeview.

		@param self: Reference to the ColorEditorTreeView instance.
		@type self: A ColorEditorTreeView object.

		@return: A model containing language information.
		@rtype: A gtk.ListStore object.
		"""
		# The model has three columns. One for the language name.
		# Another for the language id. And the last for the
		# gtksourceview.SourceLanguage object. Only the language name is
		# visible to users (i.e is displayed in the treeview).
		from gtk import TreeStore
		from gobject import TYPE_OBJECT
		model = TreeStore(str, str, TYPE_OBJECT)
		return model

	def __populate_model(self):
		"""
		Populate the treeview with language information.

		@param self: Reference to the ColorEditorTreeView instance.
		@type self: A ColorEditorTreeView object.
		"""
		self.__treeview.set_model(None)
		map(self.__fill_language_and_elements, self.__language_list)
		self.__treeview.set_model(self.__model)
		return

	def __fill_language_and_elements(self, language):
		"""
		Populate a row in the treeview with a language name and
		elements associated with the language.
		"""
		parent_iter = self.__model.append(None)
		self.__model.set(parent_iter, 0, language.get_name())
		self.__model.set(parent_iter, 1, language.get_id())
		self.__model.set(parent_iter, 2, language)
		fill_elements = lambda x: self.__fill_elements(parent_iter, language, x)
		# Populate sub-row with elements associated with this language.
		map(fill_elements, language.get_tags())
		return

	def __fill_elements(self, parent_iter, language, tag):
		"""
		Populate sub-rows of a language with associated elements.
		"""
		child_iter = self.__model.append(parent_iter)
		self.__model.set(child_iter, 0, tag.get_property("name"))
		self.__model.set(child_iter, 1, tag.get_id())
		self.__model.set(child_iter, 2, language)
		return

	def __create_renderer(self):
		"""
		Create the renderer for the treeview.

		@param self: Reference to the ColorEditorTreeView instance.
		@type self: A ColorEditorTreeView object.

		@return: A renderer for the treeview.
		@rtype: A gtk.Renderer object.
		"""
		from gtk import CellRendererText
		renderer = CellRendererText()
		return renderer

	def __create_column(self):
		"""
		Create the column for the treeview.

		@param self: Reference to the ColorEditorTreeView instance.
		@type self: A ColorEditorTreeView object.

		@return: A column for the language view.
		@rtype: A gtk.TreeViewColumn object.
		"""
		from gtk import TreeViewColumn, TREE_VIEW_COLUMN_GROW_ONLY
		from gtk import SORT_ASCENDING
		from i18n import msg0012
		column = TreeViewColumn(msg0012, self.__renderer, text=0)
		column.set_property("expand", False)
		column.set_property("sizing", TREE_VIEW_COLUMN_GROW_ONLY)
		column.set_property("clickable", True)
		column.set_sort_column_id(0)
		column.set_property("sort-indicator", True)
		column.set_property("sort-order", SORT_ASCENDING)
		return column

	def __populate_cb(self, manager):
		"""
		Handles callback when the "show-dialog" signal is emitted.

		@param self: Reference to the ColorEditorTreeView instance.
		@type self: A ColorEditorTreeView object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param dialog: The dialog being shown.
		@type dialog: A gtk.Dialog/Window object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		self.set_property("sensitive", False)
		from operator import truth
		if truth(self.__is_first_map):
			if truth(self.__editor.uri):
				language = self.__editor.language
				if truth(language):
					self.__select_language(language)
				else:
					column = self.get_column(0)
					self.set_cursor_on_cell(0, column)
					self.scroll_to_cell(0, column, True, 0.5)
			else:
				column = self.get_column(0)
				self.set_cursor_on_cell(0, column)
				self.scroll_to_cell(0, column, True, 0.5)
		self.__is_first_map = False
		self.set_property("sensitive", True)
		self.grab_focus()
		return False

	def __select_language(self, language):
		"""
		Select a language row in the treeview.

		@param self: Reference to the ColorEditorTreeView instance.
		@type self: A ColorEditorTreeView object.
		"""
		from operator import truth, ne
		model = self.get_model()
		iterator = model.get_iter_first()
		while ne(model.get_value(iterator, 1), language.get_id()):
			iterator = model.iter_next(iterator)
		if truth(iterator):
			path = model.get_path(iterator)
			column = self.get_column(0)
			self.expand_row(path, True)
			self.set_cursor_on_cell(path, column)
			self.scroll_to_cell(path, column, True, 0.3)
		else:
			column = self.get_column(0)
			self.set_cursor_on_cell(0, column)
			self.scroll_to_cell(0, column, True, 0.5)
		return

	def __reset_flag(self, *args):
		self.__is_first_map = True
		return

	def __destroy_cb(self, manager):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the ColorEditorTreeView instance.
		@type self: A ColorEditorTreeView object.

		@param manager: Reference to the ColorEditorManager instance.
		@type manager: A ColorEditorManager object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self.__manager)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__manager)
		self.__model.clear()
		self.destroy()
		del self
		self = None
		return

########################################################################
	def get_selected_path(self):
		"""
		Get the selected path or None.

		@param self: Reference to the ColorEditorTreeView instance.
		@type self: A ColorEditorTreeView object.

		@return: Return the selected path or None
		@rtype: A Tuple object.
		"""
		self.force_selection()
		iterator = self.get_selected_iter()
		if iterator:
			path = self.__model.get_path(iterator)
			return path
		path = None
		return path

	def get_selected_iter(self):
		"""
		Get the selected iterator or None.

		@param self: Reference to the ColorEditorTreeView instance.
		@type self: A ColorEditorTreeView object.

		@return: Return the selected iterator or None
		@rtype: A gtk.TreeIter object.
		"""
		self.force_selection()
		selection = self.get_selection()
		model, iterator = selection.get_selected()
		if iterator: return iterator
		iterator = None
		return iterator

	def get_language(self, column=2):
		"""
		Get the language.

		@param self: Reference to the ColorEditorTreeView instance.
		@type self: A ColorEditorTreeView object.

		@return: Return the selected iterator or None
		@rtype: A gtk.TreeIter object.
		"""
		language = None
		if self.is_parent():
			self.force_selection()
			iterator = self.get_selected_iter()
			if iterator:
				language = self.__model.get_value(iterator, column)
		else:
			self.force_selection()
			child_iterator = self.get_selected_iter()
			if child_iterator:
				iterator = self.__model.iter_parent(child_iterator)
				if iterator:
					language = self.__model.get_value(iterator, column)
		return language

	def get_element(self, column=1):
		"""
		Get the selected element.

		@param self: Reference to the ColorEditorTreeView instance.
		@type self: A ColorEditorTreeView object.

		@return: Return the selected iterator or None
		@rtype: A gtk.TreeIter object.
		"""
		element = None
		if self.is_parent() is False:
			self.force_selection()
			iterator = self.get_selected_iter()
			if iterator:
				element = self.__model.get_value(iterator, column)
		return element

	def is_parent(self):
		"""
		Return whether or not the selected row is a parent or not.

		@param self: Reference to the ColorEditorTreeView instance.
		@type self: A ColorEditorTreeView object.

		@return: True if row is a parent.
		@rtype: A Boolean object.
		"""
		value = False
		self.force_selection()
		iterator = self.get_selected_iter()
		if iterator:
			if self.__model.iter_has_child(iterator):
				value = True
		return value

	def force_selection(self):
		"""
		Force a row to be selected.

		@param self: Reference to the ColorEditorTreeView instance.
		@type self: A ColorEditorTreeView object.
		"""
		path, column = self.get_cursor()
		selection = self.get_selection()
		selection.select_path(path)
		return
