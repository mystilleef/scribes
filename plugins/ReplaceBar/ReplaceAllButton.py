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
This module exposes a class that documents the implementation of the replace all
button for the text editor's replace bar.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import Button

class ReplaceAllButton(Button):
	"""
	This class creates the text editor's replace bar's replace button. The
	class defines the behavior and default properties of the entry object.
	"""

	def __init__(self, replacebar):
		"""
		Initialize the entry object.

		@param self: Reference to the ScribesReplaceAllButton instance.
		@type self: A ScribesReplaceAllButton object.

		@param replacebar: The text editor's replace bar.
		@type replacebar: A ScribesReplaceBar object.
		"""
		Button.__init__(self)
		self.__init_attributes(replacebar)
		self.__set_properties()
		self.__create_button()
		self.__signal_id_1 = self.connect("clicked", self.__button_clicked_cb)
		self.__signal_id_2 = self.__editor.connect("show-bar", self.__button_show_bar_cb)
		self.__signal_id_3 = self.__searchmanager.connect("searching", self.__button_searching_cb)
		self.__signal_id_4 = self.__searchmanager.connect("matches-found", self.__button_matches_found_cb)
		self.__signal_id_5 = self.__searchmanager.connect("no-matches-found", self.__button_no_matches_found_cb)
		self.__signal_id_6 = self.__searchmanager.connect("cancel", self.__button_cancel_cb)
		self.__signal_id_7 = self.__find_entry.connect("changed", self.__button_changed_cb)
		self.__signal_id_8 = self.__match_word_button.connect("toggled", self.__button_toggled_cb)
		self.__signal_id_9 = self.__match_case_button.connect("toggled", self.__button_toggled_cb)
		self.__signal_id_10 = self.__replacemanager.connect("replacing", self.__button_replacing_cb)
		self.__signal_id_11 = self.__replacemanager.connect("replaced-all", self.__button_replaced_all_cb)
		self.__signal_id_12 = replacebar.connect("delete", self.__destroy_cb)

	def __init_attributes(self, replacebar):
		"""
		Initialize the entry object's attributes.

		@param self: Reference to the ScribesReplaceAllButton instance.
		@type self: A ScribesReplaceAllButton object.

		@param replacebar: The text editor's replace bar.
		@type replacebar: A ScribesReplaceBar object.
		"""
		self.__replacebar = replacebar
		self.__editor = replacebar.editor
		self.__searchmanager = self.__replacemanager = replacebar.search_replace_manager
		self.__find_entry = replacebar.find_text_entry
		self.__match_case_button = replacebar.match_case_button
		self.__match_word_button = replacebar.match_word_button
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		self.__signal_id_4 = self.__signal_id_5 = self.__signal_id_6 = None
		self.__signal_id_7 = self.__signal_id_8 = self.__signal_id_9 = None
		self.__signal_id_10 = self.__signal_id_11 = self.__signal_id_12 = None
		return

	def __set_properties(self):
		"""
		Define the entry object's properties.

		@param self: Reference to the ScribesReplaceAllButton instance.
		@type self: A ScribesReplaceAllButton object.
		"""
		self.set_property("sensitive", False)
		return

	def __create_button(self):
		"""
		Create the replace button.

		@param self: Reference to the ScribesReplaceAllButton instance.
		@type self: A ScribesReplaceAllButton object.
		"""
		from gtk import HBox, Label
		hbox = HBox()
		from i18n import msg0012
		label = Label(msg0012)
		label.set_property("use-underline", True)
		hbox.pack_start(label, False, False, 0)
		self.add(hbox)
		return

	def __button_clicked_cb(self, button):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the ScribesReplaceAllButton instance.
		@type self: A ScribesReplaceAllButton object.

		@param button: The replace bar's replace text entry widget.
		@type button: A ScribesReplaceAllButton object.
		"""
		self.__replacemanager.replace_all(self.__replacebar.replace_entry.get_text())
		return True

	def __button_show_bar_cb(self, editor, bar):
		"""
		Handles callback when the "show-bar" signal is emitted.

		@param self: Reference to the ScribesReplaceAllButton instance.
		@type self: A ScribesReplaceAllButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param bar: The text editor's replace bar.
		@type bar: A ScribesReplaceBar object.
		"""
		self.set_property("sensitive", False)
		return

	def __button_searching_cb(self, searchmanager):
		"""
		Handles callback when the "searching" signal is emitted.

		@param self: Reference to the ScribesReplaceAllButton instance.
		@type self: A ScribesReplaceAllButton object.

		@param searchmanager: The text editor's search processing object.
		@type searchmanager: A SearchProcessor object.
		"""
		self.set_property("sensitive", False)
		return

	def __button_matches_found_cb(self, searchmanager):
		"""
		Handles callback when the "matches-found" signal is emitted.

		@param self: Reference to the ScribesReplaceAllButton instance.
		@type self: A ScribesReplaceAllButton object.

		@param searchmanager: The text editor's search processing object.
		@type searchmanager: A SearchProcessor object.
		"""
		if self.__searchmanager.number_of_matches > 1:
			self.set_property("sensitive", True)
		else:
			self.set_property("sensitive", False)
		return

	def __button_no_matches_found_cb(self, searchmanager):
		"""
		Handles callback when the "no-matches-found" signal is emitted.

		@param self: Reference to the ScribesReplaceAllButton instance.
		@type self: A ScribesReplaceAllButton object.

		@param searchmanager: The text editor's search processing object.
		@type searchmanager: A SearchProcessor object.
		"""
		self.set_property("sensitive", False)
		return

	def __button_cancel_cb(self, searchmanager):
		"""
		Handles callback when the "cancel" signal is emitted.

		@param self: Reference to the ScribesReplaceAllButton instance.
		@type self: A ScribesReplaceAllButton object.

		@param searchmanager: The text editor's search processing object.
		@type searchmanager: A SearchProcessor object.
		"""
		self.set_property("sensitive", False)
		return

	def __button_changed_cb(self, entry):
		"""
		Handles callback when the find entry's "changed" signal is emitted.

		@param self: Reference to the ScribesReplaceAllButton instance.
		@type self: A ScribesReplaceAllButton object.

		@param entry: The text editor's replace bar's find entry.
		@type entry: A ScribesFindEntry object.
		"""
		self.set_property("sensitive", False)
		return True

	def __button_toggled_cb(self, checkbutton):
		"""
		Handles callback when the "toggled" signal is emitted.

		@param self: Reference to the ScribesReplaceAllButton instance.
		@type self: A ScribesReplaceAllButton object.

		@param checkbutton: Either checkbutton on the replace bar.
		@type checkbutton: A gtk.CheckButton object.
		"""
		self.set_property("sensitive", False)
		return True

	def __button_replacing_cb(self, replacemanager):
		"""
		Handles callback when the "replacing" signal is emitted.

		@param self: Reference to the ScribesReplaceButton instance.
		@type self: A ScribesReplaceButton object.

		@param replacemanager: The text editor's replace object.
		@type replacemanager: A Replace object.
		"""
		self.set_property("sensitive", False)
		return

	def __button_replaced_all_cb(self, replacemanager):
		"""
		Handles callback when the "replacing" signal is emitted.

		@param self: Reference to the ScribesReplaceButton instance.
		@type self: A ScribesReplaceButton object.

		@param replacemanager: The text editor's replace object.
		@type replacemanager: A Replace object.
		"""
		find_text =	self.__find_entry.get_text()
		replace_text = self.__replacebar.replace_entry.get_text()
		return

	def __destroy_cb(self, replacebar):
		self.__editor.disconnect_signal(self.__signal_id_1, self)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__searchmanager)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__searchmanager)
		self.__editor.disconnect_signal(self.__signal_id_5, self.__searchmanager)
		self.__editor.disconnect_signal(self.__signal_id_6, self.__searchmanager)
		self.__editor.disconnect_signal(self.__signal_id_7, self.__find_entry)
		self.__editor.disconnect_signal(self.__signal_id_8, self.__match_word_button)
		self.__editor.disconnect_signal(self.__signal_id_9, self.__match_case_button)
		self.__editor.disconnect_signal(self.__signal_id_10, self.__replacemanager)
		self.__editor.disconnect_signal(self.__signal_id_11, self.__replacemanager)
		self.__editor.disconnect_signal(self.__signal_id_12, replacebar)
		self.destroy()
		del self
		self = None
		return
