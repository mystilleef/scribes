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
Documents a class that creates the window for the preferences dialog.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2006 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from SCRIBES.sdialog import Dialog

class PreferencesWindow(Dialog):
	"""
	This class creates the window for the preferences dialog.
	"""

	def __init__(self, manager, editor):
		"""
		Initialize an instance of this class.

		@param self: Reference to the PreferencesWindow instance.
		@type self: A PreferencesWindow object.

		@param manager: Reference to the PreferencesManager instance
		@type manager: A PreferencesManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		Dialog.__init__(self)
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__signal_id = self.__manager.connect("destroy", self.__window_destroy_cb)

	def show_dialog(self):
		"""
		Show the document browser.

		@param self: Reference to the PreferencesWindow instance.
		@type self: A PreferencesWindow object.
		"""
		self.__editor.emit("show-dialog", self)
		from i18n import msg0009
		self.__status_id = self.__editor.feedback.set_modal_message(msg0009, "preferences")
		Dialog.show_dialog(self)
		return

	def hide_dialog(self):
		"""
		Hide the document browser.

		@param self: Reference to the PreferencesWindow instance.
		@type self: A PreferencesWindow object.
		"""
		self.__editor.emit("hide-dialog", self)
		self.__editor.feedback.unset_modal_message(self.__status_id)
		Dialog.hide_dialog(self)
		return

	def __window_destroy_cb(self, manager):
		"""
		Handles callback when "destroy" signal is emitted.

		@param self: Reference to the PreferencesWindow instance.
		@type self: An PreferencesWindow object.

		@param manager: Reference to the PreferencesManager.
		@type manager: An PreferencesManager object.
		"""
		from SCRIBES.utils import disconnect_signal, delete_attributes
		disconnect_signal(self.__signal_id, self.__manager)
		self.destroy()
		delete_attributes(self)
		del self
		self = None
		return

	def __init_attributes(self, manager, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the PreferencesWindow instance.
		@type self: A PreferencesWindow object.

		@param manager: Reference to the PreferencesManager instance
		@type manager: A PreferencesManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__manager = manager
		self.__editor = editor
		self.__signal_id = None
		self.__status_id = None
		return

	def __set_properties(self):
		"""
		Define the default behavior of the dialog.

		@param self: Reference to the PreferencesWindow instance.
		@type self: A PreferencesWindow object.
		"""
		self.set_property("name", "PreferencesDialog")
		from i18n import msg0010
		self.set_property("title", msg0010)
		from SCRIBES.utils import calculate_resolution_independence
		width, height = calculate_resolution_independence(self.__editor.window, 2.56, 2.56)
		self.set_property("default-width", width)
		self.set_transient_for(self.__editor.window)
		return
