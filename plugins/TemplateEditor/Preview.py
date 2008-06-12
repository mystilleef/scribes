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

from gtksourceview2 import View, Buffer

class Preview(View):
	"""
	This class implements the preview window for the template editor.
	"""

	def __init__(self, manager, editor):
		View.__init__(self, Buffer())
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("description-view-sensitivity", self.__sensitivity_cb)
		self.__sigid3 = manager.connect("template-selected", self.__template_selected_cb)
		self.__sigid4 = manager.connect("language-selected", self.__language_selected_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__buffer = self.get_property("buffer")
		return

	def __set_properties(self):
		scroll = self.__manager.glade.get_widget("ScrollWin")
		scroll.add(self)
		self.set_property("auto-indent", False)
		self.set_property("show-line-numbers", False)
		self.set_property("show-right-margin", False)
		self.__buffer.set_highlight_syntax(False)
#		self.__buffer.set_property("check-brackets", False)
		scheme = self.__buffer.get_style_scheme()
		self.__buffer.set_style_scheme(scheme)
		self.set_property("cursor-visible", False)
		self.set_property("editable", False)
		self.set_property("sensitive", False)
		value = self.__editor.textview.get_right_margin()
		self.set_right_margin(value)
		value = self.__editor.textview.get_show_right_margin()
		self.set_show_right_margin(value)
		value = self.__editor.textview.get_tab_width()
		self.set_tab_width(value)
		self.set_indent_width(-1)
		value = self.__editor.textview.get_insert_spaces_instead_of_tabs()
		self.set_insert_spaces_instead_of_tabs(value)
		value = self.__editor.textview.get_pango_context().get_font_description()
		self.modify_font(value)
		value = self.__editor.textview.get_wrap_mode()
		self.set_wrap_mode(value)
		return

	def __activate_syntax_highlight(self, language_id):
		self.__buffer.set_highlight_syntax(False)
		language = self.__editor.language_manager.get_language(language_id)
		if not language: return False
		self.__buffer.set_language(language)
		self.__buffer.set_highlight_syntax(True)
		return False

	def __destroy_cb(self, manager):
		self.__editor.disconnect_signal(self.__sigid1, manager)
		self.__editor.disconnect_signal(self.__sigid2, manager)
		self.__editor.disconnect_signal(self.__sigid3, manager)
		self.__editor.disconnect_signal(self.__sigid4, manager)
		self.destroy()
		self = None
		del self
		return

	def __sensitivity_cb(self, manager, sensitive):
		if sensitive:
			self.set_property("sensitive", sensitive)
		else:
			self.__buffer.set_text("")
			self.set_property("sensitive", sensitive)
		return

	def __set_text(self, data):
		self.set_property("sensitive", False)
		from Metadata import get_value
		language, key = data
		template = get_value(key)[1]
		self.__buffer.set_text(template)
		self.set_property("sensitive", True)
		self.__manager.emit("temp-selected", template)
		return False

	def __template_selected_cb(self, manager, data):
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__id2)
		except AttributeError:
			pass
		finally:
			self.__id2 = idle_add(self.__set_text, data, priority=3333)
		return

	def __language_selected_cb(self, manager, language):
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__id1)
		except AttributeError:
			pass
		finally:
			self.__id1 = idle_add(self.__activate_syntax_highlight, language, priority=5555)
		return
