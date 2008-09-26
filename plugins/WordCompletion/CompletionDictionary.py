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
		self.__init_attributes()
#		from gobject import idle_add, PRIORITY_LOW
#		idle_add(self.__precompile_methods, priority=PRIORITY_LOW)

	def __init_attributes(self):
		self.__is_updating = False
		self.__dictionary = {}
		return

	def update(self, dictionary):
		if self.__is_updating: return
		self.__is_updating = True
#		from gobject import idle_add, PRIORITY_LOW
#		idle_add(self.__update, dictionary, priority=9999)
		from thread import start_new_thread
		start_new_thread(self.__update, (dictionary,))
		return

	def __update(self, dictionary):
		self.__dictionary.clear()
		self.__dictionary.update(dictionary)
		self.__is_updating = False
		return False

	def get_dictionary(self):
		return self.__dictionary
