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
This module documents as class that saves files to a local or remote
location.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class OutputProcessor(object):
	"""
	This class creates an instance that saves files to local or remote
	locations.
	"""

	def __init__(self, dbus):
		"""
		Initialize this object.

		@param self: Reference to the OutputProcessor instance.
		@type self: An OutputProcessor object.
		"""
		self.__init_attributes(dbus)

	def __init_attributes(self, dbus):
		self.__dbus = dbus
		self.__file_dictionary = None
		self.__queue = []
		self.__is_busy = False
		return

	def process(self, editor_id, text, uri, encoding):
		try:
			if self.__is_busy: raise ValueError
			self.__is_busy = True
			self.__check_permissions()
			swap_file = self.__get_swap_file(editor_id)
			encoded_text = self.__encode_text()
			self.__save_file(editor_id, uri, encoded_text, swap_file)
		except ValueError:
			self.__queue.append((editor_id, text, uri, encoding))
		return

	def __check_permissions(self):
		return

	def __check_swap_file(self):
		return None

	def __encode_text(self):
		return None

	def __save_file(self, editor_id, uri, encoded_text, swap_file):
		return
