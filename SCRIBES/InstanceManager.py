# -*- coding: utf-8 -*-
# Copyright © 2006 Lateef Alabi-Oki
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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Scribes; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA	 02110-1301
# USA

"""
This module documents a class that manages instances of the text editor.
It allows editor instances to communicate with each other.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2006 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

close_file = lambda editor: editor.emit("close-document")

class Manager(object):
	"""
	This class implements an object that creates new instances of the
	text editor and manages them.
	"""

	def __init__(self):
		# Expose Scribes' service to D-Bus.
		from DBusService import DBusService
		DBusService(self)
		self.__init_attributes()
		self.__init_i18n()
		from gobject import timeout_add
		timeout_add(300000, self.__init_garbage_collector, priority=9999)
		timeout_add(21000, self.__init_psyco, priority=9999)

	def __init_attributes(self):
		from collections import deque
		self.__editor_instances = deque([])
		self.__registration_ids = deque([])
		from GlobalStore import Store
		self.__store = Store()
		from SaveProcessMonitor import SaveProcessMonitor
		self.__save_process_monitor = SaveProcessMonitor()
		return

########################################################################
#
#						Public APIs
#
########################################################################

	def register_editor(self, instance):
		self.__editor_instances.append(instance)
		from utils import generate_random_number
		number =  generate_random_number(self.__registration_ids)
		self.__registration_ids.append(number)
		return number

	def unregister_editor(self, instance, number):
		try:
			self.__editor_instances.remove(instance)
			self.__registration_ids.remove(number)
		except ValueError:
			print "===================================================="
			print "Scribes Error:"
			print "From InstanceManager.py line 118"
			print "Instance not found,", instance
			print "===================================================="
		if not self.__editor_instances: self.__quit()
		return

	def response(self):
		return False

	def block_response(self):
		return

	def unblock_response(self):
		return

	def add_object(self, name, instance):
		return self.__store.add_object(name, instance)

	def remove_object(self, name, object_id):
		return self.__store.remove_object(name, object_id)

	def get_object(self, name):
		return self.__store.get_object(name)

	def save_processor_is_ready(self):
		return self.__save_process_monitor.is_ready()

	def get_save_processor(self):
		return self.__save_process_monitor.get_processor_object()

	def open_window(self):
		instances = self.__editor_instances
		instances[0].trigger("new_window") if instances else self.__new_editor()
		return False

	def open_files(self, uris=None, encoding="utf-8"):
		if uris:
			has_uri = lambda x: x in self.get_uris()
			has_not_uri = lambda x: not (x in self.get_uris())
			open_file = lambda x: self.__open_file(x, encoding)
			# Focus respective window if file is already open.
			[self.focus_file(uri) for uri in uris if has_uri(uri)]
			# Open new file if it's not already open.
			[open_file(uri) for uri in uris if has_not_uri(uri)]
		else:
			self.open_window()
		return False

	def close_files(self, uris):
		if not uris: return False
		[self.__close_file(uri) for uri in uris]
		return False

	def close_all_windows(self):
		[close_file(instance) for instance in self.__editor_instances]
		return False

	def focus_file(self, uri):
		found_instance = [editor for editor in self.__editor_instances if str(editor.uri) == uri]
		if not found_instance: return False
		editor = found_instance[0]
		coordinates = None if editor.window.is_maximized else editor.window.get_position()
		editor.window.hide()
		if coordinates: editor.window.move(coordinates[0], coordinates[1])
		editor.window.window.show()
		editor.window.show_all()
		editor.window.present()
		editor.textview.grab_focus()
		return False

	def get_uris(self):
		if not self.__editor_instances: return []
		uris = [str(editor.uri) for editor in self.__editor_instances if editor.uri]
		return uris

	def get_editor_instances(self):
		return self.__editor_instances

	def init_authentication_manager(self):
		from gnome.ui import authentication_manager_init
		authentication_manager_init()
		return

########################################################################
#
#						Helper Methods
#
########################################################################

	def __open_file(self, uri, encoding="utf-8"):
		if not uri: return False
		instances = self.__editor_instances
		empty_windows = [x for x in instances if x.can_load_file]
		empty_windows[0].load_uri(uri, encoding) if empty_windows else self.__new_editor(uri, encoding)
		return False

	def __close_file(self, uri):
		[close_file(editor) for editor in self.__editor_instances if editor.uri == uri]
		return False

	def __new_editor(self, uri=None, encoding=None):
		from Editor import Editor
		Editor(self, uri, encoding)
		return False

	def __init_garbage_collector(self):
		from gc import collect
		from thread import start_new_thread
		start_new_thread(collect, ())
#		collect()
		return True

	def __init_psyco(self):
		try:
			from psyco import background#, log , profile#, log
#			log("/home/meek/Desktop/psyco-log.log")
			from thread import start_new_thread
			start_new_thread(background, ())
#			background()
			print "Initialized psyco profiling and optimization"
		except ImportError:
			pass
		return False

	def __init_i18n(self):
		from info import scribes_data_path
		from os import path
		locale_folder = path.join(scribes_data_path, "locale")
		# Initialize glade first.
		try:
			from locale import setlocale, LC_ALL, Error, bindtextdomain
			bindtextdomain("scribes", locale_folder)
			setlocale(LC_ALL, "")
		except Error:
			pass
		from gtk import glade
		glade.bindtextdomain("scribes", locale_folder)
		glade.textdomain("scribes")
		from gettext import textdomain, bindtextdomain
		from gettext import install, bind_textdomain_codeset
		bindtextdomain("scribes", locale_folder)
		bind_textdomain_codeset("scribes", "UTF-8")
		textdomain("scribes")
		install("scribes", locale_folder, unicode=1)
		return

	def __precompile_methods(self):
		try:
			from psyco import bind
			bind(self.get_editor_instances)
			bind(self.open_files)
			bind(self.close_files)
			bind(self.get_uris)
			bind(self.focus_file)
			bind(self.register_editor)
			bind(self.unregister_editor)
		except ImportError:
			pass
		return False

	def __remove_swap_area(self):
		from glob import glob
		from info import home_folder
		files = glob(home_folder + "/" + ".Scribes*scribes")
		from shutil import rmtree
		[rmtree(file_, True) for file_ in files]
		return

	def __kernel_signals_cb(self, *args):
		#from gobject import idle_add
		self.close_all_windows()
		return

	def __quit(self):
		self.__remove_swap_area()
		self.__save_process_monitor.destroy()
		raise SystemExit
		return
