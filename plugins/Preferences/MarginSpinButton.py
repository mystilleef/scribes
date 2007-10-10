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
This module documents a class that creates the margin spin button for the
text editor's preference dialog.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import SpinButton

class MarginSpinButton(SpinButton):
	"""
	This class creates a spin button for the text editor's preference
	dialog. The spin button allows users to set the position of the
	right margin in the buffer.
	"""

	def __init__(self, manager, editor):
		"""
		Initialize the spin button.

		@param self: Reference to the MarginSpinButton instance.
		@type self: A MarginSpinButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		SpinButton.__init__(self)
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__client.notify_add("/apps/scribes/margin_position", self.__margin_changed_cb)
		self.__client.notify_add("/apps/scribes/margin", self.__margin_cb)
		self.__signal_id_1 = self.connect("value-changed", self.__value_changed_cb)
		self.__signal_id_2 = self.__manager.connect("destroy", self.__destroy_cb)

	def __init_attributes(self, manager, editor):
		"""
		Initialize the button's data attributes.

		@param self: Reference to the MarginSpinButton instance.
		@type self: A MarginSpinButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__manager = manager
		self.__client = editor.gconf_client
		self.__signal_id_1 = self.__signal_id_2 = None
		return

	def __set_properties(self):
		"""
		Define the default behavior of the button.

		@param self: Reference to the MarginSpinButton instance.
		@type self: A MarginSpinButton object.
		"""
		margin_position = 72
		value = self.__client.get("/apps/scribes/margin_position")
		from operator import truth
		if truth(value):
			margin_position = self.__client.get_int("/apps/scribes/margin_position")
		show_margin = False
		value = self.__client.get("/apps/scribes/margin")
		from operator import truth
		if truth(value):
			show_margin = self.__client.get_bool("/apps/scribes/margin")
		self.set_property("sensitive", show_margin)
		self.set_max_length(3)
		self.set_width_chars(3)
		self.set_digits(0)
		self.set_increments(1, 5)
		self.set_range(1, 200)
		from gtk import UPDATE_ALWAYS
		self.set_update_policy(UPDATE_ALWAYS)
		self.set_numeric(True)
		self.set_snap_to_ticks(True)
		self.set_value(margin_position)
		from SCRIBES.tooltips import margin_spin_button_tip
		self.__editor.tip.set_tip(self, margin_spin_button_tip)
		return

	def __margin_changed_cb(self, client, cnxn_id, entry, data):
		"""
		Handles callback when tab size changes.

		@param self: Reference to the MarginSpinButton instance.
		@type self: A MarginSpinButton object.
		"""
		margin_position = 72
		value = self.__client.get("/apps/scribes/margin_position")
		from operator import truth
		if truth(value):
			margin_position = self.__client.get_int("/apps/scribes/margin_position")
		if int(margin_position) != int(self.get_value()):
			self.set_value(int(margin_position))
		return

	def __margin_cb(self, client, cnxn_id, entry, data):
		"""
		Handles callback when tab size changes.

		@param self: Reference to the MarginSpinButton instance.
		@type self: A MarginSpinButton object.
		"""
		show_margin = False
		value = self.__client.get("/apps/scribes/margin")
		from operator import truth
		if truth(value):
			show_margin = self.__client.get_bool("/apps/scribes/margin")
		if show_margin is False:
			self.set_property("sensitive", False)
		else:
			self.set_property("sensitive", True)
		return

	def __value_changed_cb(self, button):
		"""
		Handles callback when the "value-changed" signal is emitted.

		@param self: Reference to the MarginSpinButton instance.
		@type self: A MarginSpinButton object.

		@param button: Reference to the MarginSpinButton.
		@type button: A MarginSpinButton object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		margin_position = int(self.get_value())
		if self.__client.get_int("/apps/scribes/margin_position") != margin_position:
			self.__client.set_int("/apps/scribes/margin_position", margin_position)
			self.__client.notify("/apps/scribes/margin_position")
		from i18n import msg0025
		message = msg0025 % margin_position
		self.__editor.feedback.update_status_message(message, "succeed", 5)
		return True

	def __destroy_cb(self, manager):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the MarginSpinButton instance.
		@type self: A MarginSpinButton object.

		@param manager: Reference to the PreferencesManager instance.
		@type manager: A PreferencesManager object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__manager)
		self.destroy()
		del self
		self = None
		return
