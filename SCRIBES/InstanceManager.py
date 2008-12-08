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

close_file = lambda editor: editor.close()

class Manager(object):
	"""
	This class creates and manages new editor instances.
	"""

	def __init__(self):
		# Expose Scribes' service to D-Bus.
		from DBusService import DBusService
		DBusService(self)
		self.__init_attributes()
		from gobject import timeout_add
		timeout_add(21000, self.__init_psyco, priority=9999)
		self.__init_i18n()
		timeout_add(300000, self.__init_garbage_collector, priority=9999)

	def __init_attributes(self):
		from collections import deque
		self.__editor_instances = deque([])
		from gtk import WindowGroup
		self.__wingroup = WindowGroup()
		from SaveProcessMonitor import SaveProcessMonitor
		self.__save_process_monitor = SaveProcessMonitor()
		self.__busy = False
		self.__shortcut_list = []
		return

########################################################################
#
#						Public APIs
#
########################################################################

	def register_editor(self, instance):
		self.__wingroup.add_window(instance.window)
		self.__editor_instances.append(instance)
		return False

	def unregister_editor(self, instance):
		try:
			self.__wingroup.remove_window(instance.window)
			self.__editor_instances.remove(instance)
		except ValueError:
			print "===================================================="
			print "Module: InstanceManager.py"
			print "Class: Manager"
			print "Method: unregister_editor"
			print "Exception Type: ValueError"
			print "Error: Instance not found", instance
			print "===================================================="
		# Quit when there are no editor instances.
		if not self.__editor_instances: self.__quit()
		return

	def save_processor_is_ready(self):
		return self.__save_process_monitor.is_ready()

	def get_save_processor(self):
		return self.__save_process_monitor.get_processor_object()

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
			self.__new_editor()
		return False

	def close_files(self, uris):
		if not uris: return False
		[self.__close_file(uri) for uri in uris]
		return False

	def close_all_windows(self):
		from copy import copy
		[close_file(instance) for instance in copy(self.__editor_instances)]
		return False

	def focus_file(self, uri):
		found_instance = [editor for editor in self.__editor_instances if editor.uri == uri]
		if not found_instance: return False
		editor = found_instance[0]
		self.__focus(editor)
		return False

	def focus_by_id(self, id_):
		instance = [instance for instance in self.__editor_instances if instance.id_ == id_]
		editor = instance[0]
		self.__focus(editor)
		return False

	def get_uris(self):
		if not self.__editor_instances: return []
		return [editor.uri for editor in self.__editor_instances if editor.uri]

	def get_editor_instances(self):
		return self.__editor_instances

	def add_shortcut(self, shortcut):
		return self.__shortcut_list.append(shortcut)

	def remove_shortcut(self, shortcut):
		return self.__shortcut_list.remove(shortcut)

	def get_shortcuts(self):
		return self.__shortcut_list

	def response(self):
		if self.__busy: return False
		self.__busy = True
		from Utils import response
		response()
		self.__busy = False
		return False

########################################################################
#
#						Helper Methods
#
########################################################################

	def __open_file(self, uri, encoding="utf-8"):
		if not uri: return False
		instances = self.__editor_instances
		empty_windows = [x for x in instances if not x.contains_document]
		empty_windows[0].load_file(uri, encoding) if empty_windows else self.__new_editor(uri, encoding)
		return False

	def __close_file(self, uri):
		from copy import copy
		[close_file(editor) for editor in copy(self.__editor_instances) if editor.uri == uri]
		return False

	def __new_editor(self, uri=None, encoding=None):
		from Editor import Editor
		Editor(self, uri, encoding)
		return False

	def __focus(self, editor):
		editor.response()
		if editor.window.get_data("minimized"): editor.window.deiconify()
		coordinates = None if editor.window.get_data("maximized") else editor.window.get_position()
		editor.response()
		editor.window.hide()
		editor.response()
		if coordinates: editor.window.move(coordinates[0], coordinates[1])
		editor.response()
		editor.window.present()
		editor.response()
		editor.textview.grab_focus()
		editor.response()
		return False

	def __init_garbage_collector(self):
		from gc import collect
		collect()
		return True

	def __init_psyco(self):
		try:
			from psyco import background, profile, log
		#	background()
		#	print "Initialized psyco profiling and optimization"
		except ImportError:
			print "psyco not found"
		return False

	def __init_i18n(self):
		from Globals import data_path
		from os import path
		locale_folder = path.join(data_path, "locale")
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

	def __remove_swap_area(self):
		from glob import glob
		from Globals import home_folder, metadata_folder
		from os.path import join
		files = glob(home_folder + "/" + ".Scribes*scribes")
		from shutil import rmtree
		[rmtree(file_, True) for file_ in files]
		files = glob(join(metadata_folder, "__db*"))
		from shutil import rmtree
		[rmtree(file_, True) for file_ in files]
		return

	def __quit(self):
		self.__remove_swap_area()
		self.__save_process_monitor.destroy()
		raise SystemExit
		return
