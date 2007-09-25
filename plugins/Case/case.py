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
This module documents a class that performs case changing operations for
the text editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE

class CaseProcessor(GObject):
	"""
	This class implements an object responsible for changing the case of
	selected text in the text editor.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize the object.

		@param self: Reference to the CaseProcessor instance.
		@type self: A CaseProcessor object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		self.__signal_id_1 = self.connect("destroy", self.__destroy_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the object's data attributes.

		@param self: Reference to the CaseProcessor instance.
		@type self: A CaseProcessor object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__signal_id_1 = None
		return

	def __replace_selection_with(self, string):
		"""
		Replace a selection in the text editor's buffer with string.

		@param self: Reference to the CaseProcessor instance.
		@type self: A CaseProcessor object.

		@param string: A string to insert into the text editor's buffer.
		@type string: A String object.
		"""
		begin_iterator, end_iterator = self.__editor.textbuffer.get_selection_bounds()
		begin_offset = begin_iterator.get_offset()
		end_offset = end_iterator.get_offset()
		self.__editor.textbuffer.begin_user_action()
		self.__editor.textbuffer.delete(begin_iterator, end_iterator)
		begin_iterator = self.__editor.textbuffer.get_iter_at_offset(begin_offset)
		self.__editor.textbuffer.insert(begin_iterator, string)
		self.__editor.textbuffer.end_user_action()
		begin_iterator = self.__editor.textbuffer.get_iter_at_offset(begin_offset)
		end_iterator = self.__editor.textbuffer.get_iter_at_offset(end_offset)
		self.__editor.textbuffer.select_range(begin_iterator, end_iterator)
		return

	def upper(self):
		"""
		Convert selected string in the text editor's buffer to uppercase.

		@param self: Reference to the CaseProcessor instance.
		@type self: A CaseProcessor object.
		"""
		selection = self.__editor.textbuffer.get_selection_bounds()
		if selection is None:
			from i18n import msg0001
			self.__editor.feedback.update_status_message(msg0001, "fail")
			return
		text = self.__editor.textbuffer.get_text(selection[0], selection[1])
		unicode_text = text.decode("utf-8")
		if unicode_text.isupper():
			self.lower()
			return
		text = unicode_text.upper()
		text = text.encode("utf-8")
		self.__replace_selection_with(text)
		from i18n import msg0003
		self.__editor.feedback.update_status_message(msg0003, "suceed")
		return

	def lower(self):
		"""
		Convert selected string in the text editor's buffer to lowercase.

		@param self: Reference to the CaseProcessor instance.
		@type self: A CaseProcessor object.
		"""
		selection = self.__editor.textbuffer.get_selection_bounds()
		if selection is None:
			from i18n import msg0001
			self.__editor.feedback.update_status_message(msg0001, "fail")
			return
		text = self.__editor.textbuffer.get_text(selection[0], selection[1])
		unicode_text = text.decode("utf-8")
		if unicode_text.islower():
			self.upper()
			return
		text = unicode_text.lower()
		text = text.encode("utf-8")
		self.__replace_selection_with(text)
		from i18n import msg0005
		self.__editor.feedback.update_status_message(msg0005, "suceed")
		return

	def title(self):
		"""
		Convert selected string in the text editor's buffer to lowercase.

		@param self: Reference to the CaseProcessor instance.
		@type self: A CaseProcessor object.
		"""
		selection = self.__editor.textbuffer.get_selection_bounds()
		if selection is None:
			from i18n import msg0001
			self.__editor.feedback.update_status_message(msg0001, "fail")
			return
		text = self.__editor.textbuffer.get_text(selection[0], selection[1])
		unicode_text = text.decode("utf-8")
		if unicode_text.istitle():
			from i18n import msg0006
			self.__editor.feedback.update_status_message(msg0006, "fail")
			return
		text = unicode_text.title()
		text = text.encode("utf-8")
		self.__replace_selection_with(text)
		from i18n import msg0007
		self.__editor.feedback.update_status_message(msg0007, "suceed")
		return

	def swapcase(self):
		"""
		Convert selected string in the text editor's buffer to swapcase.

		@param self: Reference to the CaseProcessor instance.
		@type self: A CaseProcessor object.
		"""
		selection = self.__editor.textbuffer.get_selection_bounds()
		if selection is None:
			from i18n import msg0001
			self.__editor.feedback.update_status_message(msg0001, "fail")
			return
		text = self.__editor.textbuffer.get_text(selection[0], selection[1])
		unicode_text = text.decode("utf-8")
		text = unicode_text.swapcase()
		text = text.encode("utf-8")
		self.__replace_selection_with(text)
		from i18n import msg0008
		self.__editor.feedback.update_status_message(msg0008, "suceed")
		return

	def __destroy_cb(self, processor):
		"""
		Destroy instance of this class.

		@param self: Reference to the CaseProcessor instance.
		@type self: A CaseProcessor object.

		@param processor: The CaseProcessor.
		@type processor: A CaseProcessor object.
		"""
		if self.__signal_id_1 and self.handler_is_connected(self.__signal_id_1):
			self.disconnect(self.__signal_id_1)
		del self.__signal_id_1, self.__editor, self
		self = None
		return
