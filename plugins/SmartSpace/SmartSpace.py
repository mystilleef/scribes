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
This module documents a class that smartly unindents text indented with
white spaces. This is a port of Gedit's smart space plugin. All credit
goes to

Copyright (C) 2007 - Steve Frécinaux

@author: Lateef Alabi-Oki, Paolo Borelli, Steve Frécinaux
@organization: The Scribes Project
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

class SmartSpace(object):
	"""
	This class draws white spaces in the buffer.
	"""

	def __init__(self, editor, manager):
		"""
		Initialize object.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(editor, manager)
		self.__sig_id1 = self.__textview.connect('key-press-event', self.__key_press_event_cb)
		self.__sig_id2 = manager.connect("destroy", self.__destroy_cb)
		self.__sig_id3 = manager.connect("activate", self.__activate_cb)
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__precompile_method, priority=PRIORITY_LOW)

	def __init_attributes(self, editor, manager):
		"""
		Initialize data attributes.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__manager = manager
		self.__textview = editor.textview
		self.__activate = False
		self.__blocked = False
		return

	def __block_event_after_signal(self):
		if self.__blocked: return
		self.__textview.handler_block(self.__sig_id1)
		self.__blocked = True
		return

	def __unblock_event_after_signal(self):
		if self.__blocked is False: return
		self.__textview.handler_unblock(self.__sig_id1)
		self.__blocked = False
		return

	def __check_event_signal(self):
		if self.__activate:
			self.__unblock_event_after_signal()
		else:
			self.__block_event_after_signal()
		self.__textview.queue_draw()
		return

	def __precompile_method(self):
		try:
			from psyco import bind
			bind(self.__key_press_event_cb)
		except ImportError:
			pass
		return False

	def __key_press_event_cb(self, textview, event):
		if self.__activate is False: return False
		from gtk.keysyms import BackSpace
		if event.keyval != BackSpace: return False
		buffer_ = self.__textview.get_buffer()
		if buffer_.get_has_selection(): return False
		iterator = self.__editor.get_cursor_iterator()
		offset = iterator.get_line_offset()
		# We're at the begining of the line, so we can't obviously
		# unindent in this case
		if offset == 0: return False
		start = iterator.copy()
		start.backward_char()
		# If the previous char is a tab, we should just remove it
		if start.get_char() == '\t':
			buffer_.begin_user_action()
			buffer_.delete(start, iterator)
			buffer_.end_user_action()
			return True
		# Otherwise, check how many spaces we're able to remove
		max_move = (offset - 1) % self.__textview.get_tabs_width() + 1
		moved = 0
		while moved < max_move and start.get_char() == ' ':
			start.backward_char()
			moved += 1
		start.forward_char()
		# The iterator hasn't moved, so there is nothing to remove
		if moved == 0: return False
		# Actually delete the spaces
		buffer_.begin_user_action()
		buffer_.delete(start, iterator)
		buffer_.end_user_action()
		return True

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __activate_cb(self, manager, use_tabs):
		self.__activate = not use_tabs
		self.__check_event_signal()
		return False

	def __destroy(self):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		self.__editor.disconnect_signal(self.__sig_id1, self.__textview)
		self.__editor.disconnect_signal(self.__sig_id2, self.__manager)
		self.__editor.disconnect_signal(self.__sig_id3, self.__manager)
		del self
		self = None
		return
