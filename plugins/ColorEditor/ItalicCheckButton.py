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
This module documents a class that creates the italic check button
for the text editor's preference dialog.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import CheckButton

class ItalicCheckButton(CheckButton):
	"""
	This class creates a check button for the text editor's preference
	dialog. The check button allows users to set the italic attribute of
	keywords in programming languages.
	"""

	def __init__(self, editor, color_editor):
		"""
		Initialize the check button.

		@param self: Reference to the ItalicCheckButton instance.
		@type self: A ItalicCheckButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		CheckButton.__init__(self)
		self.__init_attributes(editor, color_editor)
		self.__set_properties()
		self.__sig_id_1 = self.__treeview.connect("cursor-changed", self.__button_cursor_changed)
		self.__toggle_id = self.connect("toggled", self.__toggled_cb)
		self.__sig_id_2 = color_editor.connect("destroy", self.__destroy_cb)
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monitor_id = monitor_add(self.__syntax_database_uri, MONITOR_FILE,
					self.__syntax_cb)

	def __init_attributes(self, editor, color_editor):
		"""
		Initialize the button's data attributes.

		@param self: Reference to the ItalicCheckButton instance.
		@type self: A ItalicCheckButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__treeview = color_editor.treeview
		self.__toggle_id = self.__sig_id_1 = self.__sig_id_2 = None
		from os.path import join
		syntax_folder = join(editor.metadata_folder, "SyntaxColors")
		syntax_database_path = join(syntax_folder, "SyntaxColors.gdb")
		from gnomevfs import get_uri_from_local_path
		self.__syntax_database_uri = get_uri_from_local_path(syntax_database_path)
		return

	def __set_properties(self):
		"""
		Define the default behavior of the button.

		@param self: Reference to the ItalicCheckButton instance.
		@type self: A ItalicCheckButton object.
		"""
		self.set_property("sensitive", False)
		self.set_active(False)
		from i18n import msg0016
		self.set_label(msg0016)
		self.set_use_underline(True)
		from SCRIBES.tooltips import italic_check_button_tip
		self.__editor.tip.set_tip(self, italic_check_button_tip)
		return

	def __syntax_cb(self, *args):
		"""
		Handles callback when bold attribute changes.

		@param self: Reference to the ItalicCheckButton instance.
		@type self: A ItalicCheckButton object.
		"""
		self.__set_button()
		return

	def __set_button(self):
		self.handler_block(self.__toggle_id)
		language = self.__treeview.get_language()
		tag_id = self.__treeview.get_element()
		language_id = language.get_id()
		self.set_active(False)
		value = self.__get_value(language_id, tag_id)
		if self.__treeview.is_parent():
			self.set_active(False)
		elif value is None:
			style = language.get_tag_style(tag_id)
			self.set_active(style.italic)
		elif value:
			self.set_active(True)
		else:
			self.set_active(False)
		self.handler_unblock(self.__toggle_id)
		return

	def __get_value(self, language, keyword):
		value = None
		keyword_list = self.__get_keyword_styles(language, keyword)
		if not keyword_list: return value
		value = keyword_list[3]
		return value

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

	def __update_database(self, language, keyword, value):
		keyword_list = self.__get_keyword_styles(language, keyword)
		if keyword_list:
			keyword_list = [keyword_list[0], keyword_list[1], keyword_list[2], value, keyword_list[4]]
		else:
			keyword_list = [None, None, None, value, None]
		from SyntaxColorsMetadata import set_value
		set_value(language, keyword, keyword_list)
		return

	def __toggled_cb(self, button):
		"""
		Handles callback when the "toggled" signal is emitted.

		@param self: Reference to the ItalicCheckButton instance.
		@type self: A ItalicCheckButton object.

		@param button: Reference to the ItalicCheckButton.
		@type button: A ItalicCheckButton object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		value = self.get_active()
		language = self.__treeview.get_language()
		tag_id = self.__treeview.get_element()
		language_id = language.get_id()
		if language is None or tag_id is None: return True
		self.__update_database(language_id, tag_id, value)
		self.__treeview.grab_focus()
		return True

	def __button_cursor_changed(self, treeview):
		"""
		Handles callback when the "cursor-changed" signal is emitted.

		@param self: Reference to the ItalicCheckButton instance.
		@type self: A ItalicCheckButton object.

		@param treeview: The color editor's treeview.
		@type treeview: A ColorEditorTreeView object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		if treeview.is_parent():
			self.set_property("sensitive", False)
			self.__set_button()
		else:
			self.set_property("sensitive", True)
			self.__set_button()
		return True

	def __destroy_cb(self, color_editor):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the BoldCheckButton instance.
		@type self: A BoldCheckButton object.

		@param color_editor: Reference to the ColorEditor
		@type color_editor: A ColorEditor object.
		"""
		self.__editor.disconnect_signal(self.__sig_id_1, self.__treeview)
		self.__editor.disconnect_signal(self.__sig_id_2, color_editor)
		self.__editor.disconnect_signal(self.__toggle_id, self)
		self.destroy()
		from gnomevfs import monitor_cancel
		if self.__monitor_id: monitor_cancel(self.__monitor_id)
		self = None
		del self
		return
