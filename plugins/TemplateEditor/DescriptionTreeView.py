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
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("language-selected", self.__language_selected_cb)
		self.__sigid3 = self.__treeview.connect("cursor-changed", self.__cursor_changed_cb)
		self.__sigid4 = manager.connect_after("select-description-view", self.__select_description_view_cb)
		self.__sigid5 = manager.connect("remove-templates", self.__remove_templates_cb)
		self.__sigid6 = manager.connect("database-updated", self.__database_updated_cb)
		self.__sigid7 = manager.connect("process", self.__process_cb)
		self.__sigid8 = self.__treeview.connect("row-activated", self.__row_activated_cb)
		self.__sigid9 = self.__treeview.connect("key-press-event", self.__key_press_event_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__language = None
		from collections import deque
		self.__trigger_queue = deque()
		self.__model = self.__create_model()
		self.__name_renderer = self.__create_renderer()
		self.__name_column = self.__create_name_column()
		self.__description_renderer = self.__create_renderer()
		self.__description_column = self.__create_description_column()
		self.__treeview = manager.glade.get_widget("TemplateTreeView")
		self.__selection_row_index = 0
		return

	def __set_properties(self):
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
		from gtk import ListStore
		model = ListStore(str, str, str)
		return model

	def __create_renderer(self):
		from gtk import CellRendererText
		renderer = CellRendererText()
		return renderer

	def __create_name_column(self):
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
		from gtk import TreeViewColumn, TREE_VIEW_COLUMN_GROW_ONLY
		from gtk import SORT_ASCENDING
		from i18n import msg0003
		column = TreeViewColumn(msg0003, self.__description_renderer, text=1)
		column.set_property("expand", True)
		column.set_property("sizing", TREE_VIEW_COLUMN_GROW_ONLY)
		return column

	def __populate_model(self, data):
		self.__model.clear()
		self.__treeview.set_property("sensitive", False)
		self.__manager.emit("description-view-sensitivity", False)
		if not data: return False
		self.__treeview.handler_block(self.__sigid3)
		self.__treeview.set_model(None)
		for info in data:
			self.__model.append([info[0].strip("|"), info[1], info[3]])
		self.__treeview.set_model(self.__model)
		self.__treeview.set_property("sensitive", True)
		self.__manager.emit("description-view-sensitivity", True)
		self.__treeview.handler_unblock(self.__sigid3)
		return False

	def __select_row(self):
		try:
			selection = self.__treeview.get_selection()
			selection.select_path(0)
			iterator = self.__model.get_iter_first()
			path = self.__model.get_path(iterator)
			self.__treeview.scroll_to_cell(path, self.__treeview.get_column(0), True, 0.5, 0.0)
			self.__treeview.set_cursor(path, self.__treeview.get_column(0))
			self.__treeview.columns_autosize()
		except TypeError:
			pass
		return

	def __select_row_at_index(self, index):
		try:
			iterator = self.__model.get_iter_first()
			if iterator is None: raise ValueError
			for count in xrange(index):
				result = self.__model.iter_next(iterator)
				if result is None: break
				iterator = result
			self.__select_row_at_iterator(iterator)
		except ValueError:
			self.__treeview.set_property("sensitive", False)
		return False

	def __select_row_at_iterator(self, iterator):
		selection = self.__treeview.get_selection()
		selection.unselect_all()
		selection.select_iter(iterator)
		path = self.__model.get_path(iterator)
		self.__select_row_at_path(path)
		return False

	def __select_row_at_path(self, path):
		self.__treeview.scroll_to_cell(path, self.__treeview.get_column(0), True, 0.5, 0.0)
		self.__treeview.set_cursor(path, self.__treeview.get_column(0))
		self.__treeview.columns_autosize()
		self.__treeview.grab_focus()
		return False

	def __select_row_at_trigger(self, trigger):
		return False

	def __get_triggers(self):
		iterator = self.__model.get_iter_first()
		if iterator is None: return None
		triggers = []
		trigger = self.__model.get_value(iterator, 0)
		triggers.append(trigger)
		while True:
			iterator = self.__model.iter_next(iterator)
			if iterator is None: break
			trigger = self.__model.get_value(iterator, 0)
			triggers.append(trigger)
		return triggers

	def __process_language(self, language, select=False):
		self.__language = language
		from Metadata import get_template_data
		data = get_template_data(language)
		self.__populate_model(data)
		if select: self.__select_row()
		return False

	def __select_trigger_row(self, trigger=None):
		if trigger is None: return self.__select_row_at_index(self.__selection_row_index)
		iterator = self.__model.get_iter_first()
		if iterator is None: return self.__treeview.set_property("sensitive", False)
		while True:
			trigger_ = self.__model.get_value(iterator, 0)
			if trigger == trigger_: break
			iterator = self.__model.iter_next(iterator)
			if iterator is None: break
		self.__select_row_at_iterator(iterator)
		return

	def __get_trigger_to_select(self, ot, nt):
		if ot is None: return nt[-1]
		trigger = set(nt).difference(set(ot))
		if not trigger: return None
		return trigger.pop()

	def __database_update(self):
		old_triggers = self.__get_triggers()
		self.__process_language(self.__language)
		new_triggers = self.__get_triggers()
		if not new_triggers: return self.__treeview.set_property("sensitive", False)
		trigger = self.__get_trigger_to_select(old_triggers, new_triggers)
		self.__select_trigger_row(trigger)
		return False

	def __destroy_cb(self, manager):
		self.__editor.disconnect_signal(self.__sigid1, manager)
		self.__editor.disconnect_signal(self.__sigid2, manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__treeview)
		self.__editor.disconnect_signal(self.__sigid4, manager)
		self.__editor.disconnect_signal(self.__sigid5, manager)
		self.__editor.disconnect_signal(self.__sigid6, manager)
		self.__editor.disconnect_signal(self.__sigid7, manager)
		self.__editor.disconnect_signal(self.__sigid8, self.__treeview)
		self.__editor.disconnect_signal(self.__sigid9, self.__treeview)
		self.__treeview.destroy()
		del self
		self = None
		return

	def __process_cb(self, *args):
		self.__treeview.set_property("sensitive", False)
		return False

	def __language_selected_cb(self, manager, language):
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__id)
		except AttributeError:
			pass
		finally:
			self.__id = idle_add(self.__process_language, language, True, priority=3000)
		return

	def __cursor_changed_cb(self, treeview):
		selection = treeview.get_selection()
		model, paths = selection.get_selected_rows()
		if not paths: return
		iterator = model.get_iter(paths[-1])
		database_key = model.get_value(iterator, 2)
		trigger = model.get_value(iterator, 0)
		description = model.get_value(iterator, 1)
		self.__manager.emit("template-selected", (self.__language, database_key))
		self.__manager.emit("trigger-selected", trigger)
		self.__manager.emit("description-selected", description)
		self.__selection_row_index = self.__get_triggers().index(trigger)
		return

	def __remove_templates_cb(self, *args):
		selection = self.__treeview.get_selection()
		model, paths = selection.get_selected_rows()
		if not paths: return
		self.__treeview.set_property("sensitive", False)
		iterators = [self.__model.get_iter(path) for path in paths]
		triggers = [self.__model.get_value(iterator, 0) for iterator in iterators]
		prefix = self.__language + "|"
		keys = [prefix + trigger for trigger in triggers]
		from Metadata import remove_value
		[remove_value(key) for key in keys]
		return False

	def __select_description_view_cb(self, *args):
		if self.__treeview.get_property("sensitive") is False: return False
		self.__treeview.grab_focus()
		return False

	def __database_updated_cb(self, *args):
		self.__database_update()
		return False

	def __row_activated_cb(self, *args):
		self.__manager.emit("show-edit-dialog")
		return False

	def __key_press_event_cb(self, treeview, event):
		from gtk import keysyms
		if event.keyval != keysyms.Delete: return False
		self.__manager.emit("remove-templates")
		return True
