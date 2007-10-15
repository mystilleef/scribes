# -*- coding: utf-8 -*-
# Copyright © 2006 Lateef Alabi-Oki
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
This module documents a class that creates a global storage object. The
object provides access to other objects that need to be accessed across
the project. Global storage object is useful to inter-plugin communications.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2006 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class Store(object):
	"""
	This class creates an object that stores objects that can be
	accessed publicly. Each object is associated with a string that
	uniquely identifies it. The "updated" signal is emitted everytime
	an object is added or removed from the store. The purpose of the
	store is for inter-module or inter-plugin communications. Note, all
	objects in the store can be accessed by anyone! Only the client who
	adds and object to the store can remove the same object via a
	unique id.
	"""

	def __init__(self):
		"""
		Initialize an instance of this class.

		@param self: Reference to the Store instance.
		@type self: A Store object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes()

	def __init_attributes(self):
		"""
		Initialize data attributes.

		@param self: Reference to the Store instance.
		@type self: A Store object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__object_dictionary = {}
		return

	def add_object(self, name, instance):
		"""
		Add an object to the store.

		Objects added to the store can only be removed by the client
		who adds it.

		@param self: Reference to the Store instance.
		@type self: A Store object.

		@param name: A unique identifier for an object to be stored.
		@type name: A String object.

		@param instance: An instance of an object.
		@type instance: A Python object.

		@return: A number used to remove objects from the store if necessary
		@rtype: An Integer object.
		"""
		from operator import contains
		from Exceptions import GlobalStoreObjectExistsError
		if contains(self.__object_dictionary.keys(), name): raise GlobalStoreObjectExistsError
		from utils import generate_random_number
		object_id = generate_random_number(map(lambda x: x[1],self.__object_dictionary.values()))
		self.__object_dictionary[name] = instance, object_id
		return object_id

	def remove_object(self, name, object_id):
		"""
		Remove an object from the store.

		Only clients that add objects to the store can remove it.

		@param self: Reference to the Store instance.
		@type self: A Store object.

		@param name: A unique identifier for an object to be removed.
		@type name: A String object.

		@param stored_id: A number used to verify that the client removing the object stored it.
		@type stored_id: An Integer object.
		"""
		from Exceptions import GlobalStoreObjectDoesNotExistError
		from operator import ne
		if ne(object_id, self.__object_dictionary[name][1]): raise GlobalStoreObjectDoesNotExistError
		del self.__object_dictionary[name]
		return

	def get_object(self, name):
		"""
		Get an object from the store.

		@param self: Reference to the Store instance.
		@type self: A Store object.

		@param name: A unique identifier for an object to be retrieved.
		@type name: A String object.

		@return: Return an object associated with a name from the store.
		@rtype: A Python object.
		"""
		try:
			instance = self.__object_dictionary[name]
		except KeyError:
			from Exceptions import GlobalStoreObjectDoesNotExistError
			raise GlobalStoreObjectDoesNotExistError
		return instance[0]

	def list_objects(self):
		"""
		Get all names associated with objects in the store.

		@param self: Reference to the Store instance.
		@type self: A Store object.

		@return: A list of names associated with objects.
		@rtype: A List object.
		"""
		object_names = []
		object_names = self.__object_dictionary.keys()
		object_names.sort()
		return object_names

	def __destroy(self):
		"""
		Destroy the store object, and disconnect all signals.

		@param self: Reference to the Store instance.
		@type self: A Store object.
		"""
		self.__object_dictionary.clear()
		del self
		self = None
		return
