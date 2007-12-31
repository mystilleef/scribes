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
This module documents a class that creates the spell check button
for the text editor's preference dialog.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import CheckButton

class SpellCheckButton(CheckButton):
	"""
	This class creates a check button for the text editor's preference
	dialog. The check button allows users to enable or disable spell
	checking.
	"""

	def __init__(self, manager, editor):
		"""
		Initialize the check button.

		@param self: Reference to the SpellCheckButton instance.
		@type self: A SpellCheckButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		CheckButton.__init__(self)
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__signal_id_1 = self.connect("toggled", self.__toggled_cb)
		self.__signal_id_2 = self.__manager.connect("destroy", self.__destroy_cb)
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monitor_id = monitor_add(self.__database_uri, MONITOR_FILE,
					self.__check_spelling_cb)

	def __init_attributes(self, manager, editor):
		"""
		Initialize the button's data attributes.

		@param self: Reference to the SpellCheckButton instance.
		@type self: A SpellCheckButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__manager = manager
		self.__signal_id_1 = self.__signal_id_2 = None
		from os.path import join
		preference_folder = join(editor.metadata_folder, "Preferences")
		database_path = join(preference_folder, "SpellCheck.gdb")
		from gnomevfs import get_uri_from_local_path
		self.__database_uri = get_uri_from_local_path(database_path)
		return

	def __set_properties(self):
		"""
		Define the default behavior of the button.

		@param self: Reference to the SpellCheckButton instance.
		@type self: A SpellCheckButton object.
		"""
		from SpellCheckMetadata import get_value
		check_spelling = get_value()
		self.set_active(check_spelling)
		from i18n import msg0022
		self.set_label(msg0022)
		self.set_use_underline(True)
		from SCRIBES.tooltips import spell_check_button_tip
		self.__editor.tip.set_tip(self, spell_check_button_tip)
		return

	def __check_spelling_cb(self, *args):
		"""
		Handles callback when spell checking  properties change.

		@param self: Reference to the SpellCheckButton instance.
		@type self: A SpellCheckButton object.
		"""
		from SpellCheckMetadata import get_value
		check_spelling = get_value()
		if check_spelling:
			if self.get_active() is False:
				self.set_active(True)
			from i18n import msg0023
			self.__editor.feedback.update_status_message(msg0023, "succeed", 5)
		else:
			if self.get_active():
				self.set_active(False)
			from i18n import msg0024
			self.__editor.feedback.update_status_message(msg0024, "succeed", 5)
		return

	def __toggled_cb(self, button):
		"""
		Handles callback when the "toggled" signal is emitted.

		@param self: Reference to the SpellCheckButton instance.
		@type self: A SpellCheckButton object.

		@param button: Reference to the SpellCheckButton.
		@type button: A SpellCheckButton object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		check_spelling = self.get_active()
		from SpellCheckMetadata import set_value
		if check_spelling:
			set_value(True)
		else:
			set_value(False)
		return True

	def __destroy_cb(self, manager):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the SpellCheckButton instance.
		@type self: A SpellCheckButton object.

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
