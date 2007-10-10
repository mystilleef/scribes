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
This module documents a class that defines the behavior of the template
editor's language treeview.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class TemplateLanguageTreeView(object):
	"""
	This class creates an object that defines the behavior of the
	template editor's language treeview.
	"""

	def __init__(self, manager, editor):
		"""
		Initialize object.

		@param self: Reference to the TemplateLanguageTreeView instance.
		@type self: A TemplateLanguageTreeView object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__populate_model()
		self.__select_language()
		self.__signal_id_1 = manager.connect("destroy", self.__destroy_cb)
		self.__signal_id_2 = self.__editor.connect("loaded-document", self.__generic_cb)
		self.__signal_id_3 = self.__editor.connect("renamed-document", self.__generic_cb)
		self.__signal_id_4 = manager.connect("show", self.__show_cb)
		self.__signal_id_5 = self.__treeview.connect("cursor-changed", self.__cursor_changed_cb)
		self.__signal_id_6 = manager.connect("imported-language", self.__imported_language_cb)
		self.__signal_id_7 = self.__treeview.connect("drag-data-get", self.__drag_data_get_cb)
		self.__signal_id_8 = self.__treeview.connect("drag-data-received", self.__drag_data_received_cb)

	def __init_attributes(self, manager, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the TemplateLanguageTreeView instance.
		@type self: A TemplateLanguageTreeView object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__manager = manager
		self.__editor = editor
		self.__treeview = manager.glade.get_widget("LanguageTreeView")
		self.__is_first_time = True
		self.__model = self.__create_model()
		self.__renderer = self.__create_renderer()
		self.__column = self.__create_column()
		from gtksourceview import SourceLanguagesManager
		language_list = SourceLanguagesManager().get_available_languages()
		self.__languages = [name.get_id() for name in language_list]
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		self.__signal_id_4 = self.__signal_id_5 = self.__signal_id_6 = None
		self.__signal_id_7 = self.__signal_id_8 = None
		return

	def __set_properties(self):
		"""
		Set the language view's default properties.

		@param self: Reference to the TemplateEditorLanguageView instance.
		@type self: A TemplateEditorLanguageView object.
		"""
		from gtk.gdk import ACTION_DEFAULT, BUTTON1_MASK
		from gtk import TARGET_SAME_APP
		self.__treeview.enable_model_drag_source(BUTTON1_MASK, [("STRING", 0, 123)], ACTION_DEFAULT)
		self.__treeview.enable_model_drag_dest([("STRING", TARGET_SAME_APP, 124)], ACTION_DEFAULT)
#		self.__treeview.set_property("rules-hint", True)
#		self.__treeview.set_property("search-column", 0)
#		self.__treeview.set_property("headers-clickable", True)
		self.__treeview.append_column(self.__column)
		self.__treeview.set_model(self.__model)
		self.__column.clicked()
		return

	def __create_model(self):
		"""
		Create the model for the template editor's language view.

		@param self: Reference to the TemplateEditorLanguageView instance.
		@type self: A TemplateEditorLanguageView object.

		@return: A model for the language view.
		@rtype: A gtk.ListStore object.
		"""
		from gtk import ListStore
		model = ListStore(str, str)
		return model

	def __create_column(self):
		"""
		Create the column for the template editor's language view.

		@param self: Reference to the TemplateEditorLanguageView instance.
		@type self: A TemplateEditorLanguageView object.

		@return: A column for the language view.
		@rtype: A gtk.TreeViewColumn object.
		"""
		from gtk import TreeViewColumn, TREE_VIEW_COLUMN_GROW_ONLY
		from gtk import SORT_ASCENDING
		from i18n import msg0001
		column = TreeViewColumn(msg0001, self.__renderer, text=0)
		column.set_property("expand", False)
		column.set_property("sizing", TREE_VIEW_COLUMN_GROW_ONLY)
		column.set_property("clickable", True)
		column.set_sort_column_id(0)
		column.set_property("sort-indicator", True)
		column.set_property("sort-order", SORT_ASCENDING)
		return column

	def __create_renderer(self):
		"""
		Create the renderer for the language view's column

		@param self: Reference to the TemplateEditorLanguageView instance.
		@type self: A TemplateEditorLanguageView object.

		@return: A renderer for the language view.
		@rtype: A gtk.CellRendererText object.
		"""
		from gtk import CellRendererText
		renderer = CellRendererText()
		return renderer

	def __populate_model(self):
		"""
		Populate the language view's model.

		@param self: Reference to the TemplateLanguageTreeView instance.
		@type self: A TemplateLanguageTreeView object.
		"""
		from gtksourceview import SourceLanguagesManager
		language_list = SourceLanguagesManager().get_available_languages()
		language_names = [(name.get_name(), name.get_id()) for name in language_list]
		self.__model.append(["General", "General"])
		for name, id in language_names:
			self.__model.append([name, id])
		return

	def __select_language(self, language=None):
		"""
		Select a row corresponding to the language in the tree view.

		@param self: Reference to the TemplateLanguageTreeView instance.
		@type self: A TemplateLanguageTreeView object.
		"""
		from operator import eq, not_
		if not_(language):
			language_id = self.__get_language()
		else:
			language_id = language
		model = self.__model
		iterator = model.get_iter_first()
		language = model.get_value(iterator, 1)
		if eq(language, language_id):
			selection = self.__treeview.get_selection()
			selection.select_iter(iterator)
			path = model.get_path(iterator)
			self.__treeview.scroll_to_cell(path, self.__treeview.get_column(0), True, 0.5, 0.0)
		else:
			while True:
				iterator = model.iter_next(iterator)
				if iterator:
					language = model.get_value(iterator, 1)
					if eq(language, language_id):
						selection = self.__treeview.get_selection()
						selection.select_iter(iterator)
						path = model.get_path(iterator)
						self.__treeview.scroll_to_cell(path, self.__treeview.get_column(0), True, 0.5, 0.0)
						break
				else:
					break
		return

	def __get_language(self):
		"""
		Get the current language of the file in the text editor.

		@param self: Reference to the TemplateLanguageTreeView instance.
		@type self: A TemplateLanguageTreeView object.

		@return: Return a language or "General"
		@rtype: A String object.
		"""
		language = self.__editor.language
		from operator import not_
		if not_(language): return "General"
		return language.get_id()

	def __get_templates(self, language):
		templates = []
		from Metadata import open_template_database
		from Metadata import close_template_database
		from operator import eq, not_, ne
		same_prefix = lambda x: x.startswith(language)
		remove_language = lambda x: ne(x, language)
		similar_prefix = filter(remove_language, filter(same_prefix, self.__languages))
		database = open_template_database()
		for key in database.keys():
			skip = False
			for value in similar_prefix:
				if key.startswith(value):
					skip = True
					break
			if skip: continue
			if key.startswith(language):
				boolean = True
				trigger = key.replace(language, "")
				description = database[key][0]
				template = database[key][1]
				templates.append((language, trigger, description, template))
		close_template_database(database)
		return templates

	def __get_drop_row(self, path):
		"""
		Get the language of the row drag and drop occurred.

		@param self: Reference to the TemplateEditorLanguageView instance.
		@type self: A TemplateEditorLanguageView object.

		@param path: The row a drag and drop occurred.
		@type path: A Tuple object.

		@return: The language identifier of the row a drag and drop occurred.
		@rtype: A String object.
		"""
		model = self.__treeview.get_model()
		iterator = model.get_iter(path)
		language_id = model.get_value(iterator, 1)
		return language_id

	def __create_new_templates(self, templates, language):
		"""
		Convert old template information to new one.

		@param self: Reference to the LanguageTreeView instance.
		@type self: A LanguageTreeView object.

		@param templates: Reference to the templates information.
		@type templates: A List object.

		@param language: Language category to convert templates to.
		@type language: A String object.
		"""
		def new_template(data):
			key, description, template, old_language = data
			return language, key[len(language):], description, template
		templates = map(new_template, templates)
		return templates

	def __destroy_cb(self, manager):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the TemplateLanguageTreeView instance.
		@type self: A TemplateLanguageTreeView object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, manager)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_4, manager)
		self.__editor.disconnect_signal(self.__signal_id_5, self.__treeview)
		self.__editor.disconnect_signal(self.__signal_id_6, manager)
		self.__editor.disconnect_signal(self.__signal_id_7, self.__treeview)
		self.__editor.disconnect_signal(self.__signal_id_8, self.__treeview)
		self.__model.clear()
		self.__treeview.destroy()
		self = None
		del self
		return

	def __cursor_changed_cb(self, *args):
		"""
		Handles callback when the "cursor-changed" signal is emitted.

		@param self: Reference to the TemplateLanguageTreeView instance.
		@type self: A TemplateLanguageTreeView object.
		"""
		try:
			selection = self.__treeview.get_selection()
			model, iterator = selection.get_selected()
			language_id = model.get_value(iterator, 1)
			self.__manager.emit("language-selected", language_id)
		except TypeError:
			pass
		return

	def __generic_cb(self, *args):
		"""
		A generic callback handler to select a language.

		@param self: Reference to the TemplateLanguageTreeView instance.
		@type self: A TemplateLanguageTreeView object.
		"""
		self.__select_language()
		return

	def __show_cb(self, *args):
		"""
		Handles callback when the "show" signal is emitted.

		@param self: Reference to the TemplateLanguageTreeView instance.
		@type self: A TemplateLanguageTreeView object.
		"""
		self.__treeview.grab_focus()
		self.__editor.select_row(self.__treeview)
		return

	def __imported_language_cb(self, manager, language):
		"""
		Handles callback when the "imported-language" signal is emitted.

		@param self: Reference to the TemplateLanguageTreeView instance.
		@type self: A TemplateLanguageTreeView object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param language: A language category
		@type language: A String object.
		"""
		self.__select_language(language)
		# No error occurred. I'm just using the signal to make the
		# template editor window sensitive.
		manager.emit("import-error")
		self.__editor.select_row(self.__treeview)
		self.__treeview.grab_focus()
		return

	def __drag_data_get_cb(self, treeview, context, data, info, time):
		try:
			from Exceptions import NoDataError
			selection = treeview.get_selection()
			model, iterator = selection.get_selected()
			language_id = model.get_value(iterator, 1)
			templates = self.__get_templates(language_id)
			from operator import not_
			if not_(templates): raise NoDataError
			from WriteXMLTemplate import create_template_string
			string = create_template_string(templates)
			data.set(data.target, 8, string)
		except NoDataError:
			pass
		return True

	def __drag_data_received_cb(self, treeview, context, x, y, data, info, time):
		"""
		Handles callback when the "drag-data-received" signal is emitted.

		@param self: Reference to the TemplateLanguageTreeView instance.
		@type self: A TemplateLanguageTreeView object.

		@param treeview: Reference to the TemplateEditorLanguageView.
		@type treeview: A TemplateEditorLanguageView object.

		@param context: An object containing data about a drag selection.
		@type context: A gtk.DragContextData object.

		@param x: The x-cordinate of the drop.
		@type x: An Integer object.

		@param y: The y-cordinate of the drop.
		@type y: An Integer object.

		@param selection_data: Data representing the drag selection.
		@type selection_data: A gtk.SelectionData object.

		@param info: A unique identification for the text editor.
		@type info: An Integer object.

		@param time: The time the drop operation occurred.
		@type time: An Integer object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		try:
			from Exceptions import InvalidFileError, ValidationError
			from Exceptions import NoDataError
			path, position = treeview.get_dest_row_at_pos(x, y)
			from gtk import TREE_VIEW_DROP_BEFORE, TREE_VIEW_DROP_AFTER
			if position in [TREE_VIEW_DROP_BEFORE, TREE_VIEW_DROP_AFTER]: return True
			language_id = self.__get_drop_row(path)
			string = data.data
			from ReadXMLTemplate import get_template_from_string
			templates = get_template_from_string(string)
			from operator import not_
			if not_(templates): raise NoDataError
			new_templates = self.__create_new_templates(templates, language_id)
			from WriteXMLTemplate import create_template_string
			template_string = create_template_string(new_templates)
			from ImportTemplate import import_template_from_string
			templates = import_template_from_string(template_string)
			if not_(templates): raise NoDataError
			self.__manager.emit("imported-language", language_id)
		except InvalidFileError:
			from i18n import msg0014
			self.__editor.error_dialog.show_message(msg0014, parent_window=self.__dialog)
			self.__manager.emit("import-error")
		except ValidationError:
			from i18n import msg0014
			self.__editor.error_dialog.show_message(msg0014, parent_window=self.__dialog)
			self.__manager.emit("import-error")
		except NoDataError:
			from i18n import msg0015
			self.__editor.error_dialog.show_message(msg0015, parent_window=self.__dialog)
			self.__manager.emit("import-error")
		return True
