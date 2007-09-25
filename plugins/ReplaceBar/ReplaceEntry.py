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
This module exposes a class that documents the implementation of the replace
text entry widget for the text editor's replace bar.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import Entry

class ReplaceEntry(Entry):
	"""
	This class creates the text editor's replace bar's text entry widget. The
	class defines the behavior and default properties of the entry object.
	"""

	def __init__(self, replacebar):
		"""
		Initialize the entry object.

		@param self: Reference to the ScribesReplaceEntry instance.
		@type self: A ScribesReplaceEntry object.

		@param replacebar: The text editor's replace bar.
		@type replacebar: A ScribesReplaceBar object.
		"""
		Entry.__init__(self)
		self.__init_attributes(replacebar)
		self.__set_properties()
		self.__signal_id_1 = self.connect("activate", self.__entry_activate_cb)
		self.__signal_id_2 = self.__editor.connect("show-bar", self.__entry_show_bar_cb)
		self.__signal_id_3 = self.__searchmanager.connect("searching", self.__entry_searching_cb)
		self.__signal_id_4 = self.__searchmanager.connect("matches-found", self.__entry_matches_found_cb)
		self.__signal_id_5 = self.__searchmanager.connect("no-matches-found", self.__entry_no_matches_found_cb)
		self.__signal_id_6 = self.__searchmanager.connect("cancel", self.__entry_cancel_cb)
		self.__signal_id_7 = self.__find_entry.connect("changed", self.__entry_changed_cb)
		self.__signal_id_8 = self.__match_word_button.connect("toggled", self.__entry_toggled_cb)
		self.__signal_id_9 = self.__match_case_button.connect("toggled", self.__entry_toggled_cb)
		self.__signal_id_10 = self.__replace_button.connect("clicked", self.__entry_clicked_cb)
		self.__signal_id_11 = self.__replace_all_button.connect("clicked", self.__entry_clicked_cb)
		self.__signal_id_12 = self.__replacemanager.connect("replacing", self.__entry_replacing_cb)
		self.__signal_id_13 = replacebar.connect("delete", self.__destroy_cb)

	def __init_attributes(self, replacebar):
		"""
		Initialize the entry object's attributes

		@param self: Reference to the ScribesReplaceEntry instance.
		@type self: A ScribesReplaceEntry object.

		@param replacebar: The text editor's replace bar.
		@type replacebar: A ScribesReplaceBar object.
		"""
		self.__editor = replacebar.editor
		self.__searchmanager = self.__replacemanager = replacebar.search_replace_manager
		self.__find_entry = replacebar.find_text_entry
		self.__match_case_button = replacebar.match_case_button
		self.__match_word_button = replacebar.match_word_button
		self.__replace_button = replacebar.replace_button
		self.__replace_all_button = replacebar.replace_all_button
		return

	def __set_properties(self):
		"""
		Define the entry object's properties.

		@param self: Reference to the ScribesReplaceEntry instance.
		@type self: A ScribesReplaceEntry object.
		"""
		self.set_property("sensitive", False)
		return

	def __entry_activate_cb(self, entry):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the ScribesReplaceEntry instance.
		@type self: A ScribesReplaceEntry object.

		@param entry: The replace bar's replace text entry widget.
		@type entry: A ScribesReplaceEntry object.
		"""
		self.__replace_button.activate()
		return True

	def __entry_show_bar_cb(self, editor, bar):
		"""
		Handles callback when the "show-bar" signal is emitted.

		@param self: Reference to the ScribesReplaceEntry instance.
		@type self: A ScribesReplaceEntry object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param bar: The text editor's replace bar.
		@type bar: A ScribesReplaceBar object.
		"""
		self.set_property("sensitive", False)
		return

	def __entry_searching_cb(self, searchmanager):
		"""
		Handles callback when the "searching" signal is emitted.

		@param self: Reference to the ScribesReplaceEntry instance.
		@type self: A ScribesReplaceEntry object.

		@param searchmanager: The text editor's search processing object.
		@type searchmanager: A SearchProcessor object.
		"""
		self.set_property("sensitive", False)
		return

	def __entry_matches_found_cb(self, searchmanager):
		"""
		Handles callback when the "matches-found" signal is emitted.

		@param self: Reference to the ScribesReplaceEntry instance.
		@type self: A ScribesReplaceEntry object.

		@param searchmanager: The text editor's search processing object.
		@type searchmanager: A SearchProcessor object.
		"""
		self.set_property("sensitive", True)
		return

	def __entry_no_matches_found_cb(self, searchmanager):
		"""
		Handles callback when the "no-matches-found" signal is emitted.

		@param self: Reference to the ScribesReplaceEntry instance.
		@type self: A ScribesReplaceEntry object.

		@param searchmanager: The text editor's search processing object.
		@type searchmanager: A SearchProcessor object.
		"""
		self.set_property("sensitive", False)
		return

	def __entry_cancel_cb(self, searchmanager):
		"""
		Handles callback when the "cancel" signal is emitted.

		@param self: Reference to the ScribesReplaceEntry instance.
		@type self: A ScribesReplaceEntry object.

		@param searchmanager: The text editor's search processing object.
		@type searchmanager: A SearchProcessor object.
		"""
		self.set_property("sensitive", False)
		return

	def __entry_changed_cb(self, entry):
		"""
		Handles callback when the find entry's "changed" signal is emitted.

		@param self: Reference to the ScribesReplaceEntry instance.
		@type self: A ScribesReplaceEntry object.

		@param entry: The text editor's replace bar's find entry.
		@type entry: A ScribesFindEntry object.
		"""
		self.set_property("sensitive", False)
		return True

	def __entry_toggled_cb(self, checkbutton):
		"""
		Handles callback when the "toggled" signal is emitted.

		@param self: Reference to the ScribesReplaceEntry instance.
		@type self: A ScribesReplaceEntry object.

		@param checkbutton: Either checkbutton on the replace bar.
		@type checkbutton: A gtk.CheckButton object.
		"""
		self.set_property("sensitive", False)
		return True

	def __entry_clicked_cb(self, button):
		"""
		Handles callback when the replace button's "clicked" signal is emitted.

		@param self: Reference to the ScribesReplaceEntry instance.
		@type self: A ScribesReplaceEntry object.

		@param button: The replace bar's replace button.
		@type button: A ScribesReplaceButton object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		self.grab_focus()
		return True

	def __entry_replacing_cb(self, replacemanager):
		"""
		Handles callback when the "replacing" signal is emitted.

		@param self: Reference to the ScribesReplaceEntry instance.
		@type self: A ScribesReplaceEntry object.

		@param replacemanager: The text editor's replace object.
		@type replacemanager: A Replace object.
		"""
		self.set_property("sensitive", False)
		return

	def __destroy_cb(self, replacebar):
		"""
		Handles callback when the "delete" signal is emitted.

		@param self: Reference to the ReplaceEntry instance.
		@type self: A ReplaceEntry object.

		@param replacebar: Reference to the ReplaceBar instance.
		@type replacebar: A ReplaceBar object.
		"""
		from SCRIBES.utils import disconnect_signal, delete_attributes
		disconnect_signal(self.__signal_id_1, self)
		disconnect_signal(self.__signal_id_2, self.__editor)
		disconnect_signal(self.__signal_id_3, self.__searchmanager)
		disconnect_signal(self.__signal_id_4, self.__searchmanager)
		disconnect_signal(self.__signal_id_5, self.__searchmanager)
		disconnect_signal(self.__signal_id_6, self.__searchmanager)
		disconnect_signal(self.__signal_id_7, self.__find_entry)
		disconnect_signal(self.__signal_id_8, self.__match_word_button)
		disconnect_signal(self.__signal_id_9, self.__match_case_button)
		disconnect_signal(self.__signal_id_10, self.__replace_button)
		disconnect_signal(self.__signal_id_11, self.__replace_all_button)
		disconnect_signal(self.__signal_id_12, self.__replacemanager)
		disconnect_signal(self.__signal_id_13, replacebar)
		self.destroy()
		delete_attributes(self)
		del self
		self = None
		return
