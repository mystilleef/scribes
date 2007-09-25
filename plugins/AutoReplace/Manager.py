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
This module documents a class responsible for expanding abbreviations
in the text editor's buffer.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_PYOBJECT

class AutoReplaceManager(GObject):
	"""
	This class implements an object that expands abbreviations in the
	text editor's buffer.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"abbreviations-updated": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"abbreviation-found": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self, editor):
		"""
		Initialize the AutoReplaceManager object.

		@param self: Reference to the AutoReplaceManager instance.
		@type self: An AutoReplaceManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		self.__update_abbreviation_dictionary()
		# Monitor signals.
		self.__signal_id_1 = self.connect("destroy", self.__manager_destroy_cb)
		self.__signal_id_2 = self.__monitor.connect("abbreviation-found", self.__manager_abbreviation_found_cb)
		# Monitor database for changes.
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monitor_id = monitor_add(self.__database_uri, MONITOR_FILE,
					self.__manager_database_changed_cb)

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the AutoReplaceManager instance.
		@type self: An AutoReplaceManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		# An object that monitors editor's buffer for abbreviations.
		from Monitor import AutoReplaceMonitor
		self.__monitor = AutoReplaceMonitor(self, editor)
		# An object that expands abbreviations in editor's buffer.
		from Expander import AutoReplaceExpander
		self.__expander = AutoReplaceExpander(self, editor)
		# Path to the abbreviation database.
		from SCRIBES.info import metadata_folder
		self.__database_path = metadata_folder + "abbreviations.gdb"
		from gnomevfs import get_uri_from_local_path
		self.__database_uri = get_uri_from_local_path(self.__database_path)
		# A dictionary containing abbreviations as keys and words to be
		# expanded to as values.
		self.__abbreviation_dictionary = {}
		# Identifier for the destroy signal.
		self.__signal_id_1 = None
		# Identifier for the "abbreviation-found" signal.
		self.__signal_id_2 = None
		# True if auto replacement is enabled.
		self.__is_enabled = True
		self.__monitor_id = None
		return

	def __update_abbreviation_dictionary(self):
		"""
		Generate dictionary from abbreviation database.

		@param self: Reference to the AutoReplaceManager instance.
		@type self: An AutoReplaceManager object.
		"""
		if self.__is_enabled is False:
			return
		self.__abbreviation_dictionary.clear()
		from shelve import open
		from anydbm import error
		try:
			database = open(self.__database_path, flag="r", writeback=False)
		except error:
			database = open(self.__database_path, flag="n", writeback=False)
		except:
			print "Error: Invalid database error."
			return
		if not database.keys():
			database.close()
			return
		for key, value in database.items():
			self.__abbreviation_dictionary[key] = value
		database.close()
		self.emit("abbreviations-updated", self.__abbreviation_dictionary)
		return

########################################################################
#
#					Event and Signal Handlers
#
########################################################################

	def __manager_destroy_cb(self, manager):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the AutoReplaceManager instance.
		@type self: An AutoReplaceManager object.

		@param manager: Reference to the AutoReplaceManager.
		@type manager: An AutoReplaceManager object.
		"""
		from SCRIBES.utils import disconnect_signal, delete_attributes
		self.__abbreviation_dictionary.clear()
		disconnect_signal(self.__signal_id_1, self)
		disconnect_signal(self.__signal_id_2, self.__monitor)
		from gnomevfs import monitor_cancel
		if self.__monitor_id:
			monitor_cancel(self.__monitor_id)
		delete_attributes(self)
		del self
		self = None
		return

	def __manager_abbreviation_found_cb(self, monitor, abbreviation):
		"""
		Handles callback when the "abbreviation-found" signal is emitted.

		@param self: Reference to the AutoReplaceManager instance.
		@type self: An AutoReplaceManager object.

		@param monitor: Reference to the AutoReplaceMonitor.
		@type monitor: An AutoReplaceMonitor object.

		@param abbreviation: An abbreviation eligible for replacement.
		@type abbreviation: A String object.
		"""
		self.emit("abbreviation-found", abbreviation)
		return

	def __manager_database_changed_cb(self, monitor_uri, info_uri, event_type):
		"""
		Handles callback when the abbreviation database is modified.

		@param self: Reference to the AutoReplaceManager instance.
		@type self: An AutoReplaceManager object.

		@param monitor_uri: The uri that is monitored.
		@type monitor_uri: A String object.

		@param info_uri: The uri that is monitored.
		@type info_uri: A String object.

		@param event_type: The type of modification that occured.
		@type event_type: A gnomevfs.MONITOR_EVENT* object.
		"""
		from gnomevfs import MONITOR_EVENT_DELETED
		from gnomevfs import MONITOR_EVENT_CREATED
		from gnomevfs import MONITOR_EVENT_CHANGED
		if event_type in [MONITOR_EVENT_DELETED, MONITOR_EVENT_CREATED, MONITOR_EVENT_CHANGED]:
			self.__update_abbreviation_dictionary()
		return
