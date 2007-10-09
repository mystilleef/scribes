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
This module documents a class that creates the reset button for the text
editor's color editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import Button

class ResetButton(Button):
	"""
	This class creates the reset button for the text editor's color
	editor. The reset button sets the value of all syntax properties to
	their default value.
	"""

	def __init__(self, editor, color_editor):
		"""
		Initialize the button.

		@param self: Reference to the ResetButton instance.
		@type self: A ResetButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		Button.__init__(self)
		self.__init_attributes(editor, color_editor)
		self.__set_properties()
		self.__sig_id_1 = self.__treeview.connect("cursor-changed", self.__button_cursor_changed)
		self.__client.notify_add("/apps/scribes/SyntaxHighlight", self.__syntax_cb)
		self.__sig_id_2 = color_editor.connect("destroy", self.__destroy_cb)
		self.__sig_id_3 = self.connect("clicked", self.__clicked_cb)

	def __init_attributes(self, editor, color_editor):
		"""
		Initialize the button's data attributes.

		@param self: Reference to the ResetButton instance.
		@type self: A ResetButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__treeview = color_editor.treeview
		self.__client = editor.gconf_client
		self.__gconf_syntax_folder = "/apps/scribes/SyntaxHighlight/"
		self.__sig_id_1 = self.__sig_id_2 = self.__sig_id_3 = None
		return

	def __set_properties(self):
		"""
		Define the default behavior of the button.

		@param self: Reference to the ResetButton instance.
		@type self: A ResetButton object.
		"""
		from SCRIBES.utils import create_button
		from gtk import STOCK_UNDO
		from i18n import msg0018
		hbox = create_button(STOCK_UNDO, msg0018)
		self.add(hbox)
		from SCRIBES.tooltips import reset_button_tip
		self.__editor.tip.set_tip(self, reset_button_tip)
		self.set_property("sensitive", False)
		return

	def __syntax_cb(self, client, cnxn_id, entry, data):
		"""
		Handles callback when background color changes.

		@param self: Reference to the ResetButton instance.
		@type self: A ResetButton object.
		"""
		self.__determine_sensitivity()
		return

	def __clicked_cb(self, button):
		"""
		Handles callback when the "toggled" signal is emitted.

		@param self: Reference to the ResetButton instance.
		@type self: A ResetButton object.

		@param button: Reference to the ResetButton.
		@type button: A ResetButton object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		language = self.__treeview.get_language()
		tag_id = self.__treeview.get_element()
		language_id = language.get_id()
		gconf_key = self.__gconf_syntax_folder + language_id + "/" + tag_id
		self.__client.unset(gconf_key)
		self.__client.notify(gconf_key)
		return True

	def __button_cursor_changed(self, treeview):
		"""
		Handles callback when the "cursor-changed" signal is emitted.

		@param self: Reference to the ResetButton instance.
		@type self: A ResetButton object.

		@param treeview: The treeview for the color editor.
		@type treeview: A ColorEditorTreeView object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		if treeview.is_parent():
			self.set_property("sensitive", False)
		else:
			self.__determine_sensitivity()
		return False

	def __determine_sensitivity(self):
		"""
		Determines the sensitivity of the button.

		@param self: Reference to the ResetButton instance.
		@type self: A ResetButton object.
		"""
		language = self.__treeview.get_language()
		tag_id = self.__treeview.get_element()
		language_id = language.get_id()
		gconf_key = self.__gconf_syntax_folder + language_id + "/" + tag_id
		from gconf import VALUE_STRING
		gconf_entry = self.__client.get_list(gconf_key, VALUE_STRING)
		self.set_property("sensitive", False)
		if gconf_entry: self.set_property("sensitive", True)
		self.__treeview.grab_focus()
		return

	def __destroy_cb(self, color_editor):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the ResetButton instance.
		@type self: A ResetButton object.

		@param color_editor: Reference to the ColorEditor
		@type color_editor: A ColorEditor object.
		"""
		self.__editor.disconnect_signal(self.__sig_id_1, self.__treeview)
		self.__editor.disconnect_signal(self.__sig_id_2, color_editor)
		self.__editor.disconnect_signal(self.__sig_id_3, self)
		self.destroy()
		self = None
		del self
		return
