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
This module documents a class that deactivates template mode.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

class Deactivator(object):
	"""
	This class creates an object that monitors template boundaries to exit template mode.
	"""

	def __init__(self, editor, manager):
		self.__init_attributes(editor, manager)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("template-boundaries", self.__template_boundaries_cb)
		self.__sigid3 = manager.connect("deactivate-template-mode", self.__deactivate_template_mode_cb)
		self.__sigid4 = editor.connect("cursor-moved", self.__cursor_moved_cb)
		self.__sigid5 = manager.connect("last-placeholder", self.__last_placeholder_cb)
		self.__sigid6 = editor.textbuffer.connect("insert-text", self.__insert_text_cb)
		self.__block_signal()
#		from gobject import idle_add
#		idle_add(self.__precompile_methods, priority=5000)

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		self.__boundaries_dictionary = {}
		self.__placeholder_dictionary = {}
		self.__enable = False
		self.__block = False
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		self.__editor.disconnect_signal(self.__sigid6, self.__editor.textbuffer)
		del self
		self = None
		return

	def __precompile_methods(self):
		methods = [self.__cursor_moved_cb, self.__insert_text_cb,
			self.__is_within_range, self.__is_inside_range,
			self.__check_boundary, self.__check_placeholder_boundary,
			self.__deactivate_template_mode_cb, self.__block_signal,
			self.__unblock_signal]
		self.__editor.optimize(methods)
		return False

################################################################################
#
#						Placeholder Manipulation Methods.
#
################################################################################

	def __iter_at_marks(self, marks):
		start = self.__editor.textbuffer.get_iter_at_mark(marks[0])
		end = self.__editor.textbuffer.get_iter_at_mark(marks[1])
		return start, end

	def __is_within_range(self, boundary):
		start, end = self.__iter_at_marks(boundary)
		if self.__editor.cursor.compare(start) == -1: return False
		if self.__editor.cursor.compare(end) == 1: return False
		return True

	def __is_inside_range(self, boundary):
		if len(boundary) == 2:
			start, end = self.__iter_at_marks(boundary)
			if self.__editor.cursor.in_range(start, end): return True
			if self.__editor.cursor.equal(start): return True
			if self.__editor.cursor.equal(end): return True
		else:
			start = self.__editor.textbuffer.get_iter_at_mark(boundary[0])
			if self.__editor.cursor.equal(start): return True
		return False

	def __check_boundary(self):
		if not len(self.__boundaries_dictionary): return False
		boundary = self.__get_current_boundary()
		if not boundary: return False
		if self.__is_within_range(boundary): return False
		self.__manager.emit("deactivate-template-mode")
		return False

	def __check_placeholder_boundary(self):
		if not len(self.__placeholder_dictionary): return False
		boundary = self.__get_placeholder_boundary()
		if not boundary: return False
		if len(boundary) > 2: return False
		if not self.__is_inside_range(boundary): return False
		self.__manager.emit("deactivate-template-mode")
		return False

	def __get_current_boundary(self):
		key = len(self.__boundaries_dictionary)
		boundary = self.__boundaries_dictionary[key]
		return boundary

	def __get_placeholder_boundary(self):
		key = len(self.__placeholder_dictionary)
		boundary = self.__placeholder_dictionary[key]
		return boundary

	def __remove_recent_boundary(self):
		boundary = self.__get_current_boundary()
		key = len(self.__boundaries_dictionary)
		del self.__boundaries_dictionary[key]
		return False

	def __remove_placeholder_boundary(self):
		boundary = self.__get_placeholder_boundary()
		key = len(self.__placeholder_dictionary)
		del self.__placeholder_dictionary[key]
		return False

	def __update_boundaries_dictionary(self, boundary):
		key = len(self.__boundaries_dictionary) + 1
		self.__boundaries_dictionary[key] = boundary
		return False

	def __update_placeholder_dictionary(self, boundary):
		key = len(self.__placeholder_dictionary) + 1
		self.__placeholder_dictionary[key] = boundary
		return False

################################################################################
#
#						Block and Unblock Signals
#
################################################################################

	def __block_signal(self):
		if self.__block: return
		self.__editor.handler_block(self.__sigid4)
		self.__editor.textbuffer.handler_block(self.__sigid6)
		self.__block = True
		return

	def __unblock_signal(self):
		if self.__block is False: return
		self.__editor.handler_unblock(self.__sigid4)
		self.__editor.textbuffer.handler_unblock(self.__sigid6)
		self.__block = False
		return

################################################################################
#
#						Event and Signal Handler
#
################################################################################

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __template_boundaries_cb(self, manager, boundary):
		self.__update_boundaries_dictionary(boundary)
		self.__enable = True
		self.__unblock_signal()
		return False

	def __last_placeholder_cb(self, manager, boundary):
		self.__update_placeholder_dictionary(boundary)
		return False

	def __deactivate_template_mode_cb(self, *args):
		self.__remove_recent_boundary()
		self.__remove_placeholder_boundary()
		self.__check_boundary()
		if len(self.__boundaries_dictionary): return False
		self.__block_signal()
		return False

	def __cursor_moved_cb(self, *args):
		if self.__enable is False: return False
#		try:
#			from gobject import idle_add, source_remove
#			source_remove(self.__cursorid)
#		except AttributeError:
#			pass
#		self.__cursorid = idle_add(self.__check_boundary, priority=9999)
		self.__check_boundary()
		return False

	def __insert_text_cb(self, *args):
		if self.__enable is False: return False
#		try:
#			from gobject import idle_add, source_remove
#			source_remove(self.__insertid)
#		except AttributeError:
#			pass
#		self.__insertid = idle_add(self.__check_placeholder_boundary, priority=9999)
		self.__check_placeholder_boundary()
		return False
