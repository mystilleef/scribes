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
		self.__buffer = editor.textbuffer
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
		if self.__buffer.get_has_selection(): return False
		iterator = self.__editor.get_cursor_iterator()
		if iterator.starts_line() or iterator.is_start(): return False
		start = iterator.copy()
		while True:
			start.backward_char()
			if start.get_char() != " ": break
			start.forward_char()
			start = self.__get_start_position(start, iterator.get_line_offset())
			break
		self.__buffer.begin_user_action()
		self.__buffer.delete(start, iterator)
		self.__buffer.end_user_action()
		return True

	def __get_start_position(self, start, cursor_offset):
		indentation = self.__textview.get_tabs_width()
		moves = cursor_offset % indentation
		if moves == 0 : moves = indentation
		for value in xrange(moves):
			if start.starts_line(): return start
			start.backward_char()
			if start.get_char() == " ": continue
			start.forward_char()
			break
		return start

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
