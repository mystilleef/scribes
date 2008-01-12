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

class ForegroundSyntaxButton(ColorButton):
	"""
	This class creates a color button for the text editor's color
	editor. The color button allows users to set the syntax colors for
	programming language special words.
	"""

	def __init__(self, editor, color_editor):
		"""
		Initialize the button.

		@param self: Reference to the ForegroundSyntaxButton instance.
		@type self: A ForegroundSyntaxButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		ColorButton.__init__(self)
		self.__init_attributes(editor, color_editor)
		self.__set_properties()
		self.__sig_id_1 = self.__treeview.connect("cursor-changed", self.__button_cursor_changed)
		self.__color_id = self.connect("color-set", self.__color_set_cb)
		self.__sig_id_3 = color_editor.connect("destroy", self.__destroy_cb)
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monitor_id = monitor_add(self.__syntax_database_uri, MONITOR_FILE,
					self.__syntax_cb)

	def __init_attributes(self, editor, color_editor):
		"""
		Initialize the button's data attributes.

		@param self: Reference to the ForegroundSyntaxButton instance.
		@type self: A ForegroundSyntaxButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__treeview = color_editor.treeview
		self.__default_color = "grey"
		self.__color_id = None
		self.__sig_id_1 = self.__sig_id_2 = self.__sig_id_3 = None
		from os.path import join
		syntax_folder = join(editor.metadata_folder, "SyntaxColors")
		syntax_database_path = join(syntax_folder, "SyntaxColors.gdb")
		from gnomevfs import get_uri_from_local_path
		self.__syntax_database_uri = get_uri_from_local_path(syntax_database_path)
		return

	def __set_properties(self):
		"""
		Define the default behavior of the button.

		@param self: Reference to the ForegroundSyntaxButton instance.
		@type self: A ForegroundSyntaxButton object.
		"""
		from gtk.gdk import color_parse
		color = color_parse(self.__default_color)
		self.set_color(color)
		from i18n import msg0013
		self.set_title(msg0013)
		from SCRIBES.tooltips import syntax_button_tip
		self.__editor.tip.set_tip(self, syntax_button_tip)
		self.set_property("sensitive", False)
		return

	def __syntax_cb(self, *args):
		"""
		Handles callback when background color changes.

		@param self: Reference to the ForegroundSyntaxButton instance.
		@type self: A ForegroundSyntaxButton object.
		"""
		self.__set_color()
		return

	def __color_set_cb(self, button):
		"""
		Handles callback when the "toggled" signal is emitted.

		@param self: Reference to the ForegroundSyntaxButton instance.
		@type self: A ForegroundSyntaxButton object.

		@param button: Reference to the ForegroundSyntaxButton.
		@type button: A ForegroundSyntaxButton object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		color = self.get_color()
		color = self.__editor.convert_color_to_string(color)
		language = self.__treeview.get_language()
		tag_id = self.__treeview.get_element()
		language_id = language.get_id()
		from operator import eq
		if eq(color, self.__get_color(language_id, tag_id)): return True
		self.__update_database(language_id, tag_id, color)
		self.__treeview.grab_focus()
		return True

	def __button_cursor_changed(self, treeview):
		"""
		Handles callback when the "cursor-changed" signal is emitted.

		@param self: Reference to the ForegroundSyntaxButton instance.
		@type self: A ForegroundSyntaxButton object.

		@param treeview: The treeview for the color editor.
		@type treeview: A ColorEditorTreeView object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		if treeview.is_parent():
			self.set_property("sensitive", False)
			self.__set_color()
		else:
			self.set_property("sensitive", True)
			self.__set_color()
		return False

	def __set_color(self):
		"""
		Determines the color to set for the button.

		@param self: Reference to the ForegroundSyntaxButton instance.
		@type self: A ForegroundSyntaxButton object.
		"""
		self.handler_block(self.__color_id)
		from gtk.gdk import color_parse
		if self.__treeview.is_parent():
			color = color_parse(self.__default_color)
			self.set_color(color)
		else:
			language = self.__treeview.get_language()
			tag_id = self.__treeview.get_element()
			style = language.get_tag_style(tag_id)
			language_id = language.get_id()
			color = self.__get_color(language_id, tag_id)
			if color:
				color = color_parse(color)
			else:
				color = style.foreground
		self.set_color(color)
		self.handler_unblock(self.__color_id)
		return

	def __get_color(self, language, keyword):
		color = None
		keyword_list = self.__get_keyword_styles(language, keyword)
		if not keyword_list: return color
		color = keyword_list[0]
		return color

	def __get_keyword_styles(self, language, keyword):
		try:
			keyword_list = None
			from SyntaxColorsMetadata import get_value
			keywords = get_value(language)
			from operator import eq
			get_keyword_dict = lambda dictionary: eq(keyword, dictionary.keys()[0])
			keyword_list = filter(get_keyword_dict, keywords)
			if not keyword_list: return None
			value = keyword_list[0][keyword]
		except TypeError, IndexError:
			return keyword_list
		return value

	def __update_database(self, language, keyword, color):
		keyword_list = self.__get_keyword_styles(language, keyword)
		if keyword_list:
			keyword_list = [color, keyword_list[1], keyword_list[2], keyword_list[3], keyword_list[4]]
		else:
			keyword_list = [color, None, None, None, None]
		from SyntaxColorsMetadata import set_value
		set_value(language, keyword, keyword_list)
		return

	def __destroy_cb(self, color_editor):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the ForegroundSyntaxButton instance.
		@type self: An ForegroundSyntaxButton object.

		@param *args: Irrelevant arguments.
		@type *args: A List object.
		"""
		self.__editor.disconnect_signal(self.__sig_id_1, self.__treeview)
		self.__editor.disconnect_signal(self.__color_id, self)
		self.__editor.disconnect_signal(self.__sig_id_3, color_editor)
		self.destroy()
		from gnomevfs import monitor_cancel
		if self.__monitor_id: monitor_cancel(self.__monitor_id)
		self = None
		del self
		return
