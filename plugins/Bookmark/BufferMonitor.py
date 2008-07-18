
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
This module documents a class that monitors the buffer for mark updates. When
marks are added or removed from the buffer, the "marked-lines" signal is
emitted. The signal lists all bookmarked lines in the buffer.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

class Monitor(object):
	"""
	This class monitors the buffer for mark updates (addition/removal).It emits
	a signal (marked-lines) when marks are updated.
	"""

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = self.__buffer.connect("source-mark-updated", self.__updated_cb)
		self.__sigid3 = manager.connect("gui-created", self.__updated_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__buffer = editor.textbuffer
		return

	def __find_first_mark(self):
		iterator = self.__buffer.get_bounds()[0]
		marks = self.__buffer.get_source_marks_at_iter(iterator, "scribes_bookmark")
		if marks: return marks[0]
		found_mark = self.__buffer.forward_iter_to_source_mark(iterator, "scribes_bookmark")
		if found_mark is False: raise ValueError
		marks = self.__buffer.get_source_marks_at_iter(iterator, "scribes_bookmark")
		return marks[0]

	def __get_all_marks(self, mark):
		marks = []
		append = marks.append
		append(mark)
		while True:
			mark = mark.next("scribes_bookmark")
			if mark is None: break
			append(mark)
		return marks

	def __get_lines_from_marks(self, marks):
		iter_at_mark = self.__buffer.get_iter_at_mark
		get_line_from_mark = lambda mark: iter_at_mark(mark).get_line()
		lines = [get_line_from_mark(mark) for mark in marks]
		return lines

	def __send_marked_lines(self):
		try:
			mark = self.__find_first_mark()
			marks = self.__get_all_marks(mark)
			lines = self.__get_lines_from_marks(marks)
		except ValueError:
			lines = []
		finally:
			self.__manager.emit("marked-lines", tuple(lines))
			self.__editor.refresh()
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__buffer)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __updated_cb(self, *args):
		self.__send_marked_lines()
		return False
