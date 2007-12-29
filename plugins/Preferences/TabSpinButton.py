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
This module documents a class that creates the tab spin button for the
text editor's preference dialog.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import SpinButton

class TabSpinButton(SpinButton):
	"""
	This class creates a spin button for the text editor's preference
	dialog. The spin button allows users to set the size of the tab
	width.
	"""

	def __init__(self, manager, editor):
		"""
		Initialize the spin button.

		@param self: Reference to the TabSpinButton instance.
		@type self: A TabSpinButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		SpinButton.__init__(self)
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__signal_id_1 = self.connect("value-changed", self.__value_changed_cb)
		self.__signal_id_2 = self.__manager.connect("destroy", self.__destroy_cb)
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monitor_id = monitor_add(self.__database_uri, MONITOR_FILE,
					self.__tab_size_changed_cb)

	def __init_attributes(self, manager, editor):
		"""
		Initialize the button's data attributes.

		@param self: Reference to the PreferencesFontButton instance.
		@type self: A PreferencesFontButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__manager = manager
		self.__monitor_id = None
		# Path to the font database.
		from os.path import join
		preference_folder = join(editor.metadata_folder, "Preferences")
		database_path = join(preference_folder, "TabWidth.gdb")
		from gnomevfs import get_uri_from_local_path
		self.__database_uri = get_uri_from_local_path(database_path)
		self.__signal_id_1 = self.__signal_id_2 = None
		return

	def __set_properties(self):
		"""
		Define the default behavior of the button.

		@param self: Reference to the TabSpinButton instance.
		@type self: A TabSpinButton object.
		"""
		self.set_max_length(3)
		self.set_width_chars(3)
		self.set_digits(0)
		self.set_increments(1, 5)
		self.set_range(1, 24)
		from gtk import UPDATE_ALWAYS
		self.set_update_policy(UPDATE_ALWAYS)
		self.set_numeric(True)
		self.set_snap_to_ticks(True)
		from TabWidthMetadata import get_value
		tab_size = get_value()
		self.set_value(tab_size)
		from SCRIBES.tooltips import tab_spin_button_tip
		self.__editor.tip.set_tip(self, tab_spin_button_tip)
		return

	def __tab_size_changed_cb(self, *args):
		"""
		Handles callback when tab size changes.

		@param self: Reference to the TabSpinButton instance.
		@type self: A TabSpinButton object.
		"""
		from TabWidthMetadata import get_value
		tab_size = get_value()
		from operator import eq
		if eq(tab_size, self.get_value()): return
		self.set_value(int(tab_size))
		return

	def __value_changed_cb(self, button):
		"""
		Handles callback when the "value-changed" signal is emitted.

		@param self: Reference to the TabSpinButton instance.
		@type self: A TabSpinButton object.

		@param button: Reference to the TabSpinButton.
		@type button: A TabSpinButton object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		tab_size = int(self.get_value())
		from TabWidthMetadata import set_value
		set_value(tab_size)
		from i18n import msg0012
		message = msg0012 % tab_size
		self.__editor.feedback.update_status_message(message, "succeed", 5)
		return True

	def __destroy_cb(self, manager):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the TabSpinButton instance.
		@type self: A TabSpinButton object.

		@param manager: Reference to the PreferencesManager instance.
		@type manager: A PreferencesManager object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__manager)
		self.destroy()
		from gnomevfs import monitor_cancel
		if self.__monitor_id: monitor_cancel(self.__monitor_id)
		del self
		self = None
		return
