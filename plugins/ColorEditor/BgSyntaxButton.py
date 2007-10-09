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
This module documents a class that creates the syntax color button
for the text editor's color editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import ColorButton

class BackgroundSyntaxButton(ColorButton):
	"""
	This class creates a color button for the text editor's color
	editor. The color button allows users to set the syntax colors for
	programming language special words.
	"""

	def __init__(self, editor, color_editor):
		"""
		Initialize the button.

		@param self: Reference to the BackgroundSyntaxButton instance.
		@type self: A BackgroundSyntaxButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		ColorButton.__init__(self)
		self.__init_attributes(editor, color_editor)
		self.__set_properties()
		self.__sig_id_1 = self.__treeview.connect("cursor-changed", self.__button_cursor_changed)
		self.__client.notify_add("/apps/scribes/SyntaxHighlight", self.__syntax_cb)
		self.__sig_id_2 = self.__color_id = self.connect("color-set", self.__color_set_cb)
		self.__sig_id_3 = color_editor.connect("destroy", self.__destroy_cb)

	def __init_attributes(self, editor, color_editor):
		"""
		Initialize the button's data attributes.

		@param self: Reference to the BackgroundSyntaxButton instance.
		@type self: A BackgroundSyntaxButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__treeview = color_editor.treeview
		self.__client = editor.gconf_client
		self.__default_color = "grey"
		self.__gconf_syntax_folder = "/apps/scribes/SyntaxHighlight/"
		self.__color_id = self.__sig_id_1 = self.__sig_id_2 = None
		self.__sig_id_3 = None
		return

	def __set_properties(self):
		"""
		Define the default behavior of the button.

		@param self: Reference to the BackgroundSyntaxButton instance.
		@type self: A BackgroundSyntaxButton object.
		"""
		from gtk.gdk import color_parse
		color = color_parse(self.__default_color)
		self.set_color(color)
		from i18n import msg0014
		self.set_title(msg0014)
		from SCRIBES.tooltips import syntax_button_tip
		self.__editor.tip.set_tip(self, syntax_button_tip)
		self.set_property("sensitive", False)
		return

	def __syntax_cb(self, client, cnxn_id, entry, data):
		"""
		Handles callback when background color changes.

		@param self: Reference to the BackgroundSyntaxButton instance.
		@type self: A BackgroundSyntaxButton object.
		"""
		self.handler_block(self.__color_id)
		self.__set_color()
		self.handler_unblock(self.__color_id)
		return

	def __color_set_cb(self, button):
		"""
		Handles callback when the "toggled" signal is emitted.

		@param self: Reference to the BackgroundSyntaxButton instance.
		@type self: A BackgroundSyntaxButton object.

		@param button: Reference to the BackgroundSyntaxButton.
		@type button: A BackgroundSyntaxButton object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		color = self.get_color()
		color = self.__editor.convert_color_to_string(color)
		language = self.__treeview.get_language()
		tag_id = self.__treeview.get_element()
		language_id = language.get_id()
		gconf_key = self.__gconf_syntax_folder + language_id + "/" + tag_id
		from gconf import VALUE_STRING
		gconf_entry = self.__client.get_list(gconf_key, VALUE_STRING)
		if gconf_entry:
			del gconf_entry[1]
			gconf_entry.insert(1, color)
		else:
			tag_style = language.get_tag_style(tag_id)
			bold = str(tag_style.bold)
			italic = str(tag_style.italic)
			underline = str(tag_style.underline)
			foreground = convert_color_to_spec(tag_style.foreground)
			gconf_entry = [foreground, color, bold, italic, underline]
		self.__client.set_list(gconf_key, VALUE_STRING, gconf_entry)
		self.__client.notify(gconf_key)
		self.__treeview.grab_focus()
		return True

	def __button_cursor_changed(self, treeview):
		"""
		Handles callback when the "cursor-changed" signal is emitted.

		@param self: Reference to the BackgroundSyntaxButton instance.
		@type self: A BackgroundSyntaxButton object.

		@param treeview: The treeview for the color editor.
		@type treeview: A ColorEditorTreeView object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		self.handler_block(self.__color_id)
		if treeview.is_parent():
			self.set_property("sensitive", False)
			self.__set_color()
		else:
			self.set_property("sensitive", True)
			self.__set_color()
		self.handler_unblock(self.__color_id)
		return False

	def __set_color(self):
		"""
		Determines the color to set for the button.

		@param self: Reference to the BackgroundSyntaxButton instance.
		@type self: A BackgroundSyntaxButton object.
		"""
		from gtk.gdk import color_parse
		if self.__treeview.is_parent():
			color = color_parse(self.__default_color)
			self.set_color(color)
		else:
			language = self.__treeview.get_language()
			tag_id = self.__treeview.get_element()
			tag_style = language.get_tag_style(tag_id)
			language_id = language.get_id()
			gconf_key = self.__gconf_syntax_folder + language_id + "/" + tag_id
			from gconf import VALUE_STRING
			value = self.__client.get_list(gconf_key, VALUE_STRING)
			if value:
				if value[1] != "None":
					color = color_parse(value[1])
				else:
					color = color_parse(self.__default_color)
			else:
				color = color_parse(self.__default_color)
		self.set_color(color)
		return

	def __destroy_cb(self, color_editor):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the BackgroundSyntaxButton instance.
		@type self: A BackgroundSyntaxButton object.

		@param color_editor: Reference to the color editor.
		@type color_editor: A ColorEditor object.
		"""
		self.__editor.disconnect_signal(self.__sig_id_1, self.__treeview)
		self.__editor.disconnect_signal(self.__sig_id_2, self.__color_id)
		self.__editor.disconnect_signal(self.__sig_id_3, color_editor)
		self.destroy()
		self = None
		del self
		return
