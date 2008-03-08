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

class EditorManager(object):
	"""
	This class implements an object that creates new instances of the
	text editor and manages them.
	"""

	def __init__(self):
		"""
		Initialize the object.

		@param self: Reference to the EditorManager instance.
		@type self: An EditorManager object.
		"""
		# Expose Scribes' service to D-Bus.
		from DBusService import DBusService
		DBusService(self)
		self.__init_attributes()
		self.__init_i18n()
		from gobject import idle_add, timeout_add
		idle_add(self.__precompile_methods, priority=5000)
		timeout_add(300000, self.__init_garbage_collector, priority=5000)

	def __init_attributes(self):
		"""
		Initialize data attributes.

		@param self: Reference to the EditorManager instance.
		@type self: An EditorManager object.
		"""
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
		"""
		Register successfully created editor instances.

		@param self: Reference to the EditorManager instance.
		@type self: An EditorManager object.

		@param instance: Reference to an Editor instance
		@type instance: An Editor object.

		@return: Return a unique number (id)
		@rtype: An Integer object.
		"""
		self.__editor_instances.append(instance)
		from utils import generate_random_number
		number =  generate_random_number(self.__registration_ids)
		self.__registration_ids.append(number)
		return number

	def unregister_editor(self, instance, number):
		"""
		Unregister an editor instance.

		This function removes an editor instance from the managed queue
		when the instance is no longer in use. When no editor instances
		exists, the function quits Scribes.

		@param self: Reference to the EditorManager instance.
		@type self: An EditorManager object.

		@param instance: Reference to an Editor instance.
		@type instance: An Editor object.

		@param number: A unique number associated with an editor instance.
		@param type: An Integer object.
		"""
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
		"""
		Open a new editor window.

		@param self: Reference to the EditorManager instance.
		@type self: An EditorManager object.
		"""
		if self.__editor_instances:
			editor = self.__editor_instances[0]
			editor.trigger("new_window")
		else:
			from gobject import idle_add
			idle_add(self.__new_editor)
		return False

	def open_files(self, uris=None, encoding="utf-8"):
		"""
		Open new files if they are not already open.

		@param self: Reference to the EditorManager instance.
		@type self: An EditorManager object.

		@param uris: A list of files to open.
		@type uris: A list object.
		"""
		if uris:
			has_uri = lambda x: x in self.get_uris()
			has_not_uri = lambda x: not (x in self.get_uris())
			open_file = lambda x: self.__open_file(x, encoding)
			# Focus respective window if file is already open.
			map(self.focus_file, filter(has_uri, uris))
			# Open new file if it's not already open.
			map(open_file, filter(has_not_uri, uris))
		else:
			from gobject import idle_add
			idle_add(self.open_window)
		return False

	def close_files(self, uris):
		"""
		Close files provided as arguments.

		@param self: Reference to the EditorManager instance.
		@type self: An EditorManager object.

		@param uris: A list of files to open.
		@type uris: A list object.
		"""
		if not uris: return False
		from gobject import idle_add
		for uri in uris:
			idle_add(self.__close_file, uri)
		return False

	def close_all_windows(self):
		"""
		Close all windows.

		@param self: Reference to the EditorManager instance.
		@type self: An EditorManager object.
		"""
		from gobject import idle_add
		for instance in self.__editor_instances:
			idle_add(close_file, instance)
		return False

	def focus_file(self, uri):
		"""
		Focus a window associated with a uri.

		@param self: Reference to the EditorManager instance.
		@type self: An EditorManager object.

		@param uri: A URI.
		@type uri: A String object.
		"""
		same = lambda editor: str(editor.uri) == uri
		found_instance = filter(same, self.__editor_instances)
		if not found_instance: return False
		editor = found_instance[0]
		editor.window.set_focus_on_map(True)
		xcoordinate, ycoordinate = editor.window.get_position()
		window_is_maximized = editor.window.is_maximized
		editor.window.hide()
		if not window_is_maximized: editor.window.move(xcoordinate, ycoordinate)
		editor.window.window.show()
		editor.window.show_all()
		editor.window.deiconify()
		return False

	def get_uris(self):
		"""
		Return a list of files loaded in editor windows.

		@param self: Reference to the EditorManager instance.
		@type self: An EditorManager object.

		@param return: A list of files loaded in editor windows.
		@type type: A List object.
		"""
		if not self.__editor_instances: return []
		uris = [str(editor.uri) for editor in self.__editor_instances if editor.uri]
		return uris

	def get_editor_instances(self):
		"""
		Return all editor instances.

		@param self: Reference to the InstanceManager instance.
		@type self: An InstanceManager object.

		@return: All editor instances.
		@rtype: A List object.
		"""
		return self.__editor_instances

########################################################################
#
#						Helper Methods
#
########################################################################

	def __open_file(self, uri, encoding="utf-8"):
		"""
		Open a file in an editor window.

		@param self: Reference to the EditorManager instance.
		@type self: An EditorManager object.

		@param uri: A file to open.
		@type uri: A String object.
		"""
		if not uri: return False
		instances = self.__editor_instances
		empty_windows = [x for x in instances if x.can_load_file]
		if empty_windows:
			# Always load files in empty editor windows first.
			editor = empty_windows[0]
			editor.load_uri(uri, encoding)
		else:
			from gobject import idle_add
			idle_add(self.__new_editor, uri, encoding)
		return False

	def __close_file(self, uri):
		"""
		Close an editor window containing a file.

		@param self: Reference to the EditorManager instance.
		@type self: An EditorManager object.

		@param uri: A file to close.
		@type uri: A String object.
		"""
		from itertools import ifilter
		same = lambda editor: editor.uri == uri
		from gobject import idle_add
		for document in ifilter(same, self.__editor_instances):
			idle_add(close_file, document)
		return False

	def __new_editor(self, uri=None, encoding=None):
		"""
		Create a new editor instance.

		@param self: Reference to the EditorManager instance.
		@type self: An EditorManager object.

		@param uri: A file to open.
		@type uri: A String object.
		"""
		from Editor import Editor
		Editor(self, uri, encoding)
		return False

	def __init_garbage_collector(self):
		"""
		Call the Python garbage collector.

		@param self: Reference to the EditorManager instance.
		@type self: An EditorManager object.
		"""
		from gc import collect
		collect()
		return True

	def __init_i18n(self):
		"""
		Initialize gettext modules for internationalization

		@param self: Reference to the InstanceManager instance.
		@type self: An InstanceManager object.
		"""
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
		"""
		Remove temporary saving area.

		@param self: Reference to the InstanceManager instance.
		@type self: An InstanceManager object.
		"""
		from glob import glob
		from info import home_folder
		files = glob(home_folder + "/" + ".Scribes*scribes")
		from shutil import rmtree
		for file in files:
			rmtree(file, True)
		return

	def __kernel_signals_cb(self, *args):
		#from gobject import idle_add
		self.close_all_windows()
		return

	def __quit(self):
		"""
		Quit Scribes.

		@param self: Reference to the EditorManager instance.
		@type self: A EditorManager object.
		"""
		self.__remove_swap_area()
		self.__save_process_monitor.destroy()
		from gtk import main_quit
		main_quit()
		#raise SystemExit
		return
