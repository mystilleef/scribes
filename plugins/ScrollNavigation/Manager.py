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
This module documents a class that implements keyboard scroll
operations.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class Manager(object):
	"""
	This class implements keyboard scroll operations.
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
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__precompile_methods, priority=PRIORITY_LOW)

	def __init_attributes(self, editor):
		"""
		Initialize object.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__view = editor.textview
		self.__feedback = editor.feedback
		return

	def __precompile_methods(self):
		"""
		Optimize methods using Psyco

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		try:
			from psyco import bind
			bind(self.scroll_up)
			bind(self.scroll_down)
			bind(self.center)
		except ImportError:
			pass
		return False

########################################################################
#
#							Public Methods
#
########################################################################

	def scroll_up(self):
		"""
		Scroll the view up.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		rectangle = self.__view.get_visible_rect()
		x, y, width, height = rectangle.x, rectangle.y, rectangle.width, rectangle.height
		iterator = self.__view.get_iter_at_location(x, y)
		iterator.backward_line()
		self.__view.scroll_to_iter(iterator, 0.001)
		return

	def scroll_down(self):
		"""
		Scroll the view down.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		rectangle = self.__view.get_visible_rect()
		x, y, width, height = rectangle.x, rectangle.y, rectangle.width, rectangle.height
		iterator = self.__view.get_iter_at_location(x, y+height)
		iterator.forward_line()
		self.__view.scroll_to_iter(iterator, 0.001)
		return

	def center(self):
		"""
		Center view on current line.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		iterator = self.__editor.get_cursor_iterator()
		self.__view.scroll_to_iter(iterator, 0.001, use_align=True, xalign=1.0)
		from i18n import msg0001
		self.__feedback.update_status_message(msg0001, "yes", 5)
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
