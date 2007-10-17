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

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_STRING

class Store(GObject):
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

	__gsignals__ = {
		"updated": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_STRING,)),
	}

	def __init__(self, editor):
		"""
		Initialize an instance of this class.

		@param self: Reference to the Store instance.
		@type self: A Store object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		self.__signal_id_1 = self.__editor.connect_after("close-document", self.__close_document_cb)
		self.__signal_id_2 = self.__editor.connect_after("close-document-no-save", self.__close_document_cb)

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
		try:
			store_id = None
			from types import StringType
			if type(name) is not StringType:
				from types import UnicodeType
				if type(name) is not UnicodeType:
					raise TypeError
			if (name,) in self.__object_dictionary.keys():
				raise ValueError
			self.__object_dictionary[(name,)] = instance
			store_id = self.__editor.generate_random_number(self.__object_id_dictionary.keys())
			self.__object_id_dictionary[store_id] = name
			self.emit("updated", name)
		except ValueError:
			print "Error: '%s' is already in use." % (name)
		except TypeError:
			print "Error: '%s' is not a string." % (name)
		return store_id

	def remove_object(self, name, stored_id):
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
		try:
			if not stored_id in self.__object_id_dictionary.keys():
				print "Stored ID error", name
				raise ValueError
			if name != self.__object_id_dictionary[stored_id]:
				print "Store Name Error: ", name
				raise ValueError
			del self.__object_dictionary[(name,)]
			del self.__object_id_dictionary[stored_id]
			self.emit("updated", name)
			if self.__can_quit: self.__destroy()
		except KeyError:
			print "Error: Object associated with '%s' not found." % (name)
		except ValueError:
			print "Error: Invalid ID"
		except AttributeError:
			pass
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
			instance = None
			instance = self.__object_dictionary[(name,)]
		except KeyError:
			pass
		return instance

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

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the Store instance.
		@type self: A Store object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__object_dictionary = {}
		self.__object_id_dictionary = {}
		self.__registration_id = editor.register_termination_id()
		self.__can_quit = False
		return

	def __destroy(self):
		"""
		Destroy the store object, and disconnect all signals.

		@param self: Reference to the Store instance.
		@type self: A Store object.
		"""
		#if self.__object_dictionary: return
		# Disconnect signals.
		self.__editor.disconnect_signal(self.__signal_id_1, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__editor)
		self.__object_dictionary.clear()
		self.__object_id_dictionary.clear()
		# Unregister object so that editor can quit.
		self.__editor.unregister_termination_id(self.__registration_id)
		del self
		self = None
		return

	def __close_document_cb(self, editor):
		"""
		Handles callback when the "close-document" signal is emitted.

		@param self: Reference to the Store instance.
		@type self: A Store object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__can_quit = True
		return
