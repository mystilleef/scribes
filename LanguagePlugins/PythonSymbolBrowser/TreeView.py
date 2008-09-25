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
		self.__init_attributes(editor, manager)
		self.__set_properties()
		self.__sigid1 = self.__manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = self.__manager.connect("update", self.__update_cb)
		self.__sigid3 = self.__treeview.connect("row-activated", self.__row_activated_cb)
#		from gobject import idle_add, PRIORITY_LOW
#		idle_add(self.__precompile_method, priority=PRIORITY_LOW)

	def __init_attributes(self, editor, manager):
		self.__manager = manager
		self.__symbols = None
		self.__parent = None
		self.__editor = editor
		self.__treeview = manager.glade.get_widget("TreeView")
		self.__model = self.__create_model()
		self.__column = self.__create_column()
		self.__depth_level_iter = None
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		return

	def __set_properties(self):
		self.__treeview.append_column(self.__column)
		return

	def __create_model(self):
		from gtk import TreeStore
		from gtk.gdk import Pixbuf
		model = TreeStore(int, str, str, int, Pixbuf)
		return model

	def __create_column(self):
		from gtk import TreeViewColumn, CellRendererText, CellRendererPixbuf
		from gtk import TREE_VIEW_COLUMN_FIXED
		column = TreeViewColumn()
		pixbuf_renderer = CellRendererPixbuf()
		text_renderer = CellRendererText()
		column.pack_start(pixbuf_renderer, False)
		column.pack_start(text_renderer, False)
		column.set_sizing(TREE_VIEW_COLUMN_FIXED)
		column.set_resizable(False)
		column.set_attributes(text_renderer, text=1)
		column.set_attributes(pixbuf_renderer, pixbuf=4)
		return column

	def __populate_model(self, symbols):
		self.__treeview.set_property("sensitive", False)
		if self.__symbols != symbols:
			from copy import copy
			self.__symbols = copy(symbols)
			self.__treeview.set_model(None)
			self.__model.clear()
			indentation = self.__get_indentation_levels(symbols)
			append = self.__append_symbols
			for item in symbols:
				append(item, indentation)
			self.__treeview.set_model(self.__model)
		self.__select_row()
		self.__treeview.set_property("sensitive", True)
		self.__treeview.grab_focus()
		return False

	def __select_row(self):
		current_line = self.__editor.cursor.get_line() + 1
		get_line = lambda x: x[0]
		lines = map(get_line, self.__symbols)
		lines.reverse()
		found_line = False
		for line in lines:
			if not (current_line == line or current_line > line): continue
			found_line = True
			current_line = line
			break
		if found_line:
			self.__select_line_in_treeview(current_line)
		else:
			self.__editor.select_row(self.__treeview)
		return

	def __select_line_in_treeview(self, line):
		iterator = self.__model.get_iter_root()
		while True:
			if self.__model.get_value(iterator, 0) == line: break
			if self.__model.iter_has_child(iterator):
				parent_iterator = iterator
				found_line = False
				for index in xrange(self.__model.iter_n_children(iterator)):
					iterator = self.__model.iter_nth_child(parent_iterator, index)
					if not (self.__model.get_value(iterator, 0) == line): continue
					found_line = True
					break
				if found_line: break
				iterator = parent_iterator
			iterator = self.__model.iter_next(iterator)
			if iterator is None: break
#		try:
		path = self.__model.get_path(iterator)
		self.__treeview.expand_to_path(path)
		self.__treeview.get_selection().select_iter(iterator)
		self.__treeview.set_cursor(path)
		self.__treeview.scroll_to_cell(path, use_align=True, row_align=0.5)
#		except TypeError:
#			pass
		return

	def __get_indentation_levels(self, symbols):
		get_indentation = lambda x: x[-2]
		indentations = map(get_indentation, symbols)
		indentation_levels = list(set(indentations))
		indentation_levels.sort()
		return indentation_levels

	def __append_symbols(self, item, indentation):
		index = indentation.index(item[-2])
		parent = self.__find_parent(index)
		self.__depth_level_iter = self.__model.append(parent, item)
		return

	def __find_parent(self, index):
		if not index: return None
		depth = self.__model.iter_depth(self.__depth_level_iter)
		if index == depth:
			parent = self.__model.iter_parent(self.__depth_level_iter)
		elif index < depth:
			self.__depth_level_iter = self.__model.iter_parent(self.__depth_level_iter)
			parent = self.__find_parent(index)
		elif index > depth:
			parent = self.__depth_level_iter
		return parent

	def __select_symbol(self, line, name):
		begin = self.__editor.textbuffer.get_iter_at_line(line - 1)
		end = self.__forward_to_line_end(begin.copy())
		from gtk import TEXT_SEARCH_TEXT_ONLY
		x, y = begin.forward_search(name, TEXT_SEARCH_TEXT_ONLY, end)
		self.__editor.textbuffer.select_range(x, y)
		self.__editor.move_view_to_cursor()
		return False

	def __forward_to_line_end(self, iterator):
		if iterator.ends_line(): return iterator
		iterator.forward_to_line_end()
		return iterator

	def __destroy_cb(self, manager):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__treeview)
		self.__treeview.destroy()
		del self
		self = None
		return

	def __row_activated_cb(self, treeview, path, column):
		iterator = self.__model.get_iter(path)
		line = self.__model.get_value(iterator, 0)
		name = self.__model.get_value(iterator, 1)
		self.__manager.emit("hide-window")
		self.__select_symbol(line, name)
		self.__treeview.set_property("sensitive", False)
		return True

	def __update_cb(self, manager, symbols):
		from gobject import idle_add
		idle_add(self.__populate_model, symbols, priority=9999)
		return False
