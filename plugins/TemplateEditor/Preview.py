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
This module documents a class that implements the preview window for
the template editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtksourceview import SourceView, SourceBuffer

class Preview(SourceView):
	"""
	This class implements the preview window for the template editor.
	"""

	def __init__(self, manager, editor):
		"""
		Initialize object.

		@param self: Reference to the Preview instance.
		@type self: A Preview object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		SourceView.__init__(self, SourceBuffer())
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__signal_id_1 = manager.connect("destroy", self.__destroy_cb)
		self.__signal_id_2 = manager.connect("description-treeview-sensitivity", self.__sensitivity_cb)
		self.__signal_id_3 = manager.connect("template-selected", self.__template_selected_cb)
		self.__signal_id_4 = manager.connect("language-selected", self.__language_selected_cb)

	def __init_attributes(self, manager, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the Preview instance.
		@type self: A Preview object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__manager = manager
		self.__editor = editor
		self.__buffer = self.get_property("buffer")
		self.__client = editor.gconf_client
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		return

	def __set_properties(self):
		"""
		Set default properties.

		@param self: Reference to the Preview instance.
		@type self: A Preview object.
		"""
		self.set_property("auto-indent", False)
		self.set_property("show-line-markers", False)
		self.set_property("show-line-numbers", False)
		self.set_property("show-margin", False)
		self.__buffer.set_property("highlight", False)
		self.__buffer.set_property("check-brackets", False)
		self.set_property("cursor-visible", False)
		self.set_property("editable", False)
		self.set_property("sensitive", False)
		tab_width = 4
		if self.__client.get("/apps/scribes/tab"):
			tab_width = self.__client.get_int("/apps/scribes/tab")
		self.set_tabs_width(tab_width)
		use_tabs = True
		if self.__client.get("/apps/scribes/use_tabs"):
			use_tabs = self.__client.get_bool("/apps/scribes/use_tabs")
		self.set_insert_spaces_instead_of_tabs(not use_tabs)
		gconf_font = "Monospace 12"
		if self.__client.get("/apps/scribes/font"):
			gconf_font = self.__client.get_string("/apps/scribes/font")
		from pango import FontDescription
		font = FontDescription(gconf_font)
		self.modify_font(font)
		wrap_mode_bool = True
		if self.__client.get("/apps/scribes/text_wrapping"):
			wrap_mode_bool = self.__client.get_bool("/apps/scribes/text_wrapping")
		use_theme_colors = True
		if self.__client.get("/apps/scribes/use_theme_colors"):
			use_theme_colors = self.__client.get_bool("/apps/scribes/use_theme_colors")
		from gtk import WRAP_WORD, WRAP_NONE
		if wrap_mode_bool:
			self.set_wrap_mode(WRAP_WORD)
		else:
			self.set_wrap_mode(WRAP_NONE)
		if use_theme_colors is False:
			# Use foreground and background colors specified by the user stored
			# in GConf, the GNOME configuration database.
			from gconf import VALUE_STRING
			fgcolor = "#000000"
			bgcolor = "#ffffff"
			if self.__client.get("/apps/scribes/fgcolor"):
				fgcolor = self.__client.get_string("/apps/scribes/fgcolor")
			if self.__client.get("/apps/scribes/bgcolor"):
				bgcolor = self.__client.get_string("/apps/scribes/bgcolor")
			from gtk.gdk import color_parse
			foreground_color = color_parse(fgcolor)
			background_color = color_parse(bgcolor)
			from gtk import STATE_NORMAL
			self.modify_base(STATE_NORMAL, background_color)
			self.modify_text(STATE_NORMAL, foreground_color)
		return

	def __activate_syntax_highlight(self, language_id):
		"""
		Toggle syntax highlight on for a particular language.

		@param self: Reference to the TemplateEditorTextView instance.
		@type self: A TemplateEditorTextView object.

		@param language_id: An identification for a particular language.
		@type language_id: A String object.
		"""
		self.__buffer.set_property("highlight", True)
		from gtksourceview import SourceLanguage, SourceLanguagesManager
		manager = SourceLanguagesManager()
		languages = manager.get_available_languages()
		from operator import eq
		for language in languages:
			if eq(language.get_id(), language_id):
				break
		from SCRIBES.syntax import activate_syntax_highlight
		activate_syntax_highlight(self.__buffer, language)
		return

	def __destroy_cb(self, manager):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the Preview instance.
		@type self: A Preview object.

		@param manager: Reference to the TemplateManager
		@type manager: A TemplateManager object.
		"""
		from SCRIBES.utils import delete_attributes, disconnect_signal
		disconnect_signal(self.__signal_id_1, manager)
		disconnect_signal(self.__signal_id_2, manager)
		disconnect_signal(self.__signal_id_3, manager)
		disconnect_signal(self.__signal_id_4, manager)
		self.destroy()
		delete_attributes(self)
		self = None
		del self
		return

	def __sensitivity_cb(self, manager, sensitive):
		"""
		Handles callback when the "description-treeview-sensitivity" is emitted.

		@param self: Reference to the Preview instance.
		@type self: A Preview object.

		@param manager: Reference to the TemplateManager
		@type manager: A TemplateManager object.

		@param sensitive: Whether or not the description treeview is sensitive.
		@type sensitive: A Boolean object.
		"""
		if sensitive:
			self.set_property("sensitive", sensitive)
		else:
			self.__buffer.set_text("")
			self.set_property("sensitive", sensitive)
		return

	def __template_selected_cb(self, manager, data):
		"""
		Handles callback when the "template-selected" signal is emitted.

		@param self: Reference to the Preview instance.
		@type self: A Preview object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param data: A tuple represent a template trigger and its language category.
		@type data: A tuple object.
		"""
		self.__buffer.set_text("")
		self.set_property("sensitive", False)
		from operator import ne
		language, trigger = data
		database_key = language + trigger
		from Metadata import open_template_database
		from Metadata import close_template_database
		database = open_template_database()
		for key in database.keys():
			if ne(key, database_key): continue
			template = database[key][1]
			self.__buffer.set_text(template)
			break
		close_template_database(database)
		self.set_property("sensitive", True)
		return

	def __language_selected_cb(self, manager, language):
		"""
		Handles callback when the "language-selected" signal is emitted.

		@param self: Reference to the Preview instance.
		@type self: A Preview object.

		@param manager: Reference to the TemplateManager
		@type manager: A TemplateManager object.

		@param language: A language.
		@type language: A String object.
		"""
		from operator import eq
		if eq(language, "General"):
			self.__buffer.set_property("highlight", False)
		else:
			self.__activate_syntax_highlight(language)
		return
