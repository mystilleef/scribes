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
This module exposes a class that creates the previous button for text editor's
findbar.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import Button

class FindPreviousButton(Button):
	"""
	This class creates a button for the text editor's findbar. The button allows
	users to cycle through found matches.
	"""

	def __init__(self, findbar):
		"""
		Initialize the button.

		@param self: Reference to the ScribesFindPreviousButton instance.
		@type self: A ScribesFindPreviousButton object.

		@param findbar: The text editor's findbar.
		@type findbar: A ScribesFindBar object.
		"""
		Button.__init__(self)
		self.__init_attributes(findbar)
		self.__set_properties()
		self.__create_button()
		self.__signal_id_3 = self.connect("clicked", self.__previousbutton_clicked_cb)
		self.__signal_id_4 = self.__editor.connect("show-bar", self.__previousbutton_show_bar_cb)
		self.__signal_id_5 = self.__editor.connect("hide-bar", self.__previousbutton_hide_bar_cb)
		self.__signal_id_6 = self.__entry.connect("changed", self.__previousbutton_changed_cb)
		self.__signal_id_1 = self.__searchmanager.connect_after("previous", self.__previousbutton_previous_cb)
		self.__signal_id_2 = self.__searchmanager.connect_after("next", self.__previousbutton_next_cb)
		self.__signal_id_7 = self.__word_check_button.connect("toggled", self.__previousbutton_toggled_cb)
		self.__signal_id_8 = self.__case_check_button.connect("toggled", self.__previousbutton_toggled_cb)
		self.__signal_id_9 = findbar.connect("delete", self.__destroy_cb)
		self.__block_search_replace_signals()

	def __init_attributes(self, findbar):
		"""
		Initialize the button's attributes

		@param self: Reference to the ScribesFindPreviousButton instance.
		@type self: A ScribesFindPreviousButton object.

		@param findbar: The text editor's findbar
		@type findbar: A ScribesFindBar object.
		"""
		self.__entry = findbar.find_text_entry
		self.__editor = findbar.editor
		self.__searchmanager = findbar.search_replace_manager
		self.__signal_id_1 = None
		self.__signal_id_2 = self.__signal_id_9 = None
		self.__signal_id_3 = self.__signal_id_4 = self.__signal_id_5 = None
		self.__signal_id_6 = self.__signal_id_7 = self.__signal_id_8 = None
		self.__word_check_button = findbar.match_word_button
		self.__case_check_button = findbar.match_case_button
		return

	def __set_properties(self):
		"""
		Set the button's properties.

		@param self: Reference to the ScribesFindPreviousButton instance.
		@type self: A ScribesFindPreviousButton object.
		"""
		self.set_property("sensitive", False)
		return

	def __create_button(self):
		"""
		Customize the button.

		@param self: Reference to the ScribesFindPreviousButton instance.
		@type self: A ScribesFindPreviousButton object.
		"""
		from i18n import msg0003
		from gtk import STOCK_GO_BACK
		hbox = self.__editor.create_button(STOCK_GO_BACK, msg0003)
		self.add(hbox)
		return

	def __previousbutton_clicked_cb(self, button):
		"""
		Handles callback when the "clicked" signal is emitted.

		@param self: Reference to the ScribesFindPreviousButton instance.
		@type self: A ScribesFindPreviousButton object.

		@param button: The findbar's previous button.
		@type button: A ScribesFindPreviousButton object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		self.__searchmanager.previous()
		return True

	def __previousbutton_show_bar_cb(self, editor, bar):
		"""
		Handles callback when the "show-bar" signal is emitted.

		@param self: Reference to the ScribesFindPreviousButton instance.
		@type self: A ScribesFindPreviousButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param bar: The text editor's findbar.
		@type bar: A ScribesFindBar object.
		"""
		self.__unblock_search_replace_signals()
		self.set_property("sensitive", False)
		return

	def __previousbutton_hide_bar_cb(self, editor, bar):
		"""
		Handles callback when the "hide-bar" signal is emitted.

		@param self: Reference to the ScribesFindPreviousButton instance.
		@type self: A ScribesFindPreviousButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param bar: The text editor's findbar.
		@type bar: A ScribesFindBar object.
		"""
		self.__block_search_replace_signals()
		return

	def __previousbutton_changed_cb(self, entry):
		"""
		Handles callback when the findbar's entry's "changed" signal is emitted.

		@param self: Reference to the ScribesFindPreviousButton instance.
		@type self: A ScribesFindPreviousButton object.

		@param entry: The findbar's entry.
		@type entry: A ScribesFindEntry object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		self.set_property("sensitive", False)
		return True

	def __previousbutton_previous_cb(self, searchmanager):
		"""
		Handles callback when the "previous" signal is emitted.

		@param self: Reference to the ScribesFindPreviousButton instance.
		@type self: A ScribesFindPreviousButton object.

		@param searchmanager: The text editor's search processing object.
		@type searchmanager: A SearchProcessor object.
		"""
		if searchmanager.index <= 0:
			self.set_property("sensitive", False)
		return


	def __previousbutton_next_cb(self, searchmanager):
		"""
		Handles callback when the "next" signal is emitted.

		@param self: Reference to the ScribesFindPreviousButton instance.
		@type self: A ScribesFindPreviousButton object.

		@param searchmanager: The text editor's search processing object.
		@type searchmanager: A SearchProcessor object.
		"""
		if searchmanager.index > 0:
			if self.get_property("sensitive") is False:
				self.set_property("sensitive", True)
		return

	def __previousbutton_toggled_cb(self, togglebutton):
		"""
		Handles callback when the "toggled" signal is emitted.

		@param self: Reference to the ScribesFindPreviousButton instance.
		@type self: A ScribesFindPreviousButton object.

		@param togglebutton: The check buttons on the findbar.
		@type togglebutton: A gtk.CheckButton object.

		@return: True to prevent propagation of signals to parent widgets.
		@type: A Boolean Object.
		"""
		return True

	def __block_search_replace_signals(self):
		self.__searchmanager.handler_block(self.__signal_id_1)
		self.__searchmanager.handler_block(self.__signal_id_2)
		return

	def __unblock_search_replace_signals(self):
		self.__searchmanager.handler_unblock(self.__signal_id_1)
		self.__searchmanager.handler_unblock(self.__signal_id_2)
		return

	def __destroy_cb(self, findbar):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the FindPreviousButton instance.
		@type self: A FindPreviousButton object.

		@param findbar: Reference to the FindBar instance.
		@type findbar: A FindBar object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self.__searchmanager)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__searchmanager)
		self.__editor.disconnect_signal(self.__signal_id_3, self)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_5, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_6, self.__entry)
		self.__editor.disconnect_signal(self.__signal_id_7, self.__word_check_button)
		self.__editor.disconnect_signal(self.__signal_id_8, self.__case_check_button)
		self.__editor.disconnect_signal(self.__signal_id_9, findbar)
		self.destroy()
		del self
		self = None
		return
