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
This module documents a class that manages a menu that allows users to
set or switch syntax colors for different source code types.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_PYOBJECT

class Manager(GObject):
	"""
	This class manages a group of menus that allows users to set or
	switch syntax colors for different source code types.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"syntax-update": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self, editor):
		"""
		Initialize object.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
#		self.__signal_id_1 = editor.textview.connect_after("populate-popup", self.__popup_cb)
		self.__signal_id_2 = self.connect("destroy", self.__destroy_cb)
#		self.__signal_id_3 = self.connect("syntax-update", self.__syntax_update_cb)
#		self.__signal_id_4 = self.__editor.connect("loaded-document", self.__loaded_document_cb)
#		from gobject import idle_add
#		idle_add(self.__set_syntax_highlight)

	def __init_attributes(self, editor):
		"""
		Intialize data attributes.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__signal_id_1 = self.__signal_id_2 = None
		self.__signal_id_3 = self.__signal_id_4 = None
		return

	def __set_syntax_highlight(self):
		"""
		Activate syntax color highlight based on information in syntax
		database.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		try:
			from operator import not_, ne, eq
			from Exceptions import NoDataError
			from Metadata import get_syntax_language
			if not_(self.__editor.uri): return False
			language_id = get_syntax_language(self.__editor.uri)
			try:
				if eq(self.__editor.language.get_id(), language_id): return False
			except AttributeError:
				pass
			if not_(language_id):
				self.__editor.textbuffer.set_highlight(False)
			else:
				from gtksourceview import SourceLanguagesManager
				for language in SourceLanguagesManager().get_available_languages():
					if ne(language.get_id(), language_id): continue
					from gobject import idle_add
					from Syntax import activate_syntax_highlight
					idle_add(activate_syntax_highlight, self.__editor.textbuffer, language)
					break
		except NoDataError:
			return False
		return False

	def __destroy_cb(self, *args):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
#		self.__editor.disconnect_signal(self.__signal_id_1, self.__editor.textview)
		self.__editor.disconnect_signal(self.__signal_id_2, self)
#		self.__editor.disconnect_signal(self.__signal_id_3, self)
#		self.__editor.disconnect_signal(self.__signal_id_4, self.__editor)
		del self
		self = None
		return

	def __popup_cb(self, textview, menu):
		"""
		Handles callback when the "populate-popup" signal is emitted.

		@param self: Reference to the Manager instance.
		@type self: An Manager object.

		@param textview: Reference to the editor's textview.
		@type textview: A ScribesTextView object.

		@param menu: Reference to the editor's popup menu.
		@type menu: A gtk.Menu object.
		"""
		from PopupMenuItem import HighlightPopupMenuItem
		menu.prepend(HighlightPopupMenuItem(self, self.__editor))
		menu.show_all()
		return False

	def __syntax_update_cb(self, manager, language):
		"""
		Handles callback when the "syntax-update" signal is emitted.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param language: An object containing language information.
		@type language: A gtksourceview.SourceLanguage object.
		"""
		from operator import not_
		if not_(language):
			self.__editor.textbuffer.set_highlight(False)
			if self.__editor.uri:
				from Metadata import update_database
				from gobject import idle_add
				idle_add(update_database, self.__editor.uri, "")
		else:
			from Syntax import activate_syntax_highlight
			from gobject import idle_add
			idle_add(activate_syntax_highlight, self.__editor.textbuffer, language)
			if self.__editor.uri:
				from Metadata import update_database
				from gobject import idle_add
				idle_add(update_database, self.__editor.uri, language.get_id())
		return

	def __loaded_document_cb(self, *args):
		"""
		Handles callback when the "loaded-document" signal is emitted.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		from gobject import idle_add
		idle_add(self.__set_syntax_highlight)
		return
