# -*- coding: utf8 -*-
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
This module documents a class that implements an indexer for automatic
word completion.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

dbus_service = "org.sourceforge.ScribesSaveProcessor"
dbus_path = "/org/sourceforge/ScribesSaveProcessor"

class SaveProcessor(object):
	"""
	This class indexes words for automatic word completion. An instance
	of this class runs in a separate process. The text editor
	communicates with this instance via D-Bus.
	"""

	def __init__(self):
		"""
		Initialize object.

		@param self: Reference to the CompletionIndexer instance.
		@type self: A CompletionIndexer object.
		"""
		self.__start_up_check()
		from SaveProcessorDBusService import DBusService
		dbus = DBusService(self)
		self.__init_attributes(dbus)
		from info import session_bus as session
		session.add_signal_receiver(self.__name_change_cb,
						'NameOwnerChanged',
						'org.freedesktop.DBus',
						'org.freedesktop.DBus',
						'/org/freedesktop/DBus',
						arg0='net.sourceforge.Scribes')
		self.__dbus.is_ready()
#		idle_add(self.__precompile_methods, priority=PRIORITY_LOW)

	def __init_attributes(self, dbus):
		"""
		Initialize data attributes.

		@param self: Reference to the CompletionIndexer instance.
		@type self: A CompletionIndexer object.
		"""
		from OutputProcessor import OutputProcessor
		self.__processor = OutputProcessor(dbus)
		self.__dbus = dbus
		return

	def save_file(self, editor_id, text, uri, encoding):
		from gobject import idle_add
		idle_add(self.__save_file, editor_id, text, uri, encoding)
		return
		
	def __save_file(self, editor_id, text, uri, encoding):
		self.__processor.process(editor_id, text, uri, encoding)
		return False

	def __precompile_methods(self):
		try:
			from psyco import bind
		except ImportError:
			pass
		return False

	def __name_change_cb(self, *args):
		"""
		Quit when the Scribes process dies.

		@param self: Reference to the CompletionIndexer instance.
		@type self: A CompletionIndexer object.
		"""
		from os import _exit
		_exit(0)
		return

	def __start_up_check(self):
		from info import dbus_iface
		services = dbus_iface.ListNames()
		from operator import contains, not_
		if not_(contains(services, dbus_service)): return
#		print "Ooops! Found another completion indexer, killing this one."
		from os import _exit
		_exit(0)
		return

if __name__ == "__main__":
	from sys import argv, path
	python_path = argv[1]
	path.insert(0, python_path)
	SaveProcessor()
	from gobject import MainLoop
	MainLoop().run()
