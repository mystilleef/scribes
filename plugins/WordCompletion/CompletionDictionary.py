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
This module documents a class that implements a special dictionary
object for Scribes word completion system.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class CompletionDictionary(object):
	"""
	This class implements a special dictionary for Scribes word
	completion system.
	"""

	def __init__(self):
		"""
		Initialize dictionary object.

		@param self: Reference to the CompletionDictionary instance.
		@type self: A CompletionDictionary object.
		"""
		self.__init_attributes()

	def __init_attributes(self):
		"""
		Initialize data attributes.

		@param self: Reference to the CompletionDictionary instance.
		@type self: A CompletionDictionary object.
		"""
		self.__is_updating = False
		self.__dictionary = {}
		return

	def update(self, dictionary):
		"""
		Update completion dictionary.

		@param self: Reference to the CompletionDictionary instance.
		@type self: A CompletionDictionary object.

		@param dictionary: Dictionary of words
		@type dictionary: A Dictionary object.
		"""
		if self.__is_updating: return
		self.__is_updating = True
		self.__dictionary.clear()
		self.__dictionary.update(dictionary)
		self.__is_updating = False
		return

	def get_dictionary(self):
		return self.__dictionary
