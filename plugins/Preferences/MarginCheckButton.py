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
This module documents a class that creates the text wrap check button
for the text editor's preference dialog.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import CheckButton

class MarginCheckButton(CheckButton):
	"""
	This class creates a check button for the text editor's preference
	dialog. The check button allows users to set the buffer's wrapping
	properties.
	"""

	def __init__(self, manager, editor):
		"""
		Initialize the check button.

		@param self: Reference to the MarginCheckButton instance.
		@type self: A MarginCheckButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		CheckButton.__init__(self)
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__client.notify_add("/apps/scribes/margin", self.__show_margin_cb)
		self.__signal_id_1 = self.connect("toggled", self.__toggled_cb)
		self.__signal_id_2 = self.__manager.connect("destroy", self.__destroy_cb)

	def __init_attributes(self, manager, editor):
		"""
		Initialize the button's data attributes.

		@param self: Reference to the MarginCheckButton instance.
		@type self: A MarginCheckButton object.

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

		@param self: Reference to the MarginCheckButton instance.
		@type self: A MarginCheckButton object.
		"""
		show_margin = False
		value = self.__client.get("/apps/scribes/margin")
		from operator import truth
		if truth(value): show_margin = self.__client.get_bool("/apps/scribes/margin")
		self.set_active(show_margin)
		from i18n import msg0019
		self.set_label(msg0019)
		self.set_use_underline(True)
		from SCRIBES.tooltips import margin_check_button_tip
		self.__editor.tip.set_tip(self, margin_check_button_tip)
		return

	def __show_margin_cb(self, client, cnxn_id, entry, data):
		"""
		Handles callback when text wrapping properties change.

		@param self: Reference to the MarginCheckButton instance.
		@type self: A MarginCheckButton object.
		"""
		show_margin = client.get_bool("/apps/scribes/margin")
		if show_margin:
			if self.get_active() is False:
				self.set_active(True)
			from i18n import msg0020
			self.__editor.feedback.update_status_message(msg0020, "succeed", 5)
		else:
			if self.get_active():
				self.set_active(False)
			from i18n import msg0021
			self.__editor.feedback.update_status_message(msg0021, "succeed", 5)
		return

	def __toggled_cb(self, button):
		"""
		Handles callback when the "toggled" signal is emitted.

		@param self: Reference to the MarginCheckButton instance.
		@type self: A MarginCheckButton object.

		@param button: Reference to the MarginCheckButton.
		@type button: A MarginCheckButton object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		show_margin = self.get_active()
		if show_margin:
			if self.__client.get_bool("/apps/scribes/margin") is False:
				self.__client.set_bool("/apps/scribes/margin", True)
		else:
			if self.__client.get_bool("/apps/scribes/margin"):
				self.__client.set_bool("/apps/scribes/margin", False)
		self.__client.notify("/apps/scribes/margin")
		return True

	def __destroy_cb(self, manager):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the MarginCheckButton instance.
		@type self: A MarginCheckButton object.

		@param manager: Reference to the PreferencesManager instance.
		@type manager: A PreferencesManager object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__manager)
		self.destroy()
		del self
		self = None
		return
