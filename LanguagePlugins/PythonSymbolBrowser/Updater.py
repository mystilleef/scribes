# -*- coding: utf-8 -*-
# Copyright © 2008 Lateef Alabi-Oki
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
This module documents a class that updates the symbols in a python
file.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

class Updater(object):
	"""
	This class updates symbols in a python source code.
	"""

	def __init__(self, editor, manager):
		"""
		Initialize object.

		@param self: Reference to the Updater instance.
		@type self: An Updater object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param manager: Reference to the manager object.
		@type manager: A Manager object.
		"""
		self.__init_attributes(editor, manager)
		self.__sig_id1 = manager.connect("show-window", self.__show_window_cb)
#		from gobject import idle_add, PRIORITY_LOW
#		idle_add(self.__precompile_method, priority=PRIORITY_LOW)

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		self.__sig_id1 = None
		from collections import deque
		# symbols has the format [(line_number, name, type), ...]
		self.__symbols = deque([])
		self.__depth = 0
		self.__inside_class = False
		self.__class_depth = 0
		self.__function_depth = 0
		return

	def __get_symbols(self):
		try:
			self.__symbols.clear()
			from compiler import parse
			parse_tree = parse(self.__editor.get_text())
			nodes = parse_tree.getChildNodes()
			self.__extract_symbols(nodes, 0)
			self.__manager.emit("update", self.__symbols)
		except SyntaxError:
			pass
		finally:
			from gc import collect
			collect()
		return False

	def __extract_symbols(self, nodes, depth):
		self.__depth = depth
		class_flag = False
		function_flag = False
		for node in nodes:
			if self.__is_function_node(node):
				function_flag = True
				if self.__function_depth:
					value = "Function"
				else:
					value = "Method" if self.__class_depth else "Function"
				pixbuf = self.__manager.function_pixbuf if value == "Function" else self.__manager.method_pixbuf
				self.__symbols.append((node.lineno, node.name, value, depth, pixbuf))
				self.__function_depth += 1
			if self.__is_class_node(node):
				class_flag = True
				self.__symbols.append((node.lineno, node.name, "Class", depth, self.__manager.class_pixbuf))
				self.__class_depth	+= 1
			self.__extract_symbols(node.getChildNodes(), depth+1)
			if class_flag: self.__class_depth -= 1
			if function_flag: self.__function_depth -= 1
			class_flag = False
			function_flag = False
		return

	def __is_function_node(self, node):
		attributes = set(["decorators", "name", "argnames", "defaults", "flags", "doc", "code"])
		return attributes.issubset(set(dir(node)))

	def __is_class_node(self, node):
		attributes = set(["name", "bases", "doc", "code"])
		return attributes.issubset(set(dir(node)))

	def __precompile_method(self):
		try:
			from psyco import bind
			bind(self.__get_symbols)
			bind(self.__extract_symbols)
		except ImportError:
			pass
		return False

	def __show_window_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__get_symbols, priority=2000)
		return
