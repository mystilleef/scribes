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
This modules documents a class that implements the plugin system for
Scribes.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class Manager(object):
	"""
	This class creates an object that loads and unloads plugins.
	"""

	def __init__(self, editor):
		try:
			from Exceptions import PluginFolderNotFoundError
			self.__init_attributes(editor)
			self.__check_plugin_folders()
			self.__set_plugin_search_path()
			self.__load_plugins()
			self.__sigid1 = editor.connect("quit", self.__quit_cb)
			editor.register_object(self)
			editor.response()
		except PluginFolderNotFoundError:
			print "Error: No plugin folder found"

	def __init_attributes(self, editor):
		self.__editor = editor
		# A set of initialized plugins. Each element in the set is a
		# tuple with format (plugin_name, plugin_version, plugin_object).
		self.__plugin_objects = set([])
		# A set of all plugin modules. Each element in the set is a tuple
		# with the format, (plugin_name, plugin_version, module_object).
		self.__plugin_modules = set([])
		self.__registration_id = None
		self.__is_quiting = False
		return

	def __init_module(self, filename, plugin_folder):
		from Exceptions import PluginModuleValidationError
		from Exceptions import DuplicatePluginError, DoNotLoadError
		try:
			if not (filename.startswith("Plugin") and filename.endswith(".py")): return False
			from os import path
			filepath = path.join(plugin_folder, filename)
			from imp import load_source
			module = load_source(filename[:-3], filepath)
			plugin_name, plugin_version, PluginClass = self.__get_module_info(module)
			self.__plugin_modules.add(module)
			self.__unload_duplicate_plugins(plugin_name, plugin_version)
			plugin_object = self.__load_plugin(PluginClass)
			self.__plugin_objects.add((plugin_name, plugin_version, plugin_object))
		except PluginModuleValidationError:
			print "Validation Error: ", filename
		except DuplicatePluginError:
			print "Duplicate Plugin: ", (plugin_name, plugin_version)
		except DoNotLoadError:
			#print "Not loading: ", (filename)
			self.__plugin_modules.add(module)
		return False

	def __load_plugin(self, PluginClass):
		self.__editor.busy()
		self.__editor.response()
		plugin_object = PluginClass(self.__editor)
		plugin_object.load()
#		self.__editor.refresh()
		self.__editor.busy(False)
		self.__editor.response()
		return plugin_object

	def __unload_plugin(self, plugin_info):
		self.__editor.response()
		plugin_object = plugin_info[2]
		plugin_object.unload()
		self.__plugin_objects.remove(plugin_info)
		self.__editor.response()
		return False

	def __load_plugins(self):
		core_plugin_folder = self.__editor.core_plugin_folder
		home_plugin_folder = self.__editor.home_plugin_folder
		from os import listdir
		core_files = listdir(core_plugin_folder)
		init_module = self.__init_module
		from thread import start_new_thread
		for filename in core_files:
#			idle_add(init_module, filename, core_plugin_folder, priority=9999)
			start_new_thread(init_module, (filename, core_plugin_folder))
		home_files = listdir(home_plugin_folder)
		for filename in home_files:
#			idle_add(init_module, filename, home_plugin_folder, priority=9999)
			start_new_thread(init_module, (filename, home_plugin_folder))
#			init_module(filename, home_plugin_folder)
		return False

	def __unload_plugins(self):
		from gobject import idle_add, PRIORITY_LOW
		#from thread import start_new_thread
		for plugin_info in self.__plugin_objects.copy():
			#start_new_thread(self.__unload_plugin, (plugin_info,))
			#idle_add(self.__unload_plugin, plugin_info, priority=PRIORITY_LOW)
			self.__unload_plugin(plugin_info)
		return False

	def __get_module_info(self, module):
		try:
			if not hasattr(module, "autoload"):
				raise Exception
			if not getattr(module, "autoload"):
				raise ValueError
			if hasattr(module, "version") is False:
				raise Exception
			plugin_version = getattr(module, "version")
			if hasattr(module, "class_name") is False:
				raise Exception
			plugin_name = class_name = getattr(module, "class_name")
			if hasattr(module, class_name) is False:
				raise Exception
			PluginClass = getattr(module, class_name)
			if hasattr(PluginClass, "__init__") is False:
				raise Exception
			if hasattr(PluginClass, "load") is False:
				raise Exception
			if hasattr(PluginClass, "unload") is False:
				raise Exception
		except ValueError:
			from Exceptions import DoNotLoadError
			raise DoNotLoadError
		except:
			from Exceptions import PluginModuleValidationError
			raise PluginModuleValidationError
		return plugin_name, plugin_version, PluginClass

	def __unload_duplicate_plugins(self, name, version):
		for info in self.__plugin_objects.copy():
			if name in info:
				if (version > info[1]):
					info[2].unload()
					self.__plugin_objects.remove(info)
				else:
					from Exceptions import DuplicatePluginError
					raise DuplicatePluginError
				break
		return

	def __check_plugin_folders(self):
		from os import makedirs, path
		from Exceptions import PluginFolderNotFoundError
		filename = path.join(self.__editor.core_plugin_folder, "__init__.py")
		if not path.exists(filename): raise PluginFolderNotFoundError
		filename = path.join(self.__editor.home_plugin_folder, "__init__.py")
		if path.exists(filename): return
		try:
			makedirs(self.__editor.home_plugin_folder)
		except OSError:
			pass
		try:
			handle = open(filename, "w")
			handle.close()
		except IOError:
			raise PluginFolderNotFoundError
		return

	def __set_plugin_search_path(self):
		from sys import path
		if not (self.__editor.core_plugin_folder in path): path.insert(0, self.__editor.core_plugin_folder)
		if not (self.__editor.home_plugin_folder in path): path.insert(0, self.__editor.home_plugin_folder)
		return

	def __destroy(self):
		self.__unload_plugins()
		self.__plugin_modules.clear()
		self.__plugin_objects.clear()
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return

	def __quit_cb(self, *args):
		self.__destroy()
		return False
