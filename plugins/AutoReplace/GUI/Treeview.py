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
This module documents a class that creates the treeview for the
automatic replacement dialog.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2006 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import TreeView
from gobject import SIGNAL_RUN_LAST, TYPE_NONE

class AutoReplaceTreeView(TreeView):
	"""
	This class implements the treeview for the automatic replacement
	dialog. The treeview has two columns. One for abbreviations and the
	other for text to be inserted into the buffer.
	"""

	def __init__(self, manager, editor):
		"""
		Initialize the object.

		@param self: Reference to the AutoReplaceTreeView instance.
		@type self: An AutoReplaceTreeView object.

		@param manager: Reference to the AutoReplaceManager instance.
		@type manager: An AutoReplaceManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		TreeView.__init__(self)
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__populate_model()
		self.__signal_id_1 = self.__manager.connect("destroy", self.__treeview_destroy_cb)
		self.__signal_id_2 = self.__abbreviation_renderer.connect("edited", self.__treeview_abbr_edited_cb, (self.__model, 0))
		self.__signal_id_4 = self.__model.connect("row-changed", self.__treeview_row_changed_cb)
		self.__signal_id_3 = self.__replacement_renderer.connect("edited", self.__treeview_replacement_edited_cb, (self.__model, 1))
		self.__signal_id_5 = self.__model.connect("row-deleted", self.__treeview_row_deleted_cb)
		self.__signal_id_6 = self.connect_after("map", self.__treeview_map_cb)
		# Monitor plug-in folders for changes.
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monitor_id = monitor_add(self.__database_uri, MONITOR_FILE,
					self.__treeview_database_changed_cb)

	def __init_attributes(self, manager, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the AutoReplaceTreeView instance.
		@type self: An AutoReplaceTreeView object.

		@param manager: Reference to the AutoReplaceManager instance.
		@type manager: An AutoReplaceManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__manager = manager
		self.__can_monitor = True
		self.__model = self.__create_model()
		self.__abbreviation_renderer = self.__create_renderer()
		self.__replacement_renderer = self.__create_renderer()
		self.__abbreviation_column = self.__create_abbreviation_column()
		self.__replacement_column = self.__create_replacement_column()
		self.__signal_id_1 = None
		self.__signal_id_2 = None
		self.__signal_id_3 = None
		self.__signal_id_4 = None
		self.__signal_id_5 = None
		self.__monitor_id = None
		# Path to the abbreviation database.
		self.__database_path = editor.metadata_folder + "abbreviations.gdb"
		from gnomevfs import get_uri_from_local_path
		self.__database_uri = get_uri_from_local_path(self.__database_path)
		return

	def __set_properties(self):
		"""
		Set the description view's default properties.

		@param self: Reference to the TemplateEditorLanguageView instance.
		@type self: A TemplateEditorLanguageView object.
		"""
		self.set_property("model", self.__model)
		self.set_property("rules-hint", True)
		self.set_property("search-column", 0)
		self.set_property("headers-clickable", True)
		self.append_column(self.__abbreviation_column)
		self.append_column(self.__replacement_column)
		self.__abbreviation_column.clicked()
		return

	def __populate_model(self):
		"""
		Populate the treeview with data.

		@param self: Reference to the AutoReplaceTreeView instance.
		@type self: An AutoReplaceTreeView object.
		"""
		if self.__signal_id_4:
			self.__model.handler_block(self.__signal_id_4)
			self.__model.handler_block(self.__signal_id_5)
		self.__model.clear()
		database = self.__get_abbreviations_database()
		if database is None:
			self.set_property("sensitive", False)
			if self.__signal_id_4:
				self.__model.handler_unblock(self.__signal_id_4)
				self.__model.handler_unblock(self.__signal_id_5)
			return
		if not database.keys():
			self.set_property("sensitive", False)
			database.close()
			if self.__signal_id_4:
				self.__model.handler_unblock(self.__signal_id_4)
				self.__model.handler_unblock(self.__signal_id_5)
			return
		for key, value in database.items():
			self.__model.append([key, value])
		database.close()
		if self.__signal_id_4:
			self.__model.handler_unblock(self.__signal_id_4)
			self.__model.handler_unblock(self.__signal_id_5)
		self.__editor.select_row(self)
		return

	def __create_model(self,):
		"""
		Create model for the treeview.

		@param self: Reference to the AutoReplaceTreeView instance.
		@type self: An AutoReplaceTreeView object.

		@return: Return a model for the treeview.
		@rtype: A gtk.ListStore object.
		"""
		from gtk import ListStore
		model = ListStore(str, str)
		return model

	def __create_renderer(self):
		"""
		Create the renderer for the treeview's columns.

		@param self: Reference to the AutoReplaceTreeView instance.
		@type self: A AutoReplaceTreeView object.

		@return: A renderer for treeview's columns.
		@rtype: A gtk.CellRendererText object.
		"""
		from gtk import CellRendererText
		renderer = CellRendererText()
		renderer.set_property("editable", True)
		return renderer

	def __create_abbreviation_column(self):
		"""
		Create the column for abbreviations.

		@param self: Reference to the AutoReplaceTreeView instance.
		@type self: A AutoReplaceTreeView object.

		@return: A column for abbreviations.
		@rtype: A gtk.TreeViewColumn object.
		"""
		from gtk import TreeViewColumn, TREE_VIEW_COLUMN_GROW_ONLY
		from gtk import SORT_ASCENDING
		from i18n import msg0002
		column = TreeViewColumn(msg0002, self.__abbreviation_renderer, text=0)
		column.set_property("expand", False)
		column.set_property("sizing", TREE_VIEW_COLUMN_GROW_ONLY)
		column.set_property("clickable", True)
		column.set_sort_column_id(0)
		column.set_property("sort-indicator", True)
		column.set_property("sort-order", SORT_ASCENDING)
		return column

	def __create_replacement_column(self):
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
		column = TreeViewColumn(msg0003, self.__replacement_renderer, text=1)
		column.set_property("expand", True)
		column.set_property("sizing", TREE_VIEW_COLUMN_GROW_ONLY)
		return column

	def __treeview_map_cb(self, treeview):
		self.__editor.select_row(self)
		return False

	def __treeview_destroy_cb(self, manager):
		"""
		Handles callback when "destroy" signal is emitted.

		@param self: Reference to the AutoReplaceTreeView instance.
		@type self: An AutoReplaceTreeView object.

		@param manager: Reference to the AutoReplaceManager instance.
		@type manager: An AutoReplaceManager object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self.__manager)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__abbreviation_renderer)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__replacement_renderer)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__model)
		self.__editor.disconnect_signal(self.__signal_id_5, self.__model)
		from gnomevfs import monitor_cancel
		if self.__monitor_id: monitor_cancel(self.__monitor_id)
		self.destroy()
		del self
		self = None
		return

	def __treeview_row_changed_cb(self, model, path, iterator):
		"""
		Handles callback when the "row-changed" signal is emitted.

		@param self: Reference to the AutoReplaceTreeView instance.
		@type self: An AutoReplaceTreeView object.

		@param model: The model for the treeview.
		@type model: An gtk.ListStore object.

		@param path: An object representing a row.
		@type path: A gtk.TreePath object.

		@param iterator: An object pointing to a row.
		@type iterator: A gtk.TreeIter object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		self.__update_abbreviations_database()
		return False

	def __treeview_row_deleted_cb(self, model, path):
		"""
		Handles callback when the "row-changed" signal is emitted.

		@param self: Reference to the AutoReplaceTreeView instance.
		@type self: An AutoReplaceTreeView object.

		@param model: The model for the treeview.
		@type model: An gtk.ListStore object.

		@param path: An object representing a row.
		@type path: A gtk.TreePath object.

		@param iterator: An object pointing to a row.
		@type iterator: A gtk.TreeIter object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		self.__update_abbreviations_database()
		if not len(self.__model):
			self.set_property("sensitive", False)
		else:
			self.__editor.select_row(self)
		return False

	def __treeview_abbr_edited_cb(self, cell, path , text, data):
		"""
		Handles callback when the "edited" signal is emitted.

		@param self: Reference to the AutoReplaceTreeView instance.
		@type self: An AutoReplaceTreeView object.
		"""
		model, column = data
		if not text:
			iterator = model.get_iter(path)
			model.remove(iterator)
		else:
			text = text.replace(" ", "")
			for row in self.__model:
				if row.path[0] == int(path):
					continue
				if text == row[0]:
					from i18n import msg0004
					message = msg0004 % (text)
					self.__editor.error_dialog.show_message(message)
					self.__manager.edit_button.activate()
					return
			model[path][column] = text
		return False

	def __treeview_replacement_edited_cb(self, cell, path , text, data):
		"""
		Handles callback when the "edited" signal is emitted.

		@param self: Reference to the AutoReplaceTreeView instance.
		@type self: An AutoReplaceTreeView object.
		"""
		model, column = data
		model[path][column] = text
		return False

	def __treeview_database_changed_cb(self, monitor_uri, info_uri, event_type):
		"""
		Handles callback when the abbreviation database is modified.

		@param self: Reference to the AutoReplaceTreeView instance.
		@type self: An AutoReplaceTreeView object.

		@param monitor_uri: The uri that is monitored.
		@type monitor_uri: A String object.

		@param info_uri: The uri that is monitored.
		@type info_uri: A String object.

		@param event_type: The type of modification that occured.
		@type event_type: A gnomevfs.MONITOR_EVENT* object.
		"""
		if self.__can_monitor is False:
			self.__can_monitor = True
			return
		from gnomevfs import MONITOR_EVENT_DELETED
		from gnomevfs import MONITOR_EVENT_CREATED
		from gnomevfs import MONITOR_EVENT_CHANGED
		if event_type in [MONITOR_EVENT_DELETED, MONITOR_EVENT_CREATED, MONITOR_EVENT_CHANGED]:
			self.__populate_model()
		return

	def __treeview_empty_cb(self, treeview):
		"""
		Handles callback when the "treeview-empty" signal is emitted.

		@param self: Reference to the AutoReplaceTreeView instance.
		@type self: An AutoReplaceTreeView object.

		@param treeview: Reference to the AutoReplaceTreeView instance.
		@type treeview: An AutoReplaceTreeView object.
		"""
		self.set_property("sensitive", False)
		return

	def __get_abbreviations_database(self, flag="r"):
		"""
		Get a reference to the database containing abbreviations.

		@param self: Reference to the AutoReplaceTreeView instance.
		@type self: An AutoReplaceTreeView object.

		@return: A reference to the abbreviations database.
		@rtype: An Shelve object.
		"""
		from shelve import open
		from anydbm import error
		try:
			database = None
			database = open(self.__database_path, flag=flag, writeback=False)
		except error:
			database = open(self.__database_path, flag="n", writeback=False)
			database.close()
			database = None
		except:
			print "Error: Invalid database error."
		return database

	def __update_abbreviations_database(self):
		"""
		Update the abbreviations database.

		@param self: Reference to the AutoReplaceTreeView instance.
		@type self: An AutoReplaceTreeView object.
		"""
		self.__can_monitor = False
		database = self.__get_abbreviations_database("w")
		if database is None:
			return
		database.clear()
		for abbreviation, replacement in self.__model:
			database[abbreviation] = replacement
		database.close()
		return
