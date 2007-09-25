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
This module documents a class that creates the underline check button
for the text editor's preference dialog.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import CheckButton

class UnderlineCheckButton(CheckButton):
	"""
	This class creates a check button for the text editor's preference
	dialog. The check button allows users to set the underline attribute of
	keywords in programming languages.
	"""

	def __init__(self, editor, color_editor):
		"""
		Initialize the check button.

		@param self: Reference to the UnderlineCheckButton instance.
		@type self: A UnderlineCheckButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		CheckButton.__init__(self)
		self.__init_attributes(editor, color_editor)
		self.__set_properties()
		self.__sig_id_1 = self.__treeview.connect("cursor-changed", self.__button_cursor_changed)
		self.__client.notify_add("/apps/scribes/SyntaxHighlight", self.__syntax_cb)
		self.__toggle_id = self.connect("toggled", self.__toggled_cb)
		self.__sig_id_2 = color_editor.connect("destroy", self.__destroy_cb)

	def __init_attributes(self, editor, color_editor):
		"""
		Initialize the button's data attributes.

		@param self: Reference to the UnderlineCheckButton instance.
		@type self: A UnderlineCheckButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__treeview = color_editor.treeview
		self.__client = editor.gconf_client
		self.__gconf_syntax_folder = "/apps/scribes/SyntaxHighlight/"
		self.__toggle_id = self.__sig_id_1 = self.__sig_id_2 = None
		return

	def __set_properties(self):
		"""
		Define the default behavior of the button.

		@param self: Reference to the UnderlineCheckButton instance.
		@type self: A UnderlineCheckButton object.
		"""
		self.set_property("sensitive", False)
		self.set_active(False)
		from i18n import msg0017
		self.set_label(msg0017)
		self.set_use_underline(True)
		from SCRIBES.tooltips import underline_check_button_tip
		self.__editor.tip.set_tip(self, underline_check_button_tip)
		return

	def __syntax_cb(self, client, cnxn_id, entry, data):
		"""
		Handles callback when bold attribute changes.

		@param self: Reference to the UnderlineCheckButton instance.
		@type self: A UnderlineCheckButton object.
		"""
		self.handler_block(self.__toggle_id)
		language = self.__treeview.get_language()
		tag_id = self.__treeview.get_element()
		language_id = language.get_id()
		gconf_key = self.__gconf_syntax_folder + language_id + "/" + tag_id
		from gconf import VALUE_STRING
		gconf_entry = self.__client.get_list(gconf_key, VALUE_STRING)
		self.set_active(False)
		if gconf_entry:
			value = gconf_entry[4]
			if value.startswith("T"):
				if self.get_active() is False:
					self.set_active(True)
			else:
				if self.get_active():
					self.set_active(False)
		else:
			self.__determine_toggle_option()
		self.handler_unblock(self.__toggle_id)
		return

	def __toggled_cb(self, button):
		"""
		Handles callback when the "toggled" signal is emitted.

		@param self: Reference to the UnderlineCheckButton instance.
		@type self: A UnderlineCheckButton object.

		@param button: Reference to the UnderlineCheckButton.
		@type button: A UnderlineCheckButton object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		use_underline = self.get_active()
		language = self.__treeview.get_language()
		tag_id = self.__treeview.get_element()
		language_id = language.get_id()
		gconf_key = self.__gconf_syntax_folder + language_id + "/" + tag_id
		from gconf import VALUE_STRING
		gconf_entry = self.__client.get_list(gconf_key, VALUE_STRING)
		if gconf_entry:
			del gconf_entry[4]
			gconf_entry.insert(4, str(use_underline))
		else:
			tag_style = language.get_tag_style(tag_id)
			bold = str(tag_style.bold)
			italic = str(tag_style.italic)
			underline = str(use_underline)
			from SCRIBES.utils import convert_color_to_spec
			foreground = convert_color_to_spec(tag_style.foreground)
			background = convert_color_to_spec(tag_style.background)
			gconf_entry = [foreground, "None", bold, italic, underline]
		self.__client.set_list(gconf_key, VALUE_STRING, gconf_entry)
		self.__client.notify(gconf_key)
		self.__treeview.grab_focus()
		return True

	def __button_cursor_changed(self, treeview):
		"""
		Handles callback when the "cursor-changed" signal is emitted.

		@param self: Reference to the UnderlineCheckButton instance.
		@type self: A UnderlineCheckButton object.

		@param treeview: The color editor's treeview.
		@type treeview: A ColorEditorTreeView object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		self.handler_block(self.__toggle_id)
		if treeview.is_parent():
			self.set_property("sensitive", False)
			self.__determine_toggle_option()
		else:
			self.set_property("sensitive", True)
			self.__determine_toggle_option()
		self.handler_unblock(self.__toggle_id)
		return True

	def __determine_toggle_option(self):
		"""
		Determine the toggle option of the button.

		@param self: Reference to the UnderlineCheckButton instance.
		@type self: A UnderlineCheckButton object.
		"""
		if self.__treeview.is_parent():
			self.set_active(False)
		else:
			language = self.__treeview.get_language()
			tag_id = self.__treeview.get_element()
			language_id = language.get_id()
			gconf_key = self.__gconf_syntax_folder + language_id + "/" + tag_id
			from gconf import VALUE_STRING
			gconf_entry = self.__client.get_list(gconf_key, VALUE_STRING)
			if gconf_entry:
				value = gconf_entry[4]
				if value.startswith("T"):
					self.set_active(True)
				else:
					self.set_active(False)
			else:
				tag_style = language.get_tag_style(tag_id)
				underline = tag_style.underline
				self.set_active(underline)
		return

	def __destroy_cb(self, color_editor):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the BoldCheckButton instance.
		@type self: A BoldCheckButton object.

		@param color_editor: Reference to the ColorEditor
		@type color_editor: A ColorEditor object.
		"""
		from SCRIBES.utils import delete_attributes, disconnect_signal
		disconnect_signal(self.__sig_id_1, self.__treeview)
		disconnect_signal(self.__sig_id_2, color_editor)
		disconnect_signal(self.__toggle_id, self)
		self.destroy()
		self = None
		del self
		return
