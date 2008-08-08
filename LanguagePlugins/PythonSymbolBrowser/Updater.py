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
		self.__init_attributes(editor, manager)
		self.__sig_id1 = manager.connect("show-window", self.__show_window_cb)

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
#		finally:
#			from gc import collect
#			collect()
		return False

	def __extract_symbols(self, nodes, depth):
		self.__depth = depth
		class_flag = False
		function_flag = False
		is_func_node = self.__is_function_node
		is_class_node = self.__is_class_node
		func_depth = self.__function_depth
		class_depth = self.__class_depth
		fpixbuf = self.__manager.function_pixbuf
		mpixbuf = self.__manager.method_pixbuf
		cpixbuf = self.__manager.class_pixbuf
		sappend = self.__symbols.append
		extract_symbols = self.__extract_symbols
		for node in nodes:
			if is_func_node(node):
				function_flag = True
				if func_depth:
					value = "Function"
				else:
					value = "Method" if class_depth else "Function"
				pixbuf = fpixbuf if value == "Function" else mpixbuf
				sappend((node.lineno, node.name, value, depth, pixbuf))
				func_depth += 1
			if is_class_node(node):
				class_flag = True
				sappend((node.lineno, node.name, "Class", depth, cpixbuf))
				class_depth += 1
			extract_symbols(node.getChildNodes(), depth+1)
			if class_flag: class_depth -= 1
			if function_flag: func_depth -= 1
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
		idle_add(self.__get_symbols, priority=9999)
		return
