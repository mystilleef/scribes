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
from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)
RECURSIONLIMITMULTIPLIER = 1000
indexer_dbus_service = "org.sourceforge.ScribesIndexer"
indexer_dbus_path = "/org/sourceforge/ScribesIndexer"

class CompletionIndexer(object):
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
		from DBusService import DBusService
		dbus = DBusService(self)
		self.__init_attributes(dbus)
		from SCRIBES.info import session_bus
		session_bus.add_signal_receiver(self.__name_change_cb,
						'NameOwnerChanged',
						'org.freedesktop.DBus',
						'org.freedesktop.DBus',
						'/org/freedesktop/DBus',
						arg0='net.sourceforge.Scribes')
		from os import nice
		nice(19)
		from gobject import timeout_add, idle_add, PRIORITY_LOW
		timeout_add(600000, self.__check_instances, priority=PRIORITY_LOW)
		idle_add(self.__precompile_methods, priority=PRIORITY_LOW)

	def __init_attributes(self, dbus):
		"""
		Initialize data attributes.

		@param self: Reference to the CompletionIndexer instance.
		@type self: A CompletionIndexer object.
		"""
		self.__is_busy = False
		from collections import deque
		self.__queue = deque([])
		from re import UNICODE, compile
		self.__pattern = compile(r"[^-\w]", UNICODE)
		from dbus import Dictionary, String, Int64
		try:
			self.__empty_dict = Dictionary({}, signature="ss")
		except:
			self.__empty_dict = Dictionary({}, key_type=String, value_type=Int64)
		self.__dbus = dbus
		return

	def process(self, text, id):
		"""
		Index text.

		@param self: Reference to the CompletionIndexer instance.
		@type self: A CompletionIndexer object.

		@param text: Text to be indexed for word completion.
		@type text: A String object.

		@return: A dictionary of words for automatic completion.
		@rtype: A Dict object.
		"""
		try:
			if self.__is_busy: raise ValueError
			self.__is_busy = True
			from thread import start_new_thread
			start_new_thread(self.__process_text, (text, id))
			#from gobject import timeout_add, source_remove
			#try:
			#	source_remove(self.__timer)
			#except:
			#	pass
			#self.__timer = timeout_add(1000, self.__process_text, text, id)
		except ValueError:
			self.__dbus.busy(id)
		return

	def __process_text(self, text, id):
		if not text:
			self.__dbus.finished_indexing(id, self.__empty_dict)
			self.__is_busy = False
			return False
		completions = self.__generate_completion_list(text)
		dictionary = self.__generate_completion_dictionary(completions)
		self.__dbus.finished_indexing(id, dictionary)
		self.__is_busy = False
		return False

	def __generate_completion_list(self, text):
		"""
		Generate list of words for automatic completion.

		@param self: Reference to the CompletionIndexer instance.
		@type self: A CompletionIndexer object.

		@param text: Text to be indexed for word completion.
		@type text: A String object.

		@param return: A list of words for automatic completion.
		@type return: A List object.
		"""
		if not text: return None
		from re import split
		completion_list = split(self.__pattern, text)#.decode("utf-8"))
		completions = filter(self.__filter, completion_list)
		return completions

	def __generate_completion_dictionary(self, completions):
		"""
		Rank the occurence of a list of words in a dictionary.

		@param self: Reference to the CompletionIndexer instance.
		@type self: A CompletionIndexer object.

		@param completions: A list of words for automatic completion.
		@type completions: A List object.

		@return: A dictionary of words ranked by occurence.
		@rtype: A Dict object.
		"""
		if not completions: return self.__empty_dict
		dictionary = {}
		# Index strings based on their occurence in the editor's
		# buffer and place them in a dictionary.
		for string in completions:
			if string in dictionary.keys():
				dictionary[string] += 1
			else:
				dictionary[string] = 1
		if not dictionary: return self.__empty_dict
		return dictionary

	def __filter(self, string):
		"""
		Filter out word that do not meet the criteria for completion.

		Words for completion need to be more than three alphanumeric
		characters long.

		@param self: Reference to the CompletionIndexer instance.
		@type self: A CompletionIndexer object.

		@param string: A string to check.
		@type string: A String object.
		"""
		if len(string) < 4: return False
		if string.startswith("---") or string.startswith("___"): return False
		return True

	def __update_queue(self, id, text):
		self.__queue.append((id, text))
		return

	def __precompile_methods(self):
		try:
			from psyco import bind, full
			bind(self.__generate_completion_list)
			bind(self.__generate_completion_dictionary)
			bind(self.__filter)
			full()
		except ImportError:
			pass
		except:
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
		from SCRIBES.info import dbus_iface
		services = dbus_iface.ListNames()
		if not (indexer_dbus_service in services): return
#		print "Ooops! Found another completion indexer, killing this one."
		from os import _exit
		_exit(0)
		return

	def __check_instances(self):
		"""
		Periodically check for other instances.

		@param self: Reference to the CompletionIndexer instance.
		@type self: A CompletionIndexer object.
		"""
		from SCRIBES.info import dbus_iface
		services = dbus_iface.ListNames()
		if services.count(indexer_dbus_service) == 1: return True
#		print "Ooops! Found another completion indexer, killing this one."
		from os import _exit
		_exit(0)
		return True

def __set_vm_properties():
	"""
	Set virtual machine's (Python) system properties.
	"""
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

if __name__ == "__main__":
	__set_vm_properties()
	from sys import argv, path
	python_path = argv[1]
	path.insert(0, python_path)
	from gobject import MainLoop, threads_init
	threads_init()
	CompletionIndexer()
	MainLoop().run()
