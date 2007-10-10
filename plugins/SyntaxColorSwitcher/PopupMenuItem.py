# -*- coding: utf-8 -*-
# Copyright © 2007 Lateef Alabi-Oki
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
This module documents a class that shows the menu to set or switch
syntax colors.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import ImageMenuItem

class HighlightPopupMenuItem(ImageMenuItem):
	"""
	This class constructs the menu item to set or switch syntax colors.
	"""

	def __init__(self, manager, editor):
		"""
		Initialize the object.

		@param self: Reference to the HighlightPopupMenuItem instance.
		@type self: A HighlightPopupMenuItem object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		from i18n import msg0001
		ImageMenuItem.__init__(self, msg0001)
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__signal_id_1 = self.__editor.textview.connect("focus-in-event", self.__destroy_cb)

	def __init_attributes(self, manager, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the HighlightPopupMenuItem instance.
		@type self: A HighlightPopupMenuItem object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		from i18n import msg0002
		from gtk import Menu, Image, RadioMenuItem
		self.__image = Image()
		self.__editor = editor
		self.__manager = manager
		self.__menu = Menu()
		self.__block = False
		self.__is_active = False
		self.__none_menuitem = RadioMenuItem(label=msg0002)
		self.__language_dictionary = self.__create_language_dictionary()
		self.__language = self.__get_active_language()
		return

	def __set_properties(self):
		"""
		Set default properties.

		@param self: Reference to the HighlightPopupMenuItem instance.
		@type self: A HighlightPopupMenuItem object.
		"""
		from gtk import STOCK_SELECT_COLOR
		self.__image.set_property("stock", STOCK_SELECT_COLOR)
		self.__block = True
		self.__none_menuitem.set_property("active", True)
		self.__block = False
		self.__none_menuitem.connect("activate", self.__activate_cb)
		self.set_image(self.__image)
		self.set_submenu(self.__menu)
		self.__menu.append(self.__none_menuitem)
		for category in self.__language_dictionary.keys():
			self.__create_submenus(category)
		return

	def __create_language_dictionary(self):
		"""
		Create a dictionary of languages.

		@param self: Reference to the HighlightPopupMenuItem instance.
		@type self: A HighlightPopupMenuItem object.

		@return: A language dictionary.
		@rtype: A Dictionary object.
		"""
		dictionary = {}
		from operator import contains
		from gtksourceview import SourceLanguagesManager
		for language in SourceLanguagesManager().get_available_languages():
			category = language.get_section()
			if contains(dictionary.keys(), category):
				language_list = dictionary[category]
				language_list.append(language)
				dictionary[category] = language_list
			else:
				dictionary[category] = [language]
		return dictionary

	def __create_submenus(self, category):
		"""
		Create submenus for category and languages.

		@param self: Reference to the HighlightPopupMenuItem instance.
		@type self: A HighlightPopupMenuItem object.

		@param category: A language category.
		@type category: A Category object.
		"""
		self.__block = True
		from gtk import Menu, MenuItem, RadioMenuItem
		from operator import eq, not_
		menuitem = MenuItem(category)
		self.__menu.append(menuitem)
		menu = Menu()
		menuitem.set_submenu(menu)
		for language in self.__language_dictionary[category]:
			name = language.get_id()
			radio_menuitem = RadioMenuItem(self.__none_menuitem, language.get_name())
			radio_menuitem.set_data("language", language)
			menu.append(radio_menuitem)
			self.__set_active_radio_button(radio_menuitem, language)
			radio_menuitem.connect("activate", self.__activate_cb)
		self.__block = False
		return

	def __set_active_radio_button(self, menuitem, language):
		from operator import eq, ne, is_
		if self.__is_active: return
		if is_(self.__language, None): return
		if eq(self.__language, ""):
			self.__is_active = True
			self.__none_menuitem.set_property("active", True)
		elif eq(self.__language, language.get_id()):
			self.__is_active = True
			menuitem.set_property("active", True)
		return

	def __get_active_language(self):
		"""
		Get language information from syntax database.

		@param self: Reference to the HighlightPopupMenuItem instance.
		@type self: A HighlightPopupMenuItem object.

		@return: Language identification of source code color.
		@rtype: A String object.
		"""
		try:
			from operator import not_
			from Exceptions import NoDataError
			from Metadata import get_syntax_language
			if not_(self.__editor.uri): raise NoDataError
			language_id = get_syntax_language(self.__editor.uri)
		except NoDataError:
			try:
				if not_(self.__editor.uri): return None
				language_id = self.__editor.language.get_id()
			except AttributeError:
				language_id = None
		return language_id

	def __destroy_cb(self, *args):
		"""
		Destroy object.

		@param self: Reference to the HighlightPopupMenuItem instance.
		@type self: A HighlightPopupMenuItem object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self.__editor.textview)
		self.__image.destroy()
		self.__menu.destroy()
		self.destroy()
		self = None
		del self
		return

	def __activate_cb(self, menuitem):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the HighlightPopupMenuItem instance.
		@type self: A HighlightPopupMenuItem object.

		@param menuitem: Radio menu items for languages.
		@type menuitem: A RadioMenuItem object.
		"""
		try:
			if self.__block: return
			language = menuitem.get_data("language")
			self.__manager.emit("syntax-update", language)
			from i18n import msg0003
			message = msg0003 % language.get_name()
			self.__editor.feedback.update_status_message(message, "color")
		except:
			self.__manager.emit("syntax-update", None)
			from i18n import msg0004
			self.__editor.feedback.update_status_message(msg0004, "warning")
		return
