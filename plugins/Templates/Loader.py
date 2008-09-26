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
This module documents a class that loads template dictionaries from a
database.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class Loader(object):
	"""
	This class creates an object that loads templates from a database.
	"""

	def __init__(self, editor, manager):
		self.__init_attributes(editor, manager)
		self.__signal_id_1 = manager.connect("destroy", self.__destroy_cb)
		self.__signal_id_2 = editor.connect("loaded-file", self.__loaded_document_cb)
		self.__signal_id_3 = editor.connect("renamed-file", self.__loaded_document_cb)
		# Monitor database for changes.
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monitor_id = monitor_add(self.__database_uri, MONITOR_FILE,
					self.__database_changed_cb)
		self.__load_templates()

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		# Path to the templates database.
		database_path = editor.metadata_folder + "templates.gdb"
		from gnomevfs import get_uri_from_local_path
		self.__database_uri = get_uri_from_local_path(database_path)
		return

	def __load_general_templates(self):
		from Metadata import open_database, basepath
		database = open_database(basepath, "r")
		general = {}
		for element in database.keys():
			if not element.startswith("General|"): continue
			nelement = "General" + element[len("General|"):]
			general[nelement] = database[element][1]
		self.__manager.emit("loaded-general-templates", general)
		database.close()
		return

	def __load_language_templates(self):
		self.__manager.emit("loaded-language-templates", {})
		if self.__editor.uri is None: return
		language = self.__editor.language
		if not language: return
		language_id = language
		string = language_id + "|"
		from Metadata import open_database, basepath
		database = open_database(basepath, "r")
		language = {}
		for element in database.keys():
			if not element.startswith(string): continue
			nelement = language_id + element[len(string):]
			language[nelement] = database[element][1]
		self.__manager.emit("loaded-language-templates", language)
		database.close()
		return

	def __load_templates(self):
		self.__load_general_templates()
		self.__load_language_templates()
		return

	def __destroy_cb(self, manager):
		if self.__monitor_id:
			from gnomevfs import monitor_cancel
			monitor_cancel(self.__monitor_id)
		self.__editor.disconnect_signal(self.__signal_id_1, manager)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__editor)
		del self
		self = None
		return

	def __loaded_document_cb(self, *args):
		self.__load_language_templates()
		return

	def __database_changed_cb(self, monitor_uri, info_uri, event_type):
		from gnomevfs import MONITOR_EVENT_DELETED
		from gnomevfs import MONITOR_EVENT_CREATED
		from gnomevfs import MONITOR_EVENT_CHANGED
		events = [MONITOR_EVENT_CHANGED, MONITOR_EVENT_DELETED, MONITOR_EVENT_CREATED]
		if event_type in events: self.__load_templates()
		return
