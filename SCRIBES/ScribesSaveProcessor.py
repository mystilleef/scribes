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

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)
RECURSIONLIMITMULTIPLIER = 1000000
dbus_service = "org.sourceforge.ScribesSaveProcessor"
dbus_path = "/org/sourceforge/ScribesSaveProcessor"

class SaveProcessor(object):
	"""
	The class is the external process that saves files.
	"""

	def __init__(self):
		self.__start_up_check()
		from SaveProcessorDBusService import DBusService
		dbus = DBusService(self)
		self.__init_attributes(dbus)
		from Globals import session_bus as session
		session.add_signal_receiver(self.__name_change_cb,
						'NameOwnerChanged',
						'org.freedesktop.DBus',
						'org.freedesktop.DBus',
						'/org/freedesktop/DBus',
						arg0='net.sourceforge.Scribes')
		dbus.is_ready()

	def __init_attributes(self, dbus):
		from OutputProcessor import OutputProcessor
		self.__processor = OutputProcessor(dbus)
		return

	def save_file(self, editor_id, text, uri, encoding):
		from thread import start_new_thread
		start_new_thread(self.__save_file, (editor_id, text, uri, encoding))
		return

	def update(self, editor_id):
		from thread import start_new_thread
		start_new_thread(self.__update, (editor_id,))
		return

	def __save_file(self, editor_id, text, uri, encoding):
		from thread import start_new_thread
		start_new_thread(self.__processor.process, (editor_id, text, uri, encoding))
		return False

	def __update(self, editor_id):
		from thread import start_new_thread
		start_new_thread(self.__processor.update, (editor_id,))
		return False

	def __name_change_cb(self, *args):
		from os import _exit
		_exit(0)
		return

	def __start_up_check(self):
		from Globals import dbus_iface
		services = dbus_iface.ListNames()
		if not (dbus_service in services): return
		from os import _exit
		_exit(0)
		return

def __set_vm_properties():
	from sys import setcheckinterval, getrecursionlimit
	from sys import setrecursionlimit, setdlopenflags
	try:
		from dl import RTLD_LAZY, RTLD_GLOBAL
		setdlopenflags(RTLD_LAZY|RTLD_GLOBAL)
	except ImportError:
		pass
	global RECURSIONLIMITMULTIPLIER
	setrecursionlimit(getrecursionlimit() * RECURSIONLIMITMULTIPLIER)
	return

def __init_psyco():
	try:
		from psyco import full
		full()
	except ImportError:
		pass
	return False

if __name__ == "__main__":
	__set_vm_properties()
	from sys import argv, path
	python_path = argv[1]
	path.insert(0, python_path)
	SaveProcessor()
	__init_psyco()
	from gobject import MainLoop, threads_init
	threads_init()
	MainLoop().run()

