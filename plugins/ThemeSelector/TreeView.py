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
symbol browser.

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

		@param manager: Reference to the Manager instance.
		@type manager: A Manager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(editor, manager)
		self.__set_properties()
		self.__sigid1 = self.__manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = self.__manager.connect("remove-theme", self.__remove_theme_cb)
		self.__sigid3 = self.__treeview.connect("row-activated", self.__generic_cb)
		self.__sigid4 = self.__treeview.connect("cursor-changed", self.__generic_cb)
		self.__sigid5 = self.__manager.connect("folder-changed", self.__folder_changed_cb)
		self.__sigid6 = self.__manager.connect("focus-treeview", self.__focus_treeview_cb)

		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monid1 = monitor_add(self.__uri, MONITOR_FILE, self.__theme_changed_cb)
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__precompile_method, priority=PRIORITY_LOW)
		idle_add(self.__populate_model, priority=PRIORITY_LOW)

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
		self.__schemes = []
		self.__change = True
		self.__treeview = manager.glade.get_widget("TreeView")
		self.__model = self.__create_model()
		self.__column = self.__create_column()
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		self.__monid1 = None
		from os.path import join
		preference_folder = join(editor.metadata_folder, "Preferences")
		theme_database_path = join(preference_folder, "ColorTheme.gdb")
		from gnomevfs import get_uri_from_local_path
		self.__uri = get_uri_from_local_path(theme_database_path)
		return

	def __set_properties(self):
		"""
		Define the treeview's properties.

		@param self: Reference to the BrowserTreeView instance.
		@type self: A BrowserTreeView object.
		"""
		self.__treeview.append_column(self.__column)
		return

	def __create_model(self):
		"""
		Create model for the treeview.

		@param self: Reference to the BrowserTreeView instance.
		@type self: An BrowserTreeView object.

		@return: Return a model for the treeview.
		@rtype: A gtk.ListStore object.
		"""
		from gtk import ListStore
		from gobject import TYPE_OBJECT
		model = ListStore(str, TYPE_OBJECT, bool)
		return model

	def __create_column(self):
		"""
		Create column for the treeview.

		@param self: Reference to the BrowserTreeView instance.
		@type self: A BrowserTreeView object.

		@return: A column for the treeview.
		@rtype: A gtk.TreeViewColumn object.
		"""
		from gtk import TreeViewColumn, CellRendererText, TREE_VIEW_COLUMN_FIXED
		column = TreeViewColumn()
		renderer = CellRendererText()
		column.pack_start(renderer, False)
		column.set_sizing(TREE_VIEW_COLUMN_FIXED)
		column.set_resizable(False)
		column.set_attributes(renderer, text=0)
		return column

	def __populate_model(self):
		"""
		Populate the model.

		@param self: Reference to the BrowserTreeView instance.
		@type self: A BrowserTreeView object.
		"""
		self.__treeview.handler_block(self.__sigid4)
		from Utils import get_treeview_data
		schemes = get_treeview_data(self.__editor.style_scheme_manager, self.__editor.home_folder)
		self.__treeview.set_property("sensitive", False)
		self.__update_model(schemes)
		self.__select_row()
		self.__treeview.set_property("sensitive", True)
		self.__treeview.grab_focus()
		self.__treeview.handler_unblock(self.__sigid4)
		self.__emit_can_remove_signal()
		return False

	def __update_model(self, schemes):
		if self.__schemes == schemes: return
		from copy import copy
		self.__schemes = copy(schemes)
		self.__treeview.set_model(None)
		self.__model.clear()
		schemes.sort()
		for item in schemes:
			self.__model.append([item[0], item[1], item[2]])
		self.__treeview.set_model(self.__model)
		return

	def __select_row(self):
		from ColorThemeMetadata import get_value
		scheme = get_value()
		iterator = self.__model.get_iter_first()
		try:
			while True:
				scheme_id = self.__model.get_value(iterator, 1).get_id()
				if scheme == scheme_id: break
				iterator = self.__model.iter_next(iterator)
		except TypeError:
			iterator = self.__model.get_iter_first()
		path = self.__model.get_path(iterator)
		selection = self.__treeview.get_selection()
		selection.select_iter(iterator)
		self.__treeview.set_cursor(path)
		self.__treeview.scroll_to_cell(path, use_align=True, row_align=0.5)
		return

	def __focus_treeview(self):
		self.__treeview.grab_focus()
		return

	def __precompile_method(self):
		try:
			from psyco import bind
			bind(self.__populate_model)
			bind(self.__select_row)
		except ImportError:
			pass
		return False

	def __destroy_cb(self, manager):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the BrowserTreeView instance.
		@type self: A BrowserTreeView object.

		@param manager: Reference to the BookmarkManager instance.
		@type manager: A BookmarkManager object.
		"""
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__treeview)
		self.__editor.disconnect_signal(self.__sigid4, self.__treeview)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		self.__editor.disconnect_signal(self.__sigid6, self.__manager)
		from gnomevfs import monitor_cancel
		if self.__monid1: monitor_cancel(self.__monid1)
		self.__treeview.destroy()
		del self
		self = None
		return

	def __focus_treeview_cb(self, *args):
		self.__focus_treeview()
		return True

	def __generic_cb(self, *args):
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
		self.__change_theme()
		self.__emit_can_remove_signal()
		return True

	def __remove_theme_cb(self, *args):
		scheme = self.__get_selected_scheme()
		from Utils import remove_theme
		remove_theme(scheme.get_filename())
		return True

	def __folder_changed_cb(self, *args):
		self.__treeview.set_property("sensitive", False)
#		from gobject import idle_add
#		idle_add(self.__populate_model, priority=5000)
		self.__populate_model()
		self.__change_theme()
		return True

	def __theme_changed_cb(self, *args):
		try:
			if self.__change: raise ValueError
			self.__treeview.set_property("sensitive", False)
			from gobject import idle_add
			idle_add(self.__populate_model, priority=5000)
		except ValueError:
			self.__change = True
		return

	def __emit_can_remove_signal(self):
		try:
			iterator = self.__get_selected_iter()
			can_remove = self.__model.get_value(iterator, 2)
			self.__manager.emit("can-remove", can_remove)
		except TypeError:
			pass
		return

	def __get_selected_iter(self):
		selection = self.__treeview.get_selection()
		iterator = selection.get_selected()[1]
		return iterator

	def __get_selected_scheme(self):
		iterator = self.__get_selected_iter()
		scheme = self.__model.get_value(iterator, 1)
		return scheme

	def __change_theme(self):
		try:
			self.__change = True
			iterator = self.__get_selected_iter()
			scheme = self.__model.get_value(iterator, 1)
			scheme_id = scheme.get_id()
			from Utils import change_theme
			change_theme(scheme_id)
		except TypeError:
			pass
		return False
