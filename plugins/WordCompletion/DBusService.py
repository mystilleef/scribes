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
This module documents a class that represents the Indexer process.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from dbus.service import Object, method, BusName, signal

indexer_dbus_service = "org.sourceforge.ScribesIndexer"
indexer_dbus_path = "/org/sourceforge/ScribesIndexer"

class DBusService(Object):
	"""
	This class is a D-Bus service for Scribes word completion indexer.
	"""

	def __init__(self, indexer):
		from SCRIBES.Globals import session_bus
		bus_name = BusName(indexer_dbus_service, bus=session_bus)
		Object.__init__(self, bus_name, indexer_dbus_path)
		self.__indexer = indexer

	@method(indexer_dbus_service)
	def process(self, text, id):
		return self.__indexer.process(text, id)

	@signal(indexer_dbus_service)
	def finished_indexing(self, id, dictionary):
		return

	@signal(indexer_dbus_service)		
	def busy(self, id):
		return 
