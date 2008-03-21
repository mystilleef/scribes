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
This module documents a class that manages graphic user interface
components of the symbol browser.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE
from gobject import TYPE_PYOBJECT

class Manager(GObject):
	"""
	This class manages graphic user interface components of the symbol
	browser.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"update": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"show-window": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"hide-window": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize object.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		from Updater import Updater
		Updater(editor, self)
		from TreeView import TreeView
		TreeView(editor, self)
		from Window import Window
		Window(editor, self)

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		from os.path import join, split
		current_folder = split(globals()["__file__"])[0]
		glade_file = join(current_folder, "SymbolBrowser.glade")
		from gtk.gdk import pixbuf_new_from_file
		class_pixbuf = join(current_folder, "class.png")
		self.__class_pixbuf = pixbuf_new_from_file(class_pixbuf)
		function_pixbuf = join(current_folder, "function.png")
		self.__function_pixbuf = pixbuf_new_from_file(function_pixbuf)
		from gtk.glade import XML
		method_pixbuf = join(current_folder, "method.png")
		self.__method_pixbuf = pixbuf_new_from_file(method_pixbuf)
		from gtk.glade import XML
		self.__glade = XML(glade_file, "Window", "scribes")
		return

	def __get_glade(self):
		return self.__glade

	def __get_class_pixbuf(self):
		return self.__class_pixbuf

	def __get_function_pixbuf(self):
		return self.__function_pixbuf

	def __get_method_pixbuf(self):
		return self.__method_pixbuf

	glade = property(__get_glade)
	class_pixbuf = property(__get_class_pixbuf)
	function_pixbuf = property(__get_function_pixbuf)
	method_pixbuf = property(__get_method_pixbuf)

	def show_browser(self):
		"""
		Show the document browser.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		self.emit("show-window")
		return

	def destroy(self):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		self.emit("destroy")
		del self
		self = None
		return
