# -*- coding: utf-8 -*-
# Copyright © 2005 Lateef Alabi-Oki
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
This module documents a class that (un)loads language specific plugins.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

class PluginManager(object):
	"""
	This class creates an object that loads and unloads language
	specific plugins.
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
			from Exceptions import PluginFolderNotFoundError
			self.__init_attributes(editor)
			self.__check_plugin_folders()
			self.__set_plugin_search_path()
			if editor.contains_document: self.__load_plugins()
			self.__registration_id = self.__editor.register_object()
			self.__signal_id_1 = editor.connect("close-document", self.__quit_cb)
			self.__signal_id_2 = editor.connect("close-document-no-save", self.__quit_cb)
			self.__signal_id_3 = editor.connect("loaded-document", self.__reload_cb)
			self.__signal_id_4 = editor.connect("renamed-document", self.__reload_cb)
			self.__signal_id_5 = editor.connect("reload-document", self.__reload_cb)
		except PluginFolderNotFoundError:
			print "Error: No language plugin folder found"

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
		filename = path.join(self.__editor.core_language_plugin_folder, "__init__.py")
		if not path.exists(filename): raise PluginFolderNotFoundError
		filename = path.join(self.__editor.home_language_plugin_folder, "__init__.py")
		if path.exists(filename): return
		try:
			makedirs(self.__editor.home_language_plugin_folder)
		except OSError:
			pass
		try:
			handle = open(filename, "w")
			handle.close()
		except IOError:
			raise PluginFolderNotFoundError
		return

	def __destroy(self):
		"""
		Destroy manager.

		@param self: Reference to the PluginManager instance.
		@type self: A PluginManager object.
		"""
		self.__plugin_modules.clear()
		self.__plugin_objects.clear()
		self.__editor.unregister_object(self.__registration_id)
		self.__editor.disconnect_signal(self.__signal_id_1, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_5, self.__editor)
		del self
		self = None
		return

	def __set_plugin_search_path(self):
		"""
		Add plug-in folders to Python's search path.

		@param self: Reference to the ScribesPluginManager instance.
		@type self: A ScribesPluginManager object.
		"""
		from sys import path
		if not (self.__editor.core_language_plugin_folder in path): path.insert(0, self.__editor.core_language_plugin_folder)
		if not (self.__editor.home_language_plugin_folder in path): path.insert(0, self.__editor.home_language_plugin_folder)
		return

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
			if not hasattr(module, "autoload"): raise Exception
			if not getattr(module, "autoload"): raise ValueError
			if not hasattr(module, "languages"): raise Exception
			languages = getattr(module, "languages")
			if hasattr(module, "version") is False: raise Exception
			plugin_version = getattr(module, "version")
			if hasattr(module, "class_name") is False: raise Exception
			plugin_name = class_name = getattr(module, "class_name")
			if hasattr(module, class_name) is False: raise Exception
			PluginClass = getattr(module, class_name)
			if hasattr(PluginClass, "__init__") is False: raise Exception
			if hasattr(PluginClass, "load") is False: raise Exception
			if hasattr(PluginClass, "unload") is False: raise Exception
		except ValueError:
			from Exceptions import DoNotLoadError
			raise DoNotLoadError
		except:
			from Exceptions import PluginModuleValidationError
			raise PluginModuleValidationError
		return plugin_name, plugin_version, PluginClass, languages

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
		from Exceptions import InvalidLanguagePluginError
		try:
			if not (filename.startswith("Plugin") and filename.endswith(".py")): return False
			from os import path
			filepath = path.join(plugin_folder, filename)
			from imp import load_source
			module = load_source(filename[:-3], filepath)
			plugin_name, plugin_version, PluginClass, languages = self.__get_module_info(module)
			if not (self.__editor.language.get_id() in languages): raise InvalidLanguagePluginError
			self.__plugin_modules.add(module)
			self.__unload_duplicate_plugins(plugin_name, plugin_version)
			plugin_object = self.__load_plugin(PluginClass)
			self.__plugin_objects.add((plugin_name, plugin_version, plugin_object))
		except InvalidLanguagePluginError:
			pass
		except PluginModuleValidationError:
			print "Validation Error: ", filename
		except DuplicatePluginError:
			print "Duplicate Plugin: ", (plugin_name, plugin_version)
		except DoNotLoadError:
			#print "Not loading: ", (filename)
			self.__plugin_modules.add(module)
		return False

	def __load_plugin(self, PluginClass):
		"""
		Load a plugin.

		@param self: Reference to the PluginManager instance.
		@type self: A PluginManager object.
		"""
		plugin_object = PluginClass(self.__editor)
		plugin_object.load()
		return plugin_object

	def __unload_plugin(self, plugin_info):
		"""
		Unload specific plugin.

		@param self: Reference to the PluginManager instance.
		@type self: A PluginManager object.

		@param plugin_info: Information of plugin information.
		@type plugin_info: A Tuple object.
		"""
		plugin_object = plugin_info[2]
		plugin_object.unload()
		self.__plugin_objects.remove(plugin_info)
		return False

	def __load_plugins(self):
		"""
		Load all plugins.

		@param self: Reference to the PluginManager instance.
		@type self: A PluginManager object.
		"""
		if self.__editor.language is None: return False
		from os import listdir
		from gobject import idle_add, PRIORITY_LOW
		core_files = listdir(self.__editor.core_language_plugin_folder)
		for filename in core_files:
			idle_add(self.__init_module, filename, self.__editor.core_language_plugin_folder, priority=PRIORITY_LOW)
		home_files = listdir(self.__editor.home_language_plugin_folder)
		for filename in home_files:
			idle_add(self.__init_module, filename, self.__editor.home_language_plugin_folder, priority=PRIORITY_LOW)
		return False

	def __unload_plugins(self):
		"""
		Unload plugins.

		@param self: Reference to the PluginManager instance.
		@type self: A PluginManager object.
		"""
		map(self.__unload_plugin, self.__plugin_objects.copy())
		if self.__is_quiting: self.__destroy()
		return False

	def __reload_plugins(self):
		"""
		Unload then load all plugins.

		@param self: Reference to the PluginManager instance.
		@type self: A PluginManager object.
		"""
		self.__unload_plugins()
		self.__load_plugins()
		return False

	def __reload_cb(self, *args):
		"""
		Handles callback to reload plugins.

		@param self: Reference to the PluginManager instance.
		@type self: A PluginManager object.
		"""
		self.__reload_plugins()
		return False

	def __quit_cb(self, *args):
		"""
		Destroy plugin manager.

		@param self: Reference to the PluginManager instance.
		@type self: A PluginManager object.
		"""
		if not self.__plugin_objects: return self.__destroy()
		self.__is_quiting = True
		from gobject import idle_add
		idle_add(self.__unload_plugins)
		return False
