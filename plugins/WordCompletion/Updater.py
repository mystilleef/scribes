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
		self.__init_attributes(manager, editor)
		from gobject import idle_add, PRIORITY_LOW, timeout_add
		timeout_add(2000, self.__start_indexer, priority=PRIORITY_LOW)
		self.__sigid1 = self.__editor.connect_after("loaded-file", self.__loaded_document_cb)
		self.__sigid2 = self.__editor.textbuffer.connect_after("changed", self.__changed_cb)
		self.__sigid3 = self.__manager.connect("destroy", self.__destroy_cb)
		self.__sigid4 = self.__editor.connect_after("renamed-file", self.__loaded_document_cb)
		editor.session_bus.add_signal_receiver(self.__name_change_cb,
						'NameOwnerChanged',
						'org.freedesktop.DBus',
						'org.freedesktop.DBus',
						'/org/freedesktop/DBus',
						arg0=indexer_dbus_service)
		editor.session_bus.add_signal_receiver(self.__finished_indexing_cb,
						signal_name="finished_indexing",
						dbus_interface=indexer_dbus_service)
		editor.session_bus.add_signal_receiver(self.__busy_cb,
						signal_name="busy",
						dbus_interface=indexer_dbus_service)
		idle_add(self.__precompile_methods, priority=9999)
		
	def __init_attributes(self, manager, editor):
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
		from collections import deque
		self.__queue = deque([])
		return
	
	def __precompile_methods(self):
		methods = (self.__changed_cb, self.__index, 
			self.__generate_dictionary, self.__get_text,
			self.__send_text)
		self.__editor.optimize(methods)
		return False

########################################################################
#
#						Helper Methods
#
########################################################################

	def __index(self):
		try:
			if self.__is_indexing: return False #self.__update_queue()
			if self.__editor.readonly: return False
			if self.__indexer is None:
				from gobject import idle_add, PRIORITY_LOW, timeout_add
				timeout_add(2000, self.__start_indexer, priority=PRIORITY_LOW)
				return False
			self.__remove_timer()
			from gobject import idle_add, PRIORITY_LOW, timeout_add
			self.__timer = timeout_add(500, self.__generate_dictionary, priority=9999)
			#self.__timer = idle_add(self.__generate_dictionary, priority=PRIORITY_LOW)
		except ValueError:
			return False
		return False

	def __generate_dictionary(self):
		try:
			if self.__is_indexing: return False #self.__update_queue()
			if not self.__indexer: return False
			self.__is_indexing = True
			from gobject import idle_add
			idle_add(self.__send_text, priority=9999)
#			from thread import start_new_thread
#			start_new_thread(self.__send_text, ())
		except ValueError:
			return False
		return False

	def __start_indexer(self):
		try:
			from dbus import DBusException
			from SCRIBES.Globals import dbus_iface, session_bus, python_path
			services = dbus_iface.ListNames()
			self.__indexer = None
			if indexer_dbus_service in services:
				try:
					self.__indexer = session_bus.get_object(indexer_dbus_service, indexer_dbus_path)
					from gobject import idle_add, PRIORITY_LOW
				except:
					pass
				try:
					source_remove(self.__index_timer)
				except Exception:
					pass
				self.__index_timer = idle_add(self.__index, priority=PRIORITY_LOW)
			else:
				try:
					from gobject import spawn_async
					spawn_async([self.__python_executable, self.__indexer_executable, python_path], working_directory=self.__indexer_cwd)
				except:
					pass
		except DBusException:
			pass
		except:
			pass
		return False

	def __get_text(self):
		all_text = [editor.text for editor in self.__editor.instances]
		return " ".join(all_text)

	def __remove_timer(self):
		try:
			from gobject import source_remove
			source_remove(self.__timer)
		except:
			pass
		return

	def __update_queue(self):
		if self.__queue: raise ValueError
		self.__queue.append(1)
		return

########################################################################
#
#					Signal and Event Handlers
#
########################################################################

	def __changed_cb(self, textbuffer):
		from gobject import timeout_add, idle_add, PRIORITY_LOW
		try:
			source_remove(self.__index_timer)
		except Exception:
			pass
		self.__index_timer = timeout_add(500, self.__index, priority=9999)
		return False

	def __loaded_document_cb(self, *args):
		from gobject import idle_add, PRIORITY_LOW
		try:
			source_remove(self.__index_timer)
		except Exception:
			pass
		self.__index_timer = idle_add(self.__index, priority=9999)
		return

	def __name_change_cb(self, *args):
		from gobject import idle_add, PRIORITY_LOW, timeout_add
		timeout_add(2000, self.__start_indexer, priority=PRIORITY_LOW)
		return

	def __reply_handler_cb(self, *args):
		return

	def __error_handler_cb(self, error):
		self.__is_indexing = False
		return

	def __finished_indexing_cb(self, editor_id, dictionary):
		if editor_id != self.__editor.id_: return True
#		from thread import start_new_thread
#		start_new_thread(self.__update_dictionary, (dictionary,))
		from gobject import idle_add
		idle_add(self.__update_dictionary, dictionary, priority=9999)
		return True

	def __busy_cb(self, editor_id):
		if editor_id != self.__editor.id_: return True
		self.__queue.clear()
		self.__is_indexing = False
		return True

	def __update_dictionary(self, dictionary):
		self.__manager.emit("update", dict(dictionary))
		try:
			self.__queue.pop()
			self.__send_text()
		except IndexError:
			self.__is_indexing = False
		return False

	def __send_text(self):
		try:
			self.__indexer.process(self.__get_text(), self.__editor.id_,
				dbus_interface=indexer_dbus_service,
				reply_handler=self.__reply_handler_cb,
				error_handler=self.__error_handler_cb)
		except:
			self.__is_indexing = False
		return False

########################################################################
#
#						Destroy Method
#
########################################################################

	def __destroy_cb(self, manager):
		self.__editor.session_bus.remove_signal_receiver(self.__name_change_cb,
						'NameOwnerChanged',
						'org.freedesktop.DBus',
						'org.freedesktop.DBus',
						'/org/freedesktop/DBus',
						arg0=indexer_dbus_service)
		self.__editor.session_bus.remove_signal_receiver(self.__finished_indexing_cb,
						signal_name="finished_indexing",
						dbus_interface=indexer_dbus_service)
		self.__editor.session_bus.remove_signal_receiver(self.__busy_cb,
						signal_name="busy",
						dbus_interface=indexer_dbus_service)
		self.__indexer = None
		self.__remove_timer()
		try:
			from gobject import source_remove
			source_remove(self.__index_timer)
		except Exception:
			pass
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor.textbuffer)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		del self
		self = None
		return
