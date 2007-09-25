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
The modules exposes a class that creates the text editor's findbar's entry
widget.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import Entry

class FindEntry(Entry):
	"""
	This class creates the findbar's entry for the text editor. The class defines,
	the behavior and default properties of the entry widget.
	"""

	def __init__(self, findbar):
		"""
		Initialize the entry object.

		@param self: Reference to the ScribesFindEntry instance.
		@type self: A ScribesFindEntry object.

		@param findbar: The text editor's findbar.
		@type findbar: A ScribesFindBar object.
		"""
		Entry.__init__(self)
		self.__init_attributes(findbar)
		self.__set_properties()
		self.__signal_id_1 = self.__editor.connect_after("show-bar", self.__findentry_show_bar_cb)
		self.__signal_id_2 = self.__searchmanager.connect("searching", self.__findentry_searching_cb)
		self.__signal_id_3 = self.__searchmanager.connect("matches-found", self.__findentry_matches_found_cb)
		self.__signal_id_4 = self.__searchmanager.connect("no-matches-found", self.__findentry_no_matches_found_cb)
		self.__signal_id_5 = self.__searchmanager.connect("cancel", self.__findentry_cancel_cb)
		self.__signal_id_6 = findbar.connect("delete", self.__destroy_cb)

	def __init_attributes(self, findbar):
		"""
		Initialize the entry's attributes.

		@param self: Reference to the ScribesFindEntry instance.
		@type self: A ScribesFindEntry object.

		@param findbar: The text editor's findbar.
		@type findbar: A ScribesFindBar object.
		"""
		self.__editor = findbar.editor
		self.__searchmanager = findbar.search_replace_manager
		from EntryCompletion import FindEntryCompletion
		self.__completion = FindEntryCompletion(self.__searchmanager)
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		self.__signal_id_4 = self.__signal_id_5 = None
		return

	def __set_properties(self):
		"""
		Define the text entry object's properties.

		@param self: Reference to the ScribesFindEntry instance.
		@type self: A ScribesFindEntry object.
		"""
		self.set_completion(self.__completion)
		return

	def __findentry_show_bar_cb(self, editor, bar):
		"""
		Handels callback when the "show-bar" signal is emitted.

		@param self: Reference to the ScribesFindEntry instance.
		@type self: A ScribesFindEntry object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param bar: The text editor's findbar.
		@type bar: A ScribesFindBar object.
		"""
		self.set_property("sensitive", True)
		selection = self.__editor.textbuffer.get_selection_bounds()
		if selection:
			from operator import eq
			if eq(selection[0].get_line(), selection[1].get_line()):
				text = self.__editor.textbuffer.get_text(selection[0], selection[1])
				self.set_text(text)
		self.grab_focus()
		return

	def __findentry_searching_cb(self, searchmanager):
		"""
		Handels callback when the "searching" signal is emitted.

		@param self: Reference to the ScribesFindEntry instance.
		@type self: A ScribesFindEntry object.

		@param searchmanager: The text editor's searcing processing object.
		@type searchmanager: A SearchProcessor object.
		"""
		self.set_property("sensitive", False)
		self.grab_focus()
		return

	def __findentry_matches_found_cb(self, searchmanager):
		"""
		Handels callback when the "matches-found" signal is emitted.

		@param self: Reference to the ScribesFindEntry instance.
		@type self: A ScribesFindEntry object.

		@param searchmanager: The text editor's searcing processing object.
		@type searchmanager: A SearchProcessor object.
		"""
		self.set_property("sensitive", True)
		self.grab_focus()
		return

	def __findentry_no_matches_found_cb(self, searchmanager):
		"""
		Handels callback when the "no-matches-found" signal is emitted.

		@param self: Reference to the ScribesFindEntry instance.
		@type self: A ScribesFindEntry object.

		@param searchmanager: The text editor's searcing processing object.
		@type searchmanager: A SearchProcessor object.
		"""
		self.set_property("sensitive", True)
		self.grab_focus()
		return

	def __findentry_cancel_cb(self, searchmanager):
		"""
		Handels callback when the "cancel" signal is emitted.

		@param self: Reference to the ScribesFindEntry instance.
		@type self: A ScribesFindEntry object.

		@param searchmanager: The text editor's searcing processing object.
		@type searchmanager: A SearchProcessor object.
		"""
		self.set_property("sensitive", True)
		self.grab_focus()
		return

	def __destroy_cb(self, findbar):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the FindEntry instance.
		@type self: A FindEntry object.

		@param findbar: Reference to the FindBar instance.
		@type findbar: A FindBar object.
		"""
		from SCRIBES.utils import disconnect_signal, delete_attributes
		disconnect_signal(self.__signal_id_1, self.__editor)
		disconnect_signal(self.__signal_id_2, self.__searchmanager)
		disconnect_signal(self.__signal_id_3, self.__searchmanager)
		disconnect_signal(self.__signal_id_4, self.__searchmanager)
		disconnect_signal(self.__signal_id_5, self.__searchmanager)
		disconnect_signal(self.__signal_id_6, findbar)
		if self.__completion:
			self.__completion.destroy_object()
		self.destroy()
		delete_attributes(self)
		del self
		self = None
		return
