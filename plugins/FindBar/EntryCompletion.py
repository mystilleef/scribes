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
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
This module exposes a class that creates the entry completion object for the
text editor's findbar's text entry widget.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import EntryCompletion

class FindEntryCompletion(EntryCompletion):
	"""
	This class creates the entry completion object for the text editor's findbar
	text entry widget. The class defines the behavior and default properties of
	the entry completion object.
	"""

	def __init__(self, searchmanager):
		"""
		Initialize the entry completion object.

		@param self: Reference to the ScribesFindEntryCompletion instance.
		@type self: A ScribesFindEntryCompletion object.

		@param searchmanager: The text editor's search processing object.
		@type searchmanager: A SearchProcessor object.
		"""
		EntryCompletion.__init__(self)
		self.__init_attributes(searchmanager)
		self.__set_properties()
		self.__update_model()
		self.__signal_id_1 = self.__searchmanager.connect("updated-queries", self.__completion_updated_queries_cb)

	def __init_attributes(self, searchmanager):
		"""
		Initialize the entry completion's attributes.

		@param self: Reference to the ScribesFindEntryCompletion instance.
		@type self: A ScribesFindEntryCompletion object.

		@param searchmanager: The text editor's search processing object.
		@type searchmanager: A SearchProcessor object.
		"""
		self.__searchmanager = searchmanager
		self.__model = self.__create_model()
		self.__signal_id_1 = None
		return

	def __set_properties(self):
		"""
		Define the entry completion's properties.

		@param self: Reference to the ScribesFindEntryCompletion instance.
		@type self: A ScribesFindEntryCompletion object.
		"""
		self.set_property("popup-set-width", False)
		self.set_property("model", self.__model)
		self.set_text_column(0)
		return

	def __create_model(self):
		"""
		Create the model for the entry completion object.

		@param self: Reference to the ScribesFindEntryCompletion instance.
		@type self: A ScribesFindEntryCompletion object.
		"""
		from gtk import ListStore
		from gobject import TYPE_STRING
		model = ListStore(TYPE_STRING)
		return model

	def __update_model(self):
		"""
		Update the entry completion object's model with new values if any.

		@param self: Reference to the ScribesFindEntryCompletion instance.
		@type self: A ScribesFindEntryCompletion object.
		"""
		if self.__searchmanager.queries is None:
			return
		self.__model.clear()
		for item in self.__searchmanager.queries:
			self.__model.append([item])
		return

	def __completion_updated_queries_cb(self, searchmanager):
		"""
		Handles callback when the search processor's "updated-queries" signal is
		emitted.

		@param self: Reference to the ScribesFindEntryCompletion instance.
		@type self: A ScribesFindEntryCompletion object.

		@param searchmanager: The text editor's search processing object.
		@type searchmanager: A SearchProcessor object.
		"""
		self.__update_model()
		return

	def destroy_object(self):
		"""
		Destroy instance of this class.

		@param self: Reference to the FindEntryCompletion instance.
		@type self: A FindEntryCompletion object.
		"""
		from SCRIBES.utils import disconnect_signal, delete_attributes
		disconnect_signal(self.__signal_id_1, self.__searchmanager)
		self.__model.clear()
		delete_attributes(self)
		del self
		self = None
		return
