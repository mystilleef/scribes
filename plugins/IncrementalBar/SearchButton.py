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
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
This module exposes a class that creates the search button for the text editor's
findbar.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import Button

class FindSearchButton(Button):
	"""
	This class creates a search button for the text editor's findbar. It defines
	the behavior and default properties of the button.
	"""

	def __init__(self, findbar):
		"""
		Initialize the button.

		@param self: Reference to the ScribesFindSearchButton instance.
		@type self: A ScribesFindSearchButton object.

		@param findbar: The text editor's findbar.
		@type findbar: A ScribesFindBar object.
		"""
		from gtk import STOCK_FIND
		Button.__init__(self, stock=STOCK_FIND, use_underline=True)
		self.__init_attributes(findbar)
		self.__set_properties()
		self.__signal_id_1 = self.connect("clicked", self.__searchbutton_clicked_cb)
		self.__signal_id_2 = self.__editor.connect("show-bar", self.__searchbutton_show_bar_cb)
		self.__signal_id_3 = self.__editor.connect("hide-bar", self.__searchbutton_hide_bar_cb)
		self.__signal_id_4 = self.__entry.connect("changed", self.__searchbutton_changed_cb)
		self.__signal_id_5 = self.__searchmanager.connect("cancel", self.__searchbutton_cancel_cb)
		self.__signal_id_6 = findbar.connect("delete", self.__destroy_cb)
		self.__block_search_replace_signals()

	def __init_attributes(self, findbar):
		"""
		Initialize the button's attributes.

		@param self: Reference to the ScribesFindSearchButton instance.
		@type self: A ScribesFindSearchButton object.

		@param findbar: the text editor's findbar.
		@type findbar: A ScribesFindBar object.
		"""
		self.__editor = findbar.editor
		self.__entry = findbar.find_text_entry
		self.__searchmanager = findbar.search_replace_manager
		self.__begin_pos = None
		self.__end_pos = None
		self.__status_id = None
		self.__signal_id_1 = None
		self.__signal_id_2 = None
		self.__signal_id_3 = None
		self.__signal_id_4 = None
		self.__signal_id_5 = None
		return

	def __set_properties(self):
		"""
		Set the button's default properties.

		@param self: Reference to the ScribesFindSearchButton instance.
		@type self: S ScribesFindSearchButton object.
		"""
		self.set_property("sensitive", False)
		return

	def __searchbutton_show_bar_cb(self, editor, bar):
		"""
		Handles callback when the "show-bar" signal is emitted.

		@param self: Reference to the ScribesFindSearchButton instance.
		@type self: A ScribesFindSearchButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param bar: The text editor's findbar.
		@type bar: A ScribesFindBar object.
		"""
		self.__unblock_search_replace_signals()
		if self.__entry.get_text():
			self.set_property("sensitive", True)
		else:
			self.set_property("sensitive", False)
		begin, end = self.__editor.textbuffer.get_bounds()
		selection = self.__editor.textbuffer.get_selection_bounds()
		if selection:
			from operator import eq
			if eq(selection[0].get_line(), selection[1].get_line()):
				begin = self.__editor.textbuffer.create_mark(None, begin, True)
				end = self.__editor.textbuffer.create_mark(None, end, False)
			else:
				begin = self.__editor.textbuffer.create_mark(None, selection[0], True)
				end = self.__editor.textbuffer.create_mark(None, selection[1], False)
		else:
			begin = self.__editor.textbuffer.create_mark(None, begin, True)
			end = self.__editor.textbuffer.create_mark(None, end, False)
		self.__begin_pos = begin
		self.__end_pos = end
		return

	def __searchbutton_hide_bar_cb(self, editor, bar):
		"""
		Handles callback when the "hide-bar" signal is emitted.

		@param self: Reference to the ScribesFindSearchButton instance.
		@type self: A ScribesFindSearchButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param bar: One of the text editor's bar object.
		@type bar: A ScribesBar object.
		"""
		self.__block_search_replace_signals()
		from operator import not_, truth
		if truth(self.__begin_pos) and not_(self.__begin_pos.get_deleted()):
			self.__editor.textbuffer.delete_mark(self.__begin_pos)
			self.__begin_pos = None
		if truth(self.__end_pos) and not_(self.__end_pos.get_deleted()):
			self.__editor.textbuffer.delete_mark(self.__end_pos)
			self.__end_pos = None
		return

	def __searchbutton_changed_cb(self, entry):
		"""
		Handles callback when the "changed" signal is emitted.

		@param self: Reference to the ScribesFindSearchButton instance.
		@type self: A ScribesFindSearchButton object.

		@param entry: The findbar's entry object.
		@type entry: A ScribesFindEntry object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		if entry.get_text():
			self.set_property("sensitive", True)
		else:
			self.set_property("sensitive", False)
		return True

	def __searchbutton_clicked_cb(self, button):
		"""
		Handles callback when the button's "clicked" signal is emitted.

		@param self: Reference to the ScribesFindSearchButton instance.
		@type self: A ScribesFindSearchButton object.

		@param button: The findbar's find button.
		@type button: A ScribesFindSearchButton object.
		"""
		self.__searchmanager.search(self.__entry.get_text(), self.__begin_pos, self.__end_pos)
		return True

	def __searchbutton_cancel_cb(self, searchmanager):
		"""
		Handles callback when the "cancel" signal is emitted.

		@param self: Reference to the ScribesFindSearchButton instance.
		@type self: A ScribesFindSearchButton object.

		@param searchmanager: The text editor's search processing object.
		@type searchmanager: A SearchProcessor object.
		"""
		if self.__entry.get_text():
			self.set_property("sensitive", True)
		else:
			self.set_property("sensitive", False)
		return

	def __block_search_replace_signals(self):
		self.__searchmanager.handler_block(self.__signal_id_5)
		return

	def __unblock_search_replace_signals(self):
		self.__searchmanager.handler_unblock(self.__signal_id_5)
		return

	def __destroy_cb(self, findbar):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the FindSearchButton instance.
		@type self: A FindSearchButton object.

		@param findbar: Reference to the FindBar instance.
		@type findbar: A FindBar object.
		"""
		from operator import not_, truth
		if truth(self.__begin_pos) and not_(self.__begin_pos.get_deleted()):
			self.__editor.textbuffer.delete_mark(self.__begin_pos)
			self.__begin_pos = None
		if truth(self.__end_pos) and not_(self.__end_pos.get_deleted()):
			self.__editor.textbuffer.delete_mark(self.__end_pos)
			self.__end_pos = None
		from SCRIBES.utils import disconnect_signal, delete_attributes
		disconnect_signal(self.__signal_id_1, self)
		disconnect_signal(self.__signal_id_2, self.__editor)
		disconnect_signal(self.__signal_id_3, self.__editor)
		disconnect_signal(self.__signal_id_4, self.__entry)
		disconnect_signal(self.__signal_id_5, self.__searchmanager)
		disconnect_signal(self.__signal_id_6, findbar)
		self.destroy()
		delete_attributes(self)
		del self
		self = None
		return
