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

from dbus.service import Object, method, BusName

class DBusService(Object):
	"""
	This class is a D-Bus service that ensures all instances of the
	editor share the same process.
	"""

	def __init__(self, manager):
		"""
		Initialize the D-Bus service.

		@param self: Reference to the DBusService instance.
		@type self: A DBusService object.

		@param manager: Reference to an object that manages instances of the editor.
		@type manager: An EditorManager object.
		"""
		from info import session_bus
		service_name = "net.sourceforge.Scribes"
		object_path = "/net/sourceforge/Scribes"
		bus_name = BusName(service_name, bus=session_bus)
		Object.__init__(self, bus_name, object_path)
		self.__manager = manager

	@method("net.sourceforge.Scribes")
	def open_window(self):
		return self.__manager.open_window()

	@method("net.sourceforge.Scribes")
	def open_files(self, uris):
		if not uris:
			uris = None
		return self.__manager.open_files(uris)
