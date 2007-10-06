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
This module documents a class that implements a treeview for the bookmark
browser.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2006 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import TreeView

class BookmarkTreeView(TreeView):
	"""
	This class creates a treeview for the bookmark browser.
	"""

	def __init__(self, manager, editor):
		"""
		Intialize an instance of this class.

		@param self: Reference to the BookmarkTreeView instance.
		@type self: A BookmarkTreeView object.

		@param manager: Reference to the BookmarkManager instance.
		@type manager: A BookmarkManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		TreeView.__init__(self)
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__signal_id_1 = self.__manager.connect("destroy", self.__destroy_cb)
		self.__signal_id_2 = self.__editor.store.connect("updated", self.__store_updated_cb)
		self.__signal_id_3 = self.__manager.connect("update", self.__update_cb)
		self.__signal_id_4 = self.connect("row-activated", self.__row_activated_cb)

	def __init_attributes(self, manager, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the BookmarkTreeView instance.
		@type self: A BookmarkTreeView object.

		@param manager: Reference to the BookmarkManager instance.
		@type manager: A BookmarkManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__manager = manager
		self.__editor = editor
		self.__bookmark_manager = self.__editor.store.get_object("BookmarkManager")
		self.__bookmarked_lines = []
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		self.__signal_id_4 = None
		self.__model = self.__create_model()
		self.__line_renderer = self.__create_renderer(xalign=1.0)
		self.__text_renderer = self.__create_renderer()
		from i18n import msg0003, msg0004
		self.__line_column = self.__create_column(msg0003, self.__line_renderer, 0, False, True)
		self.__text_column = self.__create_column(msg0004, self.__text_renderer, 1, True, False)
		return

	def __set_properties(self):
		"""
		Define the treeview's properties.

		@param self: Reference to the BookmarkTreeView instance.
		@type self: A BookmarkTreeView object.
		"""
		self.set_property("model", self.__model)
		self.set_property("rules-hint", True)
		self.set_property("search-column", 0)
		self.set_property("headers-clickable", True)
		self.append_column(self.__line_column)
		self.append_column(self.__text_column)
		self.__line_column.clicked()
		return

	def __create_model(self,):
		"""
		Create model for the treeview.

		@param self: Reference to the BookmarkTreeView instance.
		@type self: An BookmarkTreeView object.

		@return: Return a model for the treeview.
		@rtype: A gtk.ListStore object.
		"""
		from gtk import ListStore
		model = ListStore(int, str, "gboolean")
		return model

	def __create_renderer(self, xalign=0.0):
		"""
		Create the renderer for the treeview's columns.

		@param self: Reference to the BookmarkTreeView instance.
		@type self: A BookmarkTreeView object.

		@return: A renderer for treeview's columns.
		@rtype: A gtk.CellRendererText object.
		"""
		from gtk import CellRendererText
		renderer = CellRendererText()
		renderer.set_property('cell-background', 'yellow')
		renderer.set_property("xalign", xalign)
		return renderer

	def __create_column(self, title, renderer, text=0, expand=False, indicator=False):
		"""
		Create column for the treeview.

		@param self: Reference to the BookmarkTreeView instance.
		@type self: A BookmarkTreeView object.

		@return: A column for the treeview.
		@rtype: A gtk.TreeViewColumn object.
		"""
		from gtk import TREE_VIEW_COLUMN_AUTOSIZE, SORT_DESCENDING
		from gtk import TreeViewColumn
		column = TreeViewColumn(title, renderer, text=text)
		column.set_expand(expand)
		column.set_sizing(TREE_VIEW_COLUMN_AUTOSIZE)
		column.set_attributes(renderer, text=text, cell_background_set=2)
		column.set_sort_indicator(indicator)
		column.set_sort_order(SORT_DESCENDING)
		column.set_sort_column_id(text)
		return column

	def __destroy_cb(self, manager):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the BookmarkTreeView instance.
		@type self: A BookmarkTreeView object.

		@param manager: Reference to the BookmarkManager instance.
		@type manager: A BookmarkManager object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self.__manager)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__editor.store)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__manager)
		self.__editor.disconnect_signal(self.__signal_id_4, self)
		if self.__model: self.__model.clear()
		if self.__line_renderer: self.__line_renderer.destroy()
		if self.__text_renderer: self.__text_renderer.destroy()
		if self.__line_column: self.__line_column.destroy()
		if self.__text_column: self.__text_column.destroy()
		self.destroy()
		del self
		self = None
		return

	def __store_updated_cb(self, store, name):
		"""
		Handles callback when the "updated" signal is emitted.

		@param self: Reference to the BookmarkTreeView instance.
		@type self: A BookmarkTreeView object.

		@param store: Reference to a Store object.
		@type store: A Store object.

		@param name: The name of the object that was updated.
		@type name: A String object.
		"""
		if name in ["BookmarkManager"]:
			if self.__editor.store:
				self.__bookmark_manager = self.__editor.store.get_object("BookmarkManager")
		return

	def __update_cb(self, manager):
		"""
		Handles callback when the "update" signal is emitted.

		@param self: Reference to the BookmarkTreeView instance.
		@type self: A BookmarkTreeView object.

		@param manager: Reference to the BookmarkManager instance.
		@type manager: A BookmarkManager object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		self.__populate_model()
		return False

	def __populate_model(self):
		"""
		Populate the model.

		@param self: Reference to the BookmarkTreeView instance.
		@type self: A BookmarkTreeView object.
		"""
		if self.__bookmark_manager is None:
			return
		try:
			lines = self.__bookmark_manager.get_bookmarked_lines()
			if not lines:
				raise AttributeError
		except AttributeError:
			return
		from lines import get_text_on_line
		value = False
		bookmarked_lines = []
		for line in lines:
			text = get_text_on_line(self.__editor.textbuffer, line)
			text = text.strip(" ")
			text = text.strip("\t")
			bookmarked_lines.append((line, text))
		if self.__bookmarked_lines == bookmarked_lines:
			return
		self.__bookmarked_lines = bookmarked_lines
		recently_bookmarked_line = self.__bookmark_manager.bookmark_list[-1].get_line()
		self.__model.clear()
		for line, text in self.__bookmarked_lines:
			if line == recently_bookmarked_line:
				value = True
			self.__model.append([(line+1), text, value])
			value = False
		self.__editor.select_row(self)
		return

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
		# Get the selected line in the dialog's treeview.
		selection = treeview.get_selection()
		model, iterator = selection.get_selected()
		line = model.get_value(iterator, 0)

		# Move cursor to the selected line in the dialog's treeview.
		iterator = self.__editor.textbuffer.get_iter_at_line(int(line)-1)
		self.__editor.textbuffer.place_cursor(iterator)
		self.__editor.move_view_to_cursor()
		# Feedback to the statusbar.
		from i18n import msg0006
		message = msg0006 % int(line)
		self.__editor.feedback.update_status_message(message, "succeed")
		return True
