# -*- coding: utf-8 -*-
# Copyright © 2008 Lateef Alabi-Oki
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
This module documents a class that indents source code when the tab
key is pressed and unindents it when shift and the tab key is pressed.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

class Manager(object):
	"""
	This class indents source code when the tab key is pressed and
	unindents it when the shift and tab key are pressed.
	"""

	def __init__(self, editor):
		"""
		Initialize object.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(editor)
		self.__sig_id1 = editor.textview.connect("key-press-event", self.__key_press_event_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__buffer = editor.textbuffer
		from gtk.keysyms import Tab, ISO_Left_Tab
		self.__tab_keys = (Tab, ISO_Left_Tab)
		return

	def __key_press_event_cb(self, textview, event):
		if (event.keyval in self.__tab_keys) is False: return False
		if self.__buffer.get_property("has-selection") is False: return False
		if event.keyval == self.__tab_keys[0]:
			self.__editor.trigger("indent_line")
		else:
			self.__editor.trigger("unindent_line")
		return True
