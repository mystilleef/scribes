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

class DescriptionTreeView(object):
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
		self.__signal_id_1 = manager.connect("destroy", self.__destroy_cb)
		self.__signal_id_2 = manager.connect("language-selected", self.__language_selected_cb)
		self.__signal_id_3 = manager.connect_after("show", self.__show_cb)
		self.__signal_id_4 = self.__treeview.connect("notify::sensitive", self.__sensitive_cb)
		self.__signal_id_5 = self.__treeview.connect("cursor-changed", self.__cursor_changed_cb)
		self.__signal_id_6 = manager.connect("remove-template", self.__remove_template_cb)
		self.__signal_id_7 = manager.connect("export-template", self.__export_template_cb)
		self.__signal_id_8 = manager.connect("trigger-selected", self.__trigger_selected_cb)
		self.__signal_id_9 = manager.connect_after("sensitive", self.__manager_sensitive_cb)
		self.__signal_id_10 = self.__treeview.connect("drag-data-get", self.__drag_data_get_cb)
		# Monitor database for changes.
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monitor_id = monitor_add(self.__database_uri, MONITOR_FILE, self.__database_changed_cb)

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
		self.__can_update = True
		self.__trigger = None
		self.__model = self.__create_model()
		self.__name_renderer = self.__create_renderer()
		self.__name_column = self.__create_name_column()
		self.__description_renderer = self.__create_renderer()
		self.__description_column = self.__create_description_column()
		self.__treeview = manager.glade.get_widget("DescriptionTreeView")
		from gtksourceview import SourceLanguagesManager
		language_list = SourceLanguagesManager().get_available_languages()
		self.__languages = [name.get_id() for name in language_list]
		# Path to the templates database.
		database_path = editor.metadata_folder + "templates.gdb"
		from gnomevfs import get_uri_from_local_path
		self.__database_uri = get_uri_from_local_path(database_path)
		self.__monitor_id = None
		self.__signal_id_1 = self.__signal_id_2 = None
		self.__signal_id_3 = self.__signal_id_4 = None
		self.__signal_id_5 = self.__signal_id_6 = None
		self.__signal_id_7 = self.__signal_id_8 = None
		self.__signal_id_9 = self.__signal_id_10 = None
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

		@param self: Reference to the TemplateEditorDescriptionView instance.
		@type self: A TemplateEditorDescriptionView object.

		@return: A model for the description view.
		@rtype: A gtk.ListStore object.
		"""
		from gtk import ListStore
		model = ListStore(str, str)
		return model

	def __create_renderer(self):
		"""
		Create the renderer for the description view's column

		@param self: Reference to the TemplateEditorDescriptionView instance.
		@type self: A TemplateEditorDescriptionView object.

		@return: A renderer for the description view.
		@rtype: A gtk.CellRendererText object.
		"""
		from gtk import CellRendererText
		renderer = CellRendererText()
		return renderer

	def __create_name_column(self):
		"""
		Create the column for the template editor's description view.

		@param self: Reference to the TemplateEditorDescriptionView instance.
		@type self: A TemplateEditorDescriptionView object.

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

		@param self: Reference to the TemplateEditorDescriptionView instance.
		@type self: A TemplateEditorDescriptionView object.

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

	def __populate_model(self, language):
		"""
		Populate the treeview.

		@param self: Reference to the DescriptionTreeView instance.
		@type self: A DescriptionTreeView object.

		@param language: An object representing a language.
		@type language: A gtksourceview.SourceLanguage object.
		"""
		boolean = False
		self.__treeview.set_property("sensitive", boolean)
		self.__model.clear()
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
				name = key.replace(language, "")
				description = database[key][0]
				self.__model.append([name, description])
		close_template_database(database)
		self.__treeview.set_property("sensitive", boolean)
		if not_(boolean): return
		self.__select_row()
		return

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
			self.__treeview.grab_focus()
		except TypeError:
			pass
		return

	def __select_new_row(self):
		selection = self.__treeview.get_selection()
		selection.unselect_all()
		if self.__trigger:
			model = self.__model
			iterator = model.get_iter_first()
			trigger = model.get_value(iterator, 0)
			from operator import eq, not_
			if eq(trigger, self.__trigger):
				selection.select_iter(iterator)
				path = model.get_path(iterator)
				self.__treeview.scroll_to_cell(path, self.__treeview.get_column(0), True, 0.5, 0.0)
				self.__treeview.set_cursor(path, self.__treeview.get_column(0))
			else:
				while True:
					iterator = model.iter_next(iterator)
					if not_(iterator):
						self.__select_row()
						break
					trigger = model.get_value(iterator, 0)
					if eq(trigger, self.__trigger):
						selection.select_iter(iterator)
						path = model.get_path(iterator)
						self.__treeview.scroll_to_cell(path, self.__treeview.get_column(0), True, 0.5, 0.0)
						self.__treeview.set_cursor(path, self.__treeview.get_column(0))
						break
		else:
			self.__select_row()
		self.__trigger = None
		self.__manager.emit("sensitive", True)
		self.__treeview.columns_autosize()
		self.__treeview.grab_focus()
		return

	def __check_permission(self, filename):
		"""
		Check whether or not the location can be written to.

		@param self: Reference to the DescriptionTreeView instance.
		@type self: A DescriptionTreeView object.

		@param filename: A string representing a file.
		@type filename: A String object.
		"""
		from os import access, F_OK, W_OK, path
		from Exceptions import ExportPermissionError
		folder = path.dirname(filename)
		if access(folder, F_OK) is False:
			raise ExportPermissionError
		if access(folder, W_OK) is False:
			raise ExportPermissionError
		return

	def __get_template_info(self):
		"""
		Get template information.

		@param self: Reference to the DescriptionTreeView instance.
		@type self: A DescriptionTreeView object.

		@return: A list of template information.
		@rtype: A List object.
		"""
		selection = self.__treeview.get_selection()
		model, paths = selection.get_selected_rows()
		from operator import not_
		from Exceptions import ExportSelectionError
		if not_(paths): raise ExportSelectionError
		get_trigger = lambda path: model.get_value(model.get_iter(path), 0)
		triggers = map(get_trigger, paths)
		from Metadata import open_template_database
		from Metadata import close_template_database
		database = open_template_database()
		get_template = lambda trigger: self.__get_template(trigger, database)
		templates = map(get_template, triggers)
		close_template_database(database)
		return templates

	def __get_template(self, trigger, database):
		return self.__language, trigger, database[self.__language+trigger][0], database[self.__language+trigger][1]

	def __destroy_cb(self, manager):
		"""
		Destroy instance of this class.

		@param self: Reference to the DescriptionTreeView instance.
		@type self: A DescriptionTreeView object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, manager)
		self.__editor.disconnect_signal(self.__signal_id_2, manager)
		self.__editor.disconnect_signal(self.__signal_id_3, manager)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__treeview)
		self.__editor.disconnect_signal(self.__signal_id_5, self.__treeview)
		self.__editor.disconnect_signal(self.__signal_id_6, manager)
		self.__editor.disconnect_signal(self.__signal_id_7, manager)
		self.__editor.disconnect_signal(self.__signal_id_8, manager)
		self.__editor.disconnect_signal(self.__signal_id_9, manager)
		self.__editor.disconnect_signal(self.__signal_id_10, self.__treeview)
		if self.__monitor_id:
			from gnomevfs import monitor_cancel
			monitor_cancel(self.__monitor_id)
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
		self.__language = language
		self.__populate_model(language)
		self.__treeview.columns_autosize()
		return

	def __show_cb(self, *args):
		"""
		Handles callback when the "show" signal is emitted.

		@param self: Reference to the DescriptionTreeView instance.
		@type self: A DescriptionTreeView object.
		"""
		if self.__treeview.get_property("sensitive"): self.__treeview.grab_focus()
		return

	def __sensitive_cb(self, treeview, data):
		"""
		Handles callback when the "sensitive" property changes.

		@param self: Reference to the DescriptionTreeView instance.
		@type self: A DescriptionTreeView object.

		@param treeview: Reference to the DescriptionTreeView.
		@type treeview: A DescriptionTreeView object.

		@param data: Random data
		@type data: A GObject object.
		"""
		self.__manager.emit("description-treeview-sensitivity", treeview.get_property("sensitive"))
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
		from operator import not_
		if not_(paths): return
		iterator = model.get_iter(paths[-1])
		trigger = model.get_value(iterator, 0)
		self.__manager.emit("template-selected", (self.__language, trigger))
		return

	def __remove_template_cb(self, manager):
		"""
		Handles callback when the "remove-template" signal is emitted.

		@param self: Reference to the DescriptionTreeView instance.
		@type self: A DescriptionTreeView object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.
		"""
		manager.emit("sensitive", False)
		selection = self.__treeview.get_selection()
		model, paths = selection.get_selected_rows()
		from operator import not_, contains
		if not_(paths): return
		get_keys = lambda path: self.__language + model.get_value(model.get_iter(path), 0)
		keys = map(get_keys, paths)
		from Metadata import open_template_database
		from Metadata import close_template_database
		database = open_template_database("w")
		from operator import eq, not_
		for key in database.keys():
			if not_(contains(keys, key)): continue
			del database[key]
		close_template_database(database)
		return

	def __database_changed_cb(self, monitor_uri, info_uri, event_type):
		"""
		Handles callback when the template database is modified.

		@param self: Reference to the DescriptionTreeView instance.
		@type self: An DescriptionTreeView object.

		@param monitor_uri: The uri that is monitored.
		@type monitor_uri: A String object.

		@param info_uri: The uri that is monitored.
		@type info_uri: A String object.

		@param event_type: The type of modification that occured.
		@type event_type: A gnomevfs.MONITOR_EVENT* object.
		"""
		from gnomevfs import MONITOR_EVENT_DELETED
		from gnomevfs import MONITOR_EVENT_CREATED
		from gnomevfs import MONITOR_EVENT_CHANGED
		from operator import contains
		events = [MONITOR_EVENT_CHANGED, MONITOR_EVENT_DELETED, MONITOR_EVENT_CREATED]
		if contains(events, event_type):
			self.__populate_model(self.__language)
			self.__select_new_row()
			self.__treeview.columns_autosize()
#			self.__manager.emit("sensitive", True)
		return

	def __export_template_cb(self, manager, filename):
		"""
		Handles callback when the "export-template" signal is emitted.

		@param self: Reference to the DescriptionTreeView instance.
		@type self: A DescriptionTreeView object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.
		"""
		try:
			from Exceptions import ExportPermissionError, ExportSelectionError
			manager.emit("sensitive", False)
			self.__check_permission(filename)
			templates = self.__get_template_info()
			from WriteXMLTemplate import create_template_file
			create_template_file(templates, filename)
		except ExportPermissionError:
			from i18n import msg0011
			self.__editor.error_dialog.show_message(msg0011)
		except ExportSelectionError:
			from i18n import msg0012
			self.__editor.error_dialog.show_message(msg0012)
		manager.emit("sensitive", True)
		return

	def __trigger_selected_cb(self, manager, trigger):
		self.__trigger = trigger
		return

	def __manager_sensitive_cb(self, manager, sensitive):
		self.__editor.response()
		self.__treeview.grab_focus()
		from operator import not_
		if not_(sensitive): return
		self.__editor.response()
		self.__treeview.grab_focus()
		return

	def __drag_data_get_cb(self, treeview, context, data, info, time):
		"""
		Handles callback when the "drag-data-get" signal is emitted.

		@param self: Reference to the TemplateEditorDescriptionView instance.
		@type self: A TemplateEditorDescriptionView object.

		@param treeview: Reference to the TemplateEditorDescriptionView
		@type treeview: A TemplateEditorDescriptionView object.

		@param context: An object representing context data.
		@type context: A gtk.DragContext object.

		@param data: An object representing selection data.
		@type data: A gtk.SelectionData object.

		@param info: A unique identification number for the text editor.
		@type info: An Integer object.

		@param time: The time of the drag and drop operation.
		@type time: An Integer object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		templates = self.__get_template_info()
		from WriteXMLTemplate import create_template_string
		string = create_template_string(templates)
		data.set(data.target, 8, string)
		return False
