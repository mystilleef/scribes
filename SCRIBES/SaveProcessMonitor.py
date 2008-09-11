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
This module implements a class that monitors the file save processor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class SaveProcessMonitor(object):
	"""
	This class creates an instance that starts, manages and monitors the
	scribes' process that saves files.
	"""

	def __init__(self):
		self.__init_attributes()
		from gobject import idle_add
		idle_add(self.__start_save_processor)
		self.__session.add_signal_receiver(self.__name_change_cb,
						'NameOwnerChanged',
						'org.freedesktop.DBus',
						'org.freedesktop.DBus',
						'/org/freedesktop/DBus',
						arg0=self.__dbus_service)
		self.__session.add_signal_receiver(self.__is_ready_cb,
						signal_name="is_ready",
						dbus_interface=self.__dbus_service)

	def __init_attributes(self):
		self.__is_ready = False
		self.__quiting = False
		from os.path import join, split
		self.__cwd = split(globals()["__file__"])[0]
		self.__executable = join(self.__cwd, "ScribesSaveProcessor.py")
		from sys import prefix
		self.__python_executable = prefix + "/bin" + "/python"
		self.__dbus_service = "org.sourceforge.ScribesSaveProcessor"
		self.__dbus_path = "/org/sourceforge/ScribesSaveProcessor"
		from Globals import session_bus
		self.__session = session_bus
		self.__save_processor_id = None
		return

	def __start_save_processor(self):
		if self.__get_processor_object(): return False
		self.__save_processor_id = None
		from gobject import spawn_async
		from Globals import python_path
		data = spawn_async([self.__python_executable, self.__executable, python_path], working_directory=self.__cwd)
		self.__save_processor_id = data[0]
		return False

	def __kill_save_processor(self):
		if self.__get_processor_object() is None: return
		if self.__save_processor_id is None: return
		from os import kill
		from signal import SIGHUP
		kill(self.__save_processor_id, SIGHUP)
		return

	def __get_processor_object(self):
		try:
			from dbus import DBusException
			from Globals import dbus_iface, session_bus, python_path
			services = dbus_iface.ListNames()
			from operator import contains, not_
			if not (self.__dbus_service in services): return None
			processor_object = session_bus.get_object(self.__dbus_service, self.__dbus_path)
		except DBusException:
			return None
		return processor_object

	def __name_change_cb(self, *args):
		if self.__quiting: return
		if self.__get_processor_object(): return
		self.__is_ready = False
		from gobject import idle_add
		idle_add(self.__start_save_processor)
		return

	def __is_ready_cb(self, *args):
		self.__is_ready = True
		return

	def is_ready(self):
		return self.__is_ready

	def get_processor_object(self):
		return self.__get_processor_object()

	def destroy(self):
		self.__session.remove_signal_receiver(self.__name_change_cb,
						'NameOwnerChanged',
						'org.freedesktop.DBus',
						'org.freedesktop.DBus',
						'/org/freedesktop/DBus',
						arg0=self.__dbus_service)
		self.__session.remove_signal_receiver(self.__is_ready_cb,
						signal_name="is_ready",
						dbus_interface=self.__dbus_service)
		self.__kill_save_processor()
		del self
		self = None
		return

