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

scribes_dbus_service = "net.sourceforge.Scribes"
scribes_dbus_path = "/net/sourceforge/Scribes"

def main(argv=None):
	"""
	Main entry point to the program.

	@param argv: Command line arguments.
	@type argv:	A List object.
	"""
	from operator import truth
	if truth(argv):
		uris = __get_uris(argv)
		__open(uris)
	else:
		__open()
	__mainloop()
	return

def __open(uris=None):
	"""
	Start a new instance of the text editor.

	@param uris: A list of files to open, or None.
	@type uris: A List object.
	"""
	__open_via_dbus(uris)
	from gobject import idle_add, PRIORITY_HIGH, threads_init
	threads_init()
	idle_add(__launch_new_editor, uris, priority=PRIORITY_HIGH)
	return

def __open_via_dbus(uris=None):
	"""
	Use a running instance of the text editor to open new windows or
	files.

	This function prevents the text editor from spawning multiple
	process. All text editor instances share the same process, python
	interpreter and main loop.

	@param uris: A list of files to open, or None.
	@type uris: A List object.
	"""
	dbus_service = __get_dbus_service()
	from operator import truth, not_
	if not_(dbus_service): return
	if not_(uris): uris = ""
	dbus_service.open_files(uris, dbus_interface=scribes_dbus_service)
	raise SystemExit
	return

def __launch_new_editor(uris=None):
	"""
	Create one or more instances of the text editor.

	If files are passed as arguments, each file is loaded in a new
	editor window.

	@param uris: A list of files to open, or None.
	@type uris: A List object.

	@return: False to prevent repeated calls of this function.
	@rtype: A Boolean object.
	"""
	from InstanceManager import EditorManager
	manager = EditorManager()
	manager.open_files(uris)
	return False

def __get_dbus_service():
	"""
	Get a D-Bus object representing a running Scribes process.

	@param return: An object representing a running Scribes process.
	@param type: #FIXME: ????, or None.
	"""
	from info import dbus_iface, session_bus
	services = dbus_iface.ListNames()
	from operator import contains, not_
	if not_(contains(services, scribes_dbus_service)): return None
	proxy_object = session_bus.get_object(scribes_dbus_service, scribes_dbus_path)
	return proxy_object

def __get_uris(argv):
	"""
	Process arguments passed to the text editor.

	This function ends the process if there are no files to open.

	@param return: A list of files to open, if any.
	@param type: A List object.
	"""
	from commandline import CommandLineProcessor
	arguments = CommandLineProcessor(argv)
	uris = arguments.uri_list
	from operator import not_
	if not_(uris): raise SystemExit
	return uris

def __mainloop():
	"""
	Initialize the GObject mainloop.
	"""
	__fork_scribes()
	from info import mainloop
	from gobject import threads_init
	threads_init()
	mainloop.run()
	return

def __fork_scribes():
	"""
	Detach Scribes from the shell terminal and run it in its own
	process.
	"""
	from operator import ne, not_
	if not_(__can_fork()): return
	from os import fork
	pid = fork()
	if ne(pid, 0):
		from sys import exit
		exit(0)
	return

def __can_fork():
	"""
	Whether or not to detach Scribes from the shell terminal.

	@param return: True to detach Scribes from the shell terminal.
	@param type: A Boolean object.
	"""
	from gconf import client_get_default
	client = client_get_default()
	fork_scribes = True
	from operator import truth
	if truth(client.get("/apps/scribes/fork_scribes")):
		fork_scribes = client.get_bool("/apps/scribes/fork_scribes")
	return fork_scribes
