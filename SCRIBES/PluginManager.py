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

class PluginManager(object):
	"""
	This class creates an object that loads and unloads plugins.
	"""

	def __init__(self, editor):
		"""
		Initialize object.

		@param self: Reference to the PluginManager instance.
		@type self: A PluginManager object.

		@param editor: Reference to the editor object.
		@type editor: A editor object.
		"""
		try:
#			self.__precompile_methods() this is a test file.
			from Exceptions import PluginFolderNotFoundError
			self.__init_attributes(editor)
			self.__check_plugin_folders()
			self.__set_plugin_search_path()
			self.__load_plugins()
			self.__registration_id = self.__editor.register_object()
			self.__signal_id_1 = editor.connect("close-document", self.__quit_cb)
			self.__signal_id_2 = editor.connect("close-document-no-save", self.__quit_cb)
#			from gobject import idle_add, PRIORITY_LOW
#			idle_add(self.__precompile_methods, priority=PRIORITY_LOW)
		except PluginFolderNotFoundError:
			print "Error: No plugin folder found"

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the PluginManager instance.
		@type self: A PluginManager object.

		@param editor: Reference to the editor instance.
		@type editor: A editor object.
		"""
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
		"""
		Initialize a plugin module file.

		@param self: Reference to the PluginManager instance.
		@type self: A PluginManager object.

		@param filename: A possible plugin file.
		@type filename: A String object.
		"""
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
			print "Not loading: ", (filename)
			self.__plugin_modules.add(module)
		return False

	def __load_plugin(self, PluginClass):
		"""
		Initialize a plugin.

		@param self: Reference to the PluginManager instance.
		@type self: A PluginManager object.

		@param PluginClass: The class object of a plugin.
		@type PluginClass: A Class object.

		@return: A plugin object.
		@rtype: A Plugin object.
		"""
		plugin_object = PluginClass(self.__editor)
		plugin_object.load()
		return plugin_object

	def __unload_plugin(self, plugin_info):
		plugin_object = plugin_info[2]
		plugin_object.unload()
		self.__plugin_objects.remove(plugin_info)
		if self.__plugin_objects: return False
		if self.__is_quiting: self.__destroy()
		return False

	def __load_plugins(self):
		"""
		Initialize plugins found in plugin modules.

		@param self: Reference to the PluginManager instance.
		@type self: A PluginManager object.
		"""
		from os import listdir
		from gobject import idle_add, PRIORITY_LOW
		core_files = listdir(self.__editor.core_plugin_folder)
		#from thread import start_new_thread
		for filename in core_files:
		#	start_new_thread(self.__init_module, (filename, self.__editor.core_plugin_folder))
			idle_add(self.__init_module, filename, self.__editor.core_plugin_folder, priority=PRIORITY_LOW)
		home_files = listdir(self.__editor.home_plugin_folder)
		for filename in home_files:
			#start_new_thread(self.__init_module, (filename, self.__editor.home_plugin_folder))
			idle_add(self.__init_module, filename, self.__editor.home_plugin_folder, priority=PRIORITY_LOW)
		return False

	def __unload_plugins(self):
		"""
		Unload all plugins.

		@param self: Reference to the PluginManager instance.
		@type self: A PluginManager object.
		"""
		from gobject import idle_add, PRIORITY_LOW
		#from thread import start_new_thread
		for plugin_info in self.__plugin_objects.copy():
			#start_new_thread(self.__unload_plugin, (plugin_info,))
			idle_add(self.__unload_plugin, plugin_info, priority=PRIORITY_LOW)
		return False

	def __get_module_info(self, module):
		"""
		Extract metadata from plugin module.

		@param self: Reference to the PluginManager instance.
		@type self: A PluginManager object.

		@param module: A plugin module.
		@type module: A Module object.

		@return: plugin name, plugin version and plugin class object
		@rtype: A Tuple object.
		"""
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
		"""
		Unload old duplicate plugin versions to avoid conflict.

		@param self: Reference to the PluginManager instance.
		@type self: A PluginManager object.

		@param name: Name of a plugin.
		@type name: A String object.

		@param version: Version of a plugin.
		@type version: A Float object.
		"""
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
		"""
		Check plugin folders exist.

		If the plugin folder in ~/.gnome2/Scribes does not exist, create
		it.

		@param self: Reference to the PluginManager instance.
		@type self: A PluginManager object.
		"""
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
		"""
		Add plug-in folders to Python's search path.

		@param self: Reference to the ScribesPluginManager instance.
		@type self: A ScribesPluginManager object.
		"""
		from sys import path
		if not (self.__editor.core_plugin_folder in path): path.insert(0, self.__editor.core_plugin_folder)
		if not (self.__editor.home_plugin_folder in path): path.insert(0, self.__editor.home_plugin_folder)
		return

	def __destroy(self):
		"""
		Destroy this object.

		@param self: Reference to the PluginManager instance.
		@type self: A PluginManager object.
		"""
		self.__plugin_modules.clear()
		self.__plugin_objects.clear()
		self.__editor.unregister_object(self.__registration_id)
		self.__editor.disconnect_signal(self.__signal_id_1, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__editor)
		del self
		self = None
		return

	def __precompile_methods(self):
		try:
			from psyco import bind
			bind(self.__init_module)
			bind(self.__load_plugin)
		except:
			pass
		return False

	def __quit_cb(self, *args):
		"""
		Handles callback when the "close-document" or "close-document-no-save"
		signal is emitted.

		The function is called when the editor is closing.

		@param self: Reference to the PluginManager instance.
		@type self: A PluginManager object.
		"""
		self.__is_quiting = True
		# Unload plugins and destroy PluginManager.
		from gobject import idle_add
		idle_add(self.__unload_plugins)
		return
