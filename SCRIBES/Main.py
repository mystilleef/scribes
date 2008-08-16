# -*- coding: utf-8 -*-
# Copyright (C) 2005 Lateef Alabi-Oki
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
This module contains the function to the main entry point of the
program.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

#from dbus.mainloop.glib import DBusGMainLoop
#DBusGMainLoop(set_as_default=True)
scribes_dbus_service = "net.sourceforge.Scribes"
scribes_dbus_path = "/net/sourceforge/Scribes"

def main(argv=None):
	__open(argv)
	__mainloop()
	return

def __open(argv=None):
	uris = __get_uris(argv)
	__open_via_dbus(uris)
	#__init_threads()
	from InstanceManager import EditorManager
	EditorManager().open_files(uris)
	return

def __open_via_dbus(uris=None):
	dbus_service = __get_dbus_service()
	if not dbus_service: return
	uris = uris if uris else ""
	dbus_service.open_files(uris, dbus_interface=scribes_dbus_service)
	raise SystemExit
	return

def __init_threads():
	from gobject import threads_init
	threads_init()
	from dbus.glib import threads_init
	threads_init()
	from gtk.gdk import threads_init
	threads_init()
	return

def __get_dbus_service():
	from info import dbus_iface, session_bus
	services = dbus_iface.ListNames()
	if not (scribes_dbus_service in services): return None
	proxy_object = session_bus.get_object(scribes_dbus_service, scribes_dbus_path)
	return proxy_object

def __get_uris(argv):
	if not argv: return None
	from CommandLineProcessor import get_uris
	uris = get_uris(argv)
	if not uris: raise SystemExit
	return uris

def __mainloop():
	__fork_scribes()
	from utils import init_gnome
	init_gnome()
	from gtk import main
	main()
	return

def __fork_scribes():
	from ForkScribesMetadata import get_value as can_fork
	if not can_fork(): return
	from os import fork
	pid = fork()
	if pid != 0: raise SystemExit
	return

try:
	from psyco import bind
	bind(__mainloop)
except:
	pass
