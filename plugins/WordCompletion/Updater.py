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
This module documents a class that updates the word completion dictionary
when text is entered into the text editor's buffer.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

indexer_dbus_service = "org.sourceforge.ScribesIndexer"
indexer_dbus_path = "/org/sourceforge/ScribesIndexer"

class CompletionUpdater(object):
	"""
	This class creates an object updates the word completion dictionary
	when the buffer is modified.
	"""

	def __init__(self, manager, editor):
		"""
		Initialize object.

		@param self: Reference to the CompletionUpdater instance.
		@type self: A CompletionUpdater object.

		@param manager: Reference to the CompletionManager instance.
		@type manager: A CompletionManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(manager, editor)
		from thread import start_new_thread
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__start_indexer)
		idle_add(self.__precompile_methods, priority=PRIORITY_LOW)
		self.__signal_id_1 = self.__editor.connect("loaded-document", self.__loaded_document_cb)
		self.__signal_id_2 = self.__editor.textbuffer.connect_after("changed", self.__changed_cb)
		self.__signal_id_3 = self.__manager.connect("destroy", self.__destroy_cb)
		self.__signal_id_4 = self.__editor.connect("renamed-document", self.__loaded_document_cb)
		editor.session_bus.add_signal_receiver(self.__name_change_cb,
						'NameOwnerChanged',
						'org.freedesktop.DBus',
						'org.freedesktop.DBus',
						'/org/freedesktop/DBus',
						arg0=indexer_dbus_service)
		editor.session_bus.add_signal_receiver(self.__finished_indexing_cb,
						signal_name="finished_indexing",
						dbus_interface=indexer_dbus_service)

	def __init_attributes(self, manager, editor):
		"""
		Initialize data attributes.
		@param self: Reference to the CompletionUpdater instance.
		@type self: A CompletionUpdater object.

		@param manager: Reference to the CompletionManager instance.
		@type manager: A CompletionManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		from os.path import join, split
		self.__indexer_cwd = split(globals()["__file__"])[0]
		self.__indexer_executable = join(self.__indexer_cwd, "Indexer.py")
		from sys import prefix
		self.__python_executable = prefix + "/bin" + "/python"
		self.__editor = editor
		self.__manager = manager
		self.__timer = None
		self.__indexer = None
		self.__is_indexing = False
		self.__signal_id_1 = self.__signal_id_2 = None
		self.__signal_id_3 = self.__signal_id_4 = None
		return

########################################################################
#
#						Helper Methods
#
########################################################################

	def __index(self):
		"""
		Generate word completion dictionary.

		@param self: Reference to the CompletionUpdater instance.
		@type self: A CompletionUpdater object.
		"""
		from operator import is_, truth
		if truth(self.__editor.is_readonly): return False
		if is_(self.__indexer, None):
			from gobject import idle_add
			idle_add(self.__start_indexer)
			return False
		self.__remove_timer()
		from gobject import timeout_add, PRIORITY_LOW
		self.__timer = timeout_add(500, self.__generate_dictionary, priority=PRIORITY_LOW)
		return False

	def __generate_dictionary(self):
		"""
		Generate word completion dictionary.

		Send text to the indexer, an external process, to generate
		a list of words for automatic completion.

		@param self: Reference to the CompletionUpdater instance.
		@type self: A CompletionUpdater object.
		"""
		if self.__is_indexing:
			from gobject import idle_add, PRIORITY_LOW
			try:
				source_remove(self.__index_timer)
			except Exception:
				pass
			self.__index_timer = idle_add(self.__index, priority=PRIORITY_LOW)
		else:
			from operator import not_
			if not_(self.__indexer): return
			self.__is_indexing = True
			self.__indexer.process(self.__get_text(), self.__editor.id,
					dbus_interface=indexer_dbus_service,
					reply_handler=self.__reply_handler_cb,
					error_handler=self.__error_handler_cb)
		return False

	def __start_indexer(self):
		"""
		Start the word completion indexer and get a reference to it.

		@param self: Reference to the CompletionUpdater instance.
		@type self: A CompletionUpdater object.
		"""
		try:
			from dbus import DBusException
			from SCRIBES.info import dbus_iface, session_bus, python_path
			services = dbus_iface.ListNames()
			from operator import contains
			self.__indexer = None
			if contains(services, indexer_dbus_service):
				self.__indexer = session_bus.get_object(indexer_dbus_service, indexer_dbus_path)
				from gobject import idle_add, PRIORITY_LOW
				try:
					source_remove(self.__index_timer)
				except Exception:
					pass
				self.__index_timer = idle_add(self.__index, priority=PRIORITY_LOW)
			else:
				from gobject import spawn_async
				spawn_async([self.__python_executable, self.__indexer_executable, python_path], working_directory=self.__indexer_cwd)
		except DBusException:
			pass
		return False

	def __get_text(self):
		"""
		Get text from all editors.

		@param self: Reference to the CompletionUpdater instance.
		@type self: A CompletionUpdater object.

		@return: text to index.
		@rtype: A String object.
		"""
		get_text = lambda editor: editor.get_text()
		all_text = map(get_text, self.__editor.get_editor_instances())
		return " ".join(all_text)

	def __remove_timer(self):
		"""
		Remove timer assocated with a time out function callback.

		@param self: Reference to the CompletionUpdater instance.
		@type self: A CompletionUpdater object.
		"""
		try:
			from gobject import source_remove
			source_remove(self.__timer)
		except:
			pass
		return

########################################################################
#
#					Signal and Event Handlers
#
########################################################################

	def __changed_cb(self, textbuffer):
		"""
		Handles callback when the "changed" signal is emitted.

		@param self: Reference to the CompletionUpdater instance.
		@type self: A CompletionUpdater object.

		@param textbuffer: Reference to the text editor's buffer.
		@type textbuffer: A ScribesTextBuffer object.
		"""
		from gobject import idle_add, PRIORITY_LOW
		try:
			source_remove(self.__index_timer)
		except Exception:
			pass
		self.__index_timer = idle_add(self.__index, priority=PRIORITY_LOW)
		return False

	def __loaded_document_cb(self, editor, uri):
		"""
		Handles callback when the "loaded-document" signal is emitted.

		@param self: Reference to the CompletionUpdater instance.
		@type self: A CompletionUpdater object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		from gobject import idle_add, PRIORITY_LOW
		try:
			source_remove(self.__index_timer)
		except Exception:
			pass
		self.__index_timer = idle_add(self.__index, priority=PRIORITY_LOW)
		return

	def __name_change_cb(self, *args):
		"""
		Callback when the indexing process dies.

		@param self: Reference to the CompletionUpdater instance.
		@type self: A CompletionUpdater object.

		@param *args: Useless arguments.
		@type *args: A List object.
		"""
		from gobject import idle_add
		idle_add(self.__start_indexer)
		return

	def __reply_handler_cb(self, *args):
		"""
		Successful message from the indexer

		@param self: Reference to the CompletionUpdater instance.
		@type self: A CompletionUpdater object.

		@param dictionary: Word completion dictionary.
		@type dictionary: A Dict object.
		"""
		#self.__manager.emit("update", dict(dictionary))
		#self.__is_indexing = False
		return

	def __error_handler_cb(self, error):
		"""
		Handles callback when an error message is received from the
		indexer.

		@param self: Reference to the CompletionUpdater instance.
		@type self: A CompletionUpdater object.

		@param error: An error message.
		@type error: A String object.
		"""
		print "INDEXER ERROR: Failed to index text"
		print "========================================================"
		print error
		print "========================================================"
		self.__is_indexing = False
		return

	def __finished_indexing_cb(self, editor_id, dictionary):
		from operator import ne
		if ne(editor_id, self.__editor.id): return
		self.__manager.emit("update", dict(dictionary))
		self.__is_indexing = False
		return

	def __destroy_cb(self, manager):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the CompletionUpdater instance.
		@type self: An CompletionUpdater object.

		@param manager: Reference to the CompletionManager.
		@type manager: An CompletionManager object.
		"""
		self.__editor.session_bus.remove_signal_receiver(self.__name_change_cb,
						'NameOwnerChanged',
						'org.freedesktop.DBus',
						'org.freedesktop.DBus',
						'/org/freedesktop/DBus',
						arg0=indexer_dbus_service)
		self.__editor.session_bus.remove_signal_receiver(self.__finished_indexing_cb,
						signal_name="finished_indexing",
						dbus_interface=indexer_dbus_service)
		self.__indexer = None
		self.__remove_timer()
		try:
			from gobject import source_remove
			source_remove(self.__index_timer)
		except Exception:
			pass
		self.__editor.disconnect_signal(self.__signal_id_1, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__editor.textbuffer)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__manager)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__editor)
		self.__editor.delete_attributes(self)
		del self
		self = None
		return

	def __precompile_methods(self):
		try:
			from psyco import bind
			bind(self.__index)
			bind(self.__generate_dictionary)
			bind(self.__start_indexer)
		except ImportError:
			pass
		return False
