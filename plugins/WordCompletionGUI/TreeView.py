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

	def __init__(self, manager, editor, completion):
		"""
		Initialize object.

		@param self: Reference to the CompletionTreeView instance.
		@type self: A CompletionTreeView object.

		@param manager: Reference to the CompletionManager instance.
		@type manager: A CompletionManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param completion: Reference to the WordCompletionManager instance.
		@type completion: A WordCompletionManager object.
		"""
		TreeView.__init__(self)
		self.__init_attributes(manager, editor, completion)
		self.__set_properties()
		from gobject import idle_add
		idle_add(self.__precompile_methods)
		self.__signal_id_1 = manager.connect("destroy", self.__destroy_cb)
		self.__signal_id_2 = completion.connect("match-found", self.__match_found_cb)
		self.__signal_id_3 = self.connect("row-activated", self.__row_activated_cb)
		self.__signal_id_4 = self.connect("button-press-event", self.__button_press_event)
		self.__signal_id_5 = manager.connect("is-visible", self.__is_visible_cb)
		self.__signal_id_7 = editor.textview.connect("key-press-event", self.__key_press_event_cb)
		self.__signal_id_8 = self.connect("cursor-changed", self.__cursor_changed_cb)
		self.__block_textview()

	def __init_attributes(self, manager, editor, completion):
		"""
		Initialize data attributes.

		@param self: Reference to the CompletionTreeView instance.
		@type self: A CompletionTreeView object.

		@param manager: Reference to the CompletionManager instance.
		@type manager: A CompletionManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param completion: Reference to the WordCompletionManager instance.
		@type completion: A WordCompletionManager object.
		"""
		self.__editor = editor
		self.__manager = manager
		self.__completion = completion
		self.__model = self.__create_model()
		self.__renderer = self.__create_renderer()
		self.__column = self.__create_column()
		self.__is_blocked = False
		self.__is_visible = False
		self.__word_list = []
		return

	def __set_properties(self):
		"""
		Define the view object's properties.

		@param self: Reference to the CompletionTreeView instance.
		@type self: A CompletionTreeView object.
		"""
		self.append_column(self.__column)
		self.set_headers_visible(False)
		self.set_property("rules-hint", True)
		self.set_property("hover-selection", True)
		self.set_property("model", self.__model)
		from gtk import STATE_SELECTED, STATE_ACTIVE
		style = self.__editor.textview.get_style()
		color = style.base[STATE_SELECTED]
		self.modify_base(STATE_ACTIVE, color)
		return

########################################################################
#
#							Helper Methods
#
########################################################################

	def __populate_model(self, completion_list):
		"""
		Populate the view's data model.

		@param self: Reference to the CompletionTreeView instance.
		@type self: A CompletionTreeView object.
		"""
		from operator import ne
		if ne(completion_list, self.__word_list):
			self.__word_list = completion_list
			self.__model.clear()
			for word in self.__word_list:
				self.__model.append([word])
			self.columns_autosize()
		self.get_selection().select_path(0)
		self.__manager.emit("populated-model", self)
		return

	def __insert_word_completion(self, path):
		"""
		Insert items selected in the completion window into the text editor's
		buffer.

		@param path: The selected row in the completion window.
		@type path: A gtk.TreeRow object.

		@param editor: Reference to the editor object.
		@type editor: An editor object.
		"""
		# Get the database containing potential completion string matches.
		model = self.__model
		# Get the selected completion string.
		completion_string = model[path[0]][0].decode("utf8")
		# Index to split completion string for insertion into the text editor's
		# buffer. Encode to utf8 before insertion.
		index = len(self.__editor.get_word_before_cursor().decode("utf8"))
		string = completion_string[index:]
		# Split completion_string at the right index and insert into the editor's
		# buffer.
		self.__editor.textbuffer.begin_user_action()
		self.__editor.textbuffer.insert_at_cursor(string)
		self.__editor.textbuffer.end_user_action()
		# Feedback to the status bar indicating word completion occurred.
		from i18n import msg0001
		self.__editor.feedback.update_status_message(msg0001, "succeed")
		return

	def __precompile_methods(self):
		try:
			from psyco import bind
			bind(self.__populate_model)
			bind(self.__insert_word_completion)
		except ImportError:
			pass
		return False

########################################################################
#
#						TreeView Creation Stuff
#
########################################################################

	def __create_model(self):
		"""
		Create the view's model, or database.

		@param self: Reference to the CompletionTreeView instance.
		@type self: A CompletionTreeView object.
		"""
		from gtk import ListStore
		model = ListStore(str)
		return model

	def __create_renderer(self):
		"""
		Create the view's text renderer.

		@param self: Reference to the CompletionTreeView instance.
		@type self: A CompletionTreeView object.
		"""
		from gtk import CellRendererText
		renderer = CellRendererText()
		return renderer

	def __create_column(self):
		"""
		Create the view's column.

		@param self: Reference to the CompletionTreeView instance.
		@type self: A CompletionTreeView object.
		"""
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
		"""
		Destroy instance of this object.

		@param self: Reference to the CompletionTreeView instance.
		@type self: A CompletionTreeView object.

		@param manager: Reference to the CompletionManager instance.
		@type manager: A CompletionManager object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, manager)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__completion)
		self.__editor.disconnect_signal(self.__signal_id_3, self)
		self.__editor.disconnect_signal(self.__signal_id_4, self)
		self.__editor.disconnect_signal(self.__signal_id_5, manager)
		self.__editor.disconnect_signal(self.__signal_id_7, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_8, self)
		self.destroy()
		del self
		self = None
		return

	def __match_found_cb(self, completion, completion_list):
		"""
		Handles callback when the "match-found" signal is emitted.

		@param self: Reference to the CompletionTreeView instance.
		@type self: A CompletionTreeView object.

		@param completion: Reference to the WordCompletionManager instance.
		@type completion: A WordCompletionManager object.

		@param completion_list: A list of words for completion.
		@type completion_list: A List object.
		"""
		self.__populate_model(completion_list)
		return

	def __row_activated_cb(self, treeview, path, column):
		"""
		Handles callback when the "row-activated" signal is emitted.

		@param self: Reference to the CompletionView instance.
		@type self: A CompletionView object.

		@param treeview: The text editor's completion window's view.
		@type treeview: A CompletionView object.

		@param path: An object representing a row in the view.
		@type path: A Path object.

		@param column: The text editor's completion window's view's column.
		@type column: A gtk.TreeViewColumn object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		try:
			self.__is_visible = False
			self.__insert_word_completion(path)
		except AttributeError:
			pass
		self.__manager.emit("hide-window")
		self.__is_visible = False
		return True

	def __button_press_event(self, treeview, event):
		"""
		Handles callback when the "button-press-event" signal is emitted.

		@param self: Reference to the CompletionTreeView instance.
		@type self: A CompletionTreeView object.

		@param treeview: The text editor's completion window's view.
		@type treeview: A CompletionTreeView object.

		@param event: An event that occurs when the right mouse button is pressed.
		@type event: A gtk.Event object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
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
		"""
		Handles callback when the "key-press-event" signal is emitted.

		This function allows the "Up" and "Down" arrow keys to work in
		the word completion window.

		@param self: Reference to the CompletionView instance.
		@type self: A CompletionView object.

		@param treeview: The text editor's completion view.
		@type treeview: A CompletionView object.

		@param event: An event that occurs when keys are pressed.
		@type event: A gtk.Event object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		from operator import not_, eq, truth
		if not_(self.__is_visible): return False
		# Get the selected item on the completion window.
		selection = self.get_selection()
		# Get the model and iterator of the selected item.
		model, iterator = selection.get_selected()
		# If for whatever reason the selection is lost, select the first row
		# automactically when the up or down arrow key is pressed.
		if not_(iterator):
			selection.select_path((0,))
			model, iterator = selection.get_selected()
		path = model.get_path(iterator)
		from gtk import keysyms
		if eq(event.keyval, keysyms.Return):
			# Insert the selected item into the editor's buffer when the enter key
			# event is detected.
			self.row_activated(path, self.get_column(0))
		elif eq(event.keyval, keysyms.Up):
			# If the up key is pressed check to see if the first row is selected.
			# If it is, select the last row. Otherwise, get the path to the row
			# above and select it.
			if not_(path[0]):
				number_of_rows = len(model)
				selection.select_path(number_of_rows-1)
				self.scroll_to_cell(number_of_rows-1)
			else:
				selection.select_path((path[0]-1,))
				self.scroll_to_cell((path[0]-1,))
		elif eq(event.keyval, keysyms.Down):
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
		"""
		Handles callback when the "is-visible" signal is emitted.

		@param self: Reference to the CompletionTreeView instance.
		@type self: A CompletionTreeView object.

		@param manager: Reference to the CompletionManager instance.
		@type manager: A CompletionManager object.

		@param is_visible: Whether or not the word completion window is visible.
		@type is_visible: A Boolean object.
		"""
		from operator import truth
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
		"""
		Unblock textview's "key-press-event" signal.

		@param self: Reference to the CompletionTreeView instance.
		@type self: A CompletionTreeView object.
		"""
		from operator import not_
		if not_(self.__is_blocked): return
		self.__editor.textview.handler_unblock(self.__signal_id_7)
		self.__is_blocked = False
		return

	def __block_textview(self):
		"""
		Block textview's "key-press-event" signal.

		The "key-press-event" signal is only useful when the word
		completion window is visible.

		@param self: Reference to the CompletionTreeView instance.
		@type self: A CompletionTreeView object.
		"""
		from operator import truth
		if truth(self.__is_blocked): return
		self.__editor.textview.handler_block(self.__signal_id_7)
		self.__is_blocked = True
		return

	def __cursor_changed_cb(self, *args):
		self.get_selection().select_path(0)
		return False
