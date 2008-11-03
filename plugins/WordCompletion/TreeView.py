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
This module documents a class that creates the treeview for the word
completion window.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import TreeView

class CompletionTreeView(TreeView):
	"""
	This class implements the treeview for the word completion window.
	"""

	def __init__(self, manager, editor):
		TreeView.__init__(self)
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("match-found", self.__match_found_cb)
		self.__sigid3 = self.connect("row-activated", self.__row_activated_cb)
		self.__sigid4 = self.connect("button-press-event", self.__button_press_event)
		self.__sigid5 = manager.connect("is-visible", self.__is_visible_cb)
		self.__sigid7 = editor.textview.connect("key-press-event", self.__key_press_event_cb)
		self.__sigid8 = self.connect("cursor-changed", self.__cursor_changed_cb)
		self.__sigid9 = manager.connect("no-match-found", self.__no_match_found_cb)
		self.__block_textview()
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__precompile_methods, priority=PRIORITY_LOW)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		self.__model = self.__create_model()
		self.__renderer = self.__create_renderer()
		self.__column = self.__create_column()
		self.__is_blocked = False
		self.__is_visible = False
		from collections import deque
		self.__word_list = deque([])
		return

	def __precompile_methods(self):
		methods = (self.__populate_model, self.__key_press_event_cb,
		 	self.__cursor_changed_cb, self.__no_match_found_cb,
		 	self.__match_found_cb, self.__is_visible_cb)
		self.__editor.optimize(methods)
		return False

	def __set_properties(self):
		self.append_column(self.__column)
		self.set_headers_visible(False)
		self.set_property("rules-hint", True)
		self.set_property("hover-selection", True)
		self.set_property("model", self.__model)
		from gtk import STATE_SELECTED, STATE_ACTIVE, STATE_NORMAL
		style = self.__editor.textview.get_style()
		color = style.base[STATE_SELECTED]
		self.modify_base(STATE_ACTIVE, color)
		color = style.text[STATE_NORMAL]
		self.modify_text(STATE_SELECTED, color)
		self.modify_text(STATE_ACTIVE, color)
		return

########################################################################
#
#							Helper Methods
#
########################################################################

	def __populate_model(self, completion_list):
		if completion_list != self.__word_list:
			self.set_model(None)
			self.__word_list = completion_list
			self.__model.clear()
			append = self.__model.append
			for word in self.__word_list:
				append([word])
			self.__column.queue_resize()
			self.columns_autosize()
			self.set_model(self.__model)
		self.__manager.emit("populated-model", self)
		self.get_selection().select_path(0)
		return False

	def __get_word_before_cursor(self):
		if self.__editor.inside_word() is False: return None
		word = self.__editor.textbuffer.get_text(*(self.__editor.get_word_boundary()))
		if len(word) > 2: return word
		return None

	def __insert_word_completion(self, path):
		# Get the database containing potential completion string matches.
		model = self.__model
		# Get the selected completion string.
		completion_string = model[path[0]][0].decode("utf8")
		# Index to split completion string for insertion into the text editor's
		# buffer. Encode to utf8 before insertion.
		index = len(self.__get_word_before_cursor().decode("utf8"))
		string = completion_string[index:]
		# Split completion_string at the right index and insert into the editor's
		# buffer.
		self.__editor.textbuffer.begin_user_action()
		self.__editor.textbuffer.insert_at_cursor(string)
		self.__editor.textbuffer.end_user_action()
		self.__manager.emit("no-match-found")
		# Feedback to the status bar indicating word completion occurred.
		from i18n import msg0001
		self.__editor.update_message(msg0001, "pass")
		return

########################################################################
#
#						TreeView Creation Stuff
#
########################################################################

	def __create_model(self):
		from gtk import ListStore
		model = ListStore(str)
		return model

	def __create_renderer(self):
		from gtk import CellRendererText
		renderer = CellRendererText()
		return renderer

	def __create_column(self):
		from gtk import TreeViewColumn
		column = TreeViewColumn("", self.__renderer, text=0)
		column.set_expand(False)
		return column

########################################################################
#
#						Signal and Event Handlers
#
########################################################################

	def __destroy_cb(self, manager):
		self.__editor.disconnect_signal(self.__sigid1, manager)
		self.__editor.disconnect_signal(self.__sigid2, manager)
		self.__editor.disconnect_signal(self.__sigid3, self)
		self.__editor.disconnect_signal(self.__sigid4, self)
		self.__editor.disconnect_signal(self.__sigid5, manager)
		self.__editor.disconnect_signal(self.__sigid7, self.__editor)
		self.__editor.disconnect_signal(self.__sigid8, self)
		self.__editor.disconnect_signal(self.__sigid9, manager)
		self.destroy()
		del self
		self = None
		return

	def __match_found_cb(self, completion, completion_list):
		try:
			from gobject import source_remove, timeout_add
			source_remove(self.__populate_id)
		except AttributeError:
			pass
		finally:
			from collections import deque
			self.__populate_id = timeout_add(100, self.__populate_model, deque(completion_list), priority=9999)
		return

	def __no_match_found_cb(self, *args):
		try:
			from gobject import source_remove
			source_remove(self.__populate_id)
		except AttributeError:
			pass
		return

	def __row_activated_cb(self, treeview, path, column):
		try:
			self.__is_visible = False
			self.__insert_word_completion(path)
		except AttributeError:
			pass
		self.__manager.emit("hide-window")
		self.__is_visible = False
		return True

	def __button_press_event(self, treeview, event):
		# Get the selected item on the completion window.
		selection = treeview.get_selection()
		# Get the model and iterator of the selected item.
		model, iterator = selection.get_selected()
		# Get the path and column of the selected item.
		path = model.get_path(iterator)
		column = treeview.get_column(0)
		# Activate the selected item to trigger word completion.
		treeview.row_activated(path, column)
		return True

	def __key_press_event_cb(self, treeview, event):
		if not self.__is_visible: return False
		# Get the selected item on the completion window.
		selection = self.get_selection()
		# Get the model and iterator of the selected item.
		model, iterator = selection.get_selected()
		# If for whatever reason the selection is lost, select the first row
		# automactically when the up or down arrow key is pressed.
		if not iterator:
			selection.select_path((0,))
			model, iterator = selection.get_selected()
		path = model.get_path(iterator)
		from gtk import keysyms
		if event.keyval == keysyms.Return:
			# Insert the selected item into the editor's buffer when the enter key
			# event is detected.
			self.row_activated(path, self.get_column(0))
			self.__manager.emit("no-match-found")
		elif event.keyval == keysyms.Up:
			# If the up key is pressed check to see if the first row is selected.
			# If it is, select the last row. Otherwise, get the path to the row
			# above and select it.
			if not path[0]:
				number_of_rows = len(model)
				selection.select_path(number_of_rows-1)
				self.scroll_to_cell(number_of_rows-1)
			else:
				selection.select_path((path[0]-1,))
				self.scroll_to_cell((path[0]-1,))
		elif event.keyval == keysyms.Down:
			# Get the iterator of the next row.
			next_iterator = model.iter_next(iterator)
			# If the next row exists, select it, if not select the first row.
			if next_iterator:
				selection.select_iter(next_iterator)
				path = model.get_path(next_iterator)
				self.scroll_to_cell(path)
			else:
				selection.select_path(0)
				self.scroll_to_cell(0)
		else:
			return False
		return True

	def __is_visible_cb(self, manager, is_visible):
		if is_visible:
			self.__is_visible = True
			self.columns_autosize()
			self.__unblock_textview()
			self.get_selection().select_path(0)
		else:
			self.__is_visible = False
			self.__block_textview()
		return

	def __unblock_textview(self):
		if not self.__is_blocked: return
		self.__editor.textview.handler_unblock(self.__sigid7)
		self.__is_blocked = False
		return

	def __block_textview(self):
		if self.__is_blocked: return
		self.__editor.textview.handler_block(self.__sigid7)
		self.__is_blocked = True
		return

	def __cursor_changed_cb(self, *args):
		self.get_selection().select_path(0)
		return False
