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
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

"""
This module documents a class that implements the replace bar's
incremental search check button.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import CheckButton

class ReplaceIncrementalButton(CheckButton):
	"""
	This class implements the replace bar's incremental search check
	button. It defines the default property and behavior of the check
	button.
	"""

	def __init__(self, replacebar):
		"""
		Initialize the check button object.

		@param self: Reference to the ScribesReplaceIncrementalButton instance.
		@type self: A ScribesReplaceIncrementalButton object.

		@param replacebar: The text editor's replacebar
		@type replacebar: A ScribesReplaceBar object.
		"""
		from i18n import msg0013
		CheckButton.__init__(self, msg0013, use_underline=True)
		self.__init_attributes(replacebar)
		self.__signal_id_1 = self.connect("toggled", self.__checkbutton_toggled_cb)
		self.__signal_id_2 = self.__editor.connect("show-bar", self.__checkbutton_show_bar_cb)
		self.__signal_id_3 = self.__editor.connect("hide-bar", self.__checkbutton_hide_bar_cb)
		self.__signal_id_4 = self.__searchmanager.connect("searching", self.__checkbutton_searching_cb)
		self.__signal_id_5 = self.__searchmanager.connect("matches-found", self.__checkbutton_matches_found_cb)
		self.__signal_id_6 = self.__searchmanager.connect("no-matches-found", self.__checkbutton_no_matches_found_cb)
		self.__signal_id_7 = self.__searchmanager.connect("cancel", self.__checkbutton_cancel_cb)
		self.__signal_id_8 = replacebar.connect("delete", self.__destroy_cb)

	def __init_attributes(self, replacebar):
		"""
		Initialize the check button's data attributes.

		@param self: Reference to the ScribesReplaceIncrementalButton instance.
		@type self: A ScribesReplaceIncrementalButton object.

		@param replacebar: The text editor's replacebar
		@type replacebar: A ScribesReplaceBar object.
		"""
		self.__replacebar = replacebar
		self.__editor = replacebar.editor
		self.__searchmanager = replacebar.search_replace_manager
		self.__searchentry = replacebar.find_text_entry
		self.__signal_id_1 = self.__signal_id_2 = None
		self.__signal_id_3 = self.__signal_id_4 = None
		self.__signal_id_5 = self.__signal_id_6 = None
		self.__signal_id_7 = self.__signal_id_8 = None
		return

	def __checkbutton_toggled_cb(self, togglebutton):
		"""
		Handles callback when the "toggled" signal is emitted.

		@param self: Reference to the ScribesReplaceIncrementalButton instance.
		@type self: A ScribesReplaceIncrementalButton object.

		@param togglebutton: The findbar's case check button.
		@type togglebutton: A CheckButton object.
		"""
		self.__searchmanager.reset()
		value = self.get_property("active")
		self.__searchmanager.enable_incremental_searching(value)
		return True

	def __checkbutton_show_bar_cb(self, editor, bar):
		"""
		Handles callback when the "show-bar" signal is emitted.

		@param self: Reference to the ScribesReplaceIncrementalButton instance.
		@type self: A ScribesReplaceIncrementalButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param bar: One of the text editor's bars.
		@type bar: A ScribesBar object.
		"""
		if bar is self.__replacebar:
			value = self.get_property("active")
			self.__searchmanager.enable_incremental_searching(value)
		return

	def __checkbutton_hide_bar_cb(self, editor, bar):
		"""
		Handles callback when the "show-bar" signal is emitted.

		@param self: Reference to the ScribesReplaceIncrementalButton instance.
		@type self: A ScribesReplaceIncrementalButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param bar: One of the text editor's bars.
		@type bar: A ScribesBar object.
		"""
		if bar is self.__replacebar:
			self.__searchmanager.reset()
		return

	def __checkbutton_searching_cb(self, searchmanager):
		"""
		Handles callback when the "searching" signal is emitted.

		@param self: Reference to the ScribesReplaceIncrementalButton instance.
		@type self: A ScribesReplaceIncrementalButton object.

		@param searchmanager: The text editor's search processor.
		@type searchmanager: A SearchProcessor object.
		"""
		self.set_property("sensitive", False)
		return

	def __checkbutton_matches_found_cb(self, searchmanager):
		"""
		Handles callback when the "matches-found" signal is emitted.

		@param self: Reference to the ScribesReplaceIncrementalButton instance.
		@type self: A ScribesReplaceIncrementalButton object.

		@param searchmanager: The text editor's search processor.
		@type searchmanager: A SearchProcessor object.
		"""
		self.set_property("sensitive", True)
		return

	def __checkbutton_no_matches_found_cb(self, searchmanager):
		"""
		Handles callback when the "no-matches-found" signal is emitted.

		@param self: Reference to the ScribesReplaceIncrementalButton instance.
		@type self: A ScribesReplaceIncrementalButton object.

		@param searchmanager: The text editor's search processor.
		@type searchmanager: A SearchProcessor object.
		"""
		self.set_property("sensitive", True)
		return

	def __checkbutton_cancel_cb(self, searchmanager):
		"""
		Handles callback when the "cancel" signal is emitted.

		@param self: Reference to the ScribesReplaceIncrementalButton instance.
		@type self: A ScribesReplaceIncrementalButton object.

		@param searchmanager: The text editor's search processor.
		@type searchmanager: A SearchProcessor object.
		"""
		self.set_property("sensitive", True)
		return

	def __destroy_cb(self, replacebar):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the ReplaceIncrementalButton instance.
		@type self: A ReplaceIncrementalButton object.

		@param replacebar: Reference to the ReplaceBar instance.
		@type replacebar: A ReplaceBar object.
		"""
		from SCRIBES.utils import disconnect_signal, delete_attributes
		disconnect_signal(self.__signal_id_1, self)
		disconnect_signal(self.__signal_id_2, self.__editor)
		disconnect_signal(self.__signal_id_3, self.__editor)
		disconnect_signal(self.__signal_id_4, self.__searchmanager)
		disconnect_signal(self.__signal_id_5, self.__searchmanager)
		disconnect_signal(self.__signal_id_6, self.__searchmanager)
		disconnect_signal(self.__signal_id_7, self.__searchmanager)
		disconnect_signal(self.__signal_id_8, replacebar)
		self.destroy()
		del self
		self = None
		return
