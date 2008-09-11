# -*- coding: utf-8 -*-
# Copyright © 2007 Lateef Alabi-Oki
#
# This file is part of striim.
#
# striim is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# striim is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with striim; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

"""
This module documents a class that represents the Indexer process.

@author: Lateef Alabi-Oki
@organization: The striim Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from dbus.service import Object, method, BusName, signal
dbus_service = "org.sourceforge.ScribesSaveProcessor"
dbus_path = "/org/sourceforge/ScribesSaveProcessor"

class DBusService(Object):
	"""
	This class is a D-Bus service for striim word completion indexer.
	"""

	def __init__(self, processor):
		from Globals import session_bus as session
		bus_name = BusName(dbus_service, bus=session)
		Object.__init__(self, bus_name, dbus_path)
		self.__processor = processor

	@method(dbus_service)
	def process(self, editor_id, text, uri, encoding):
		return self.__processor.save_file(editor_id, text, uri, encoding)

	@method(dbus_service)
	def update(self, editor_id):
		return self.__processor.update(editor_id)

	@signal(dbus_service)
	def is_ready(self):
		return

	@signal(dbus_service)
	def saved_file(self, editor_id, uri, encoding):
		return

	@signal(dbus_service)
	def error(self, editor_id, error_message, error_id):
		return
		
