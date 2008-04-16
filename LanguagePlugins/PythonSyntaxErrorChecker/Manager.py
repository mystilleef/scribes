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
This module documents a class that checks python source code for 
syntax errors.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

class Manager(object):
	"""
	This class checks python source code for syntax errors.
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

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		return

	def __move_cursor_to_error_line(self, line):
		iterator = self.__editor.textbuffer.get_iter_at_line(line - 1)
		self.__editor.textbuffer.place_cursor(iterator)
		self.__editor.move_view_to_cursor()
		message = "Syntax error on line " + str(line)
		self.__editor.update_status_message(message, "no", 10)
		return

	def check(self):
		try:
			from compiler import parse
			parse_tree = parse(self.__editor.get_text())
			message = "No syntax errors found"
			self.__editor.update_status_message(message, "yes")
		except SyntaxError:
			from sys import exc_info
			exc = exc_info()[1]
			self.__move_cursor_to_error_line(exc.lineno)
		finally:
			from gc import collect
			collect()
			from sys import exc_clear
			exc_clear()
		return

	def destroy(self):
		"""
		Destroy object.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		del self
		self = None
		return
