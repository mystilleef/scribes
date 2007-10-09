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

class ThemeCheckButton(CheckButton):
	"""
	This class creates a check button for the text editor's preference
	dialog. The check button allows users to set the buffer's wrapping
	properties.
	"""

	def __init__(self, manager, editor):
		"""
		Initialize the check button.

		@param self: Reference to the ThemeCheckButton instance.
		@type self: A ThemeCheckButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		CheckButton.__init__(self)
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__client.notify_add("/apps/scribes/use_theme_colors", self.__use_theme_colors_cb)
		self.__signal_id_1 = self.__manager.connect("destroy", self.__destroy_cb)
		self.__signal_id_2 = self.connect("toggled", self.__toggled_cb)

	def __init_attributes(self, manager, editor):
		"""
		Initialize the button's data attributes.

		@param self: Reference to the ThemeCheckButton instance.
		@type self: A ThemeCheckButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		from gconf import client_get_default
		self.__client = client_get_default()
		self.__manager = manager
		self.__signal_id_1 = self.__signal_id_2 = None
		return

	def __set_properties(self):
		"""
		Define the default behavior of the button.

		@param self: Reference to the ThemeCheckButton instance.
		@type self: A ThemeCheckButton object.
		"""
		use_theme_colors = True
		value = self.__client.get("/apps/scribes/use_theme_colors")
		from operator import truth
		if truth(value):
			use_theme_colors = self.__client.get_bool("/apps/scribes/use_theme_colors")
		self.set_active(use_theme_colors)
		from i18n import msg0003
		self.set_label(msg0003)
		self.set_use_underline(True)
		from SCRIBES.tooltips import theme_check_button_tip
		self.__editor.tip.set_tip(self, theme_check_button_tip)
		return

	def __use_theme_colors_cb(self, client, cnxn_id, entry, data):
		"""
		Handles callback when text wrapping properties change.

		@param self: Reference to the ThemeCheckButton instance.
		@type self: A ThemeCheckButton object.
		"""
		self.handler_block(self.__signal_id_2)
		use_theme_colors = client.get_bool("/apps/scribes/use_theme_colors")
		from operator import truth, not_
		if truth(use_theme_colors):
			if not_(self.get_active()):
				self.set_active(True)
			from i18n import msg0004
			self.__editor.feedback.update_status_message(msg0004, "succeed", 5)
		else:
			if truth(self.get_active()):
				self.set_active(False)
			from i18n import msg0005
			self.__editor.feedback.update_status_message(msg0005, "succeed", 5)
		self.handler_unblock(self.__signal_id_2)
		return

	def __toggled_cb(self, button):
		"""
		Handles callback when the "toggled" signal is emitted.

		@param self: Reference to the ThemeCheckButton instance.
		@type self: A ThemeCheckButton object.

		@param button: Reference to the ThemeCheckButton.
		@type button: A ThemeCheckButton object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		use_theme_colors = self.get_active()
		from operator import truth
		if truth(use_theme_colors):
			self.__client.set_bool("/apps/scribes/use_theme_colors", True)
		else:
			self.__client.set_bool("/apps/scribes/use_theme_colors", False)
		self.__client.notify("/apps/scribes/use_theme_colors")
		return True

	def __destroy_cb(self, manager):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the ThemeCheckButton instance.
		@type self: A ThemeCheckButton object.

		@param manager: Reference to the ColorEditormanager instance.
		@type manager: A ColorEditormanager object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self.__manager)
		self.__editor.disconnect_signal(self.__signal_id_2, self)
		self.destroy()
		del self
		self = None
		return
