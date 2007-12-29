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
		self.__signal_id_1 = self.connect("font-set", self.__font_set_cb)
		self.__signal_id_2 = self.__manager.connect("destroy", self.__destroy_cb)
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monitor_id = monitor_add(self.__database_uri, MONITOR_FILE,
					self.__font_changed_cb)

	def __init_attributes(self, manager, editor):
		"""
		Initialize the button's data attributes.

		@param self: Reference to the PreferencesFontButton instance.
		@type self: A PreferencesFontButton object.
		"""
		self.__editor = editor
		self.__manager = manager
		self.__monitor_id = None
		# Path to the font database.
		from os.path import join
		preference_folder = join(editor.metadata_folder, "Preferences")
		database_path = join(preference_folder, "Font.gdb")
		from gnomevfs import get_uri_from_local_path
		self.__database_uri = get_uri_from_local_path(database_path)
		self.__signal_id_1 = self.__signal_id_2 = None
		return

	def __set_properties(self):
		"""
		Define the default behavior of the button.

		@param self: Reference to the PreferencesFontButton instance.
		@type self: A PreferencesFontButton object.
		"""
		from FontMetadata import get_value
		font_name = get_value()
		self.set_font_name(font_name)
		from SCRIBES.tooltips import font_button_tip
		self.__editor.tip.set_tip(self, font_button_tip)
		return

	def __font_changed_cb(self, *args):
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
		from FontMetadata import get_value
		font_name = get_value()
		from operator import eq
		if eq(font_name, self.get_font_name()): return
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
		from FontMetadata import set_value
		set_value(font_name)
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
		self.__editor.disconnect_signal(self.__signal_id_1, self)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__manager)
		self.destroy()
		from gnomevfs import monitor_cancel
		if self.__monitor_id: monitor_cancel(self.__monitor_id)
		del self
		self = None
		return
