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
This module documents a class that creates the font button for the text
editor's preference dialog.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import FontButton

class PreferencesFontButton(FontButton):
	"""
	This class creates a font button for the text editor's preference
	dialog.
	"""

	def __init__(self, manager, editor):
		"""
		Initialize the font button.

		@param self: Reference to the PreferencesFontButton instance.
		@type self: A PreferencesFontButton object.
		"""
		FontButton.__init__(self)
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__client.notify_add("/apps/scribes/font", self.__font_changed_cb)
		self.__signal_id_1 = self.connect("font-set", self.__font_set_cb)
		self.__signal_id_2 = self.__manager.connect("destroy", self.__destroy_cb)

	def __init_attributes(self, manager, editor):
		"""
		Initialize the button's data attributes.

		@param self: Reference to the PreferencesFontButton instance.
		@type self: A PreferencesFontButton object.
		"""
		self.__editor = editor
		self.__manager = manager
		self.__client = editor.gconf_client
		self.__signal_id_1 = self.__signal_id_2 = None
		return

	def __set_properties(self):
		"""
		Define the default behavior of the button.

		@param self: Reference to the PreferencesFontButton instance.
		@type self: A PreferencesFontButton object.
		"""
		font_name = "Monospace 12"
		value = self.__client.get("/apps/scribes/font")
		from operator import truth
		if truth(value):
			font_name = self.__client.get_string("/apps/scribes/font")
		self.set_font_name(font_name)
		from SCRIBES.tooltips import font_button_tip
		self.__editor.tip.set_tip(self, font_button_tip)
		return

	def __font_changed_cb(self, client, cnxn_id, entry, data):
		"""
		Handles callback when font changes.

		@param self: Reference to the PreferencesFontButton instance.
		@type self: A PreferencesFontButton object.

		@param client: A client used to query the GConf daemon and database
		@type client: A gconf.Client object.

		@param cnxn_id: The identification number for the GConf client.
		@type cnxn_id: An Integer object.

		@param entry: An entry from the GConf database.
		@type entry: A gconf.Entry object.

		@param data: Optional data
		@type data: Any type object.
		"""
		font_name = entry.value.to_string()
		if font_name != self.get_font_name():
			self.set_font_name(font_name)
		return

	def __font_set_cb(self, button):
		"""
		Handles callback when the "clicked" signal is emitted.

		@param self: Reference to the PreferencesFontButton instance.
		@type self: A PreferencesFontButton object.

		@param button: Reference to the PreferencesFontButton.
		@type button: A PreferencesFontButton object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		font_name = self.get_font_name()
		self.__client.set_string("/apps/scribes/font", font_name)
		self.__client.notify("/apps/scribes/font")
		from i18n import msg0011
		message = msg0011 % font_name
		self.__editor.feedback.update_status_message(message, "succeed", 5)
		return True

	def __destroy_cb(self, manager):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the PreferencesFontButton instance.
		@type self: A PreferencesFontButton object.

		@param manager: Reference to the PreferencesManager instance.
		@type manager: A PreferencesManager object.
		"""
		from SCRIBES.utils import disconnect_signal, delete_attributes
		disconnect_signal(self.__signal_id_1, self)
		disconnect_signal(self.__signal_id_2, self.__manager)
		self.destroy()
		delete_attributes(self)
		del self
		self = None
		return
