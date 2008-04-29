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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Scribes; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

"""
Documents a class that shows the editor's color editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2006 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import SIGNAL_RUN_LAST, TYPE_NONE, GObject, TYPE_PYOBJECT

class Manager(GObject):
	"""
	This class is the GUI manager for the color editor.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"show-window": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"can-remove": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"remove-theme": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize instance of this class.

		@param self: Reference to the ColorEditorManager instance.
		@type self: A ColorEditorManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		from Window import Window
		Window(editor, self)
		from RemoveButton import RemoveButton
		RemoveButton(editor, self)
		from TreeView import TreeView
		TreeView(editor, self)

	def show_window(self):
		"""
		Show the editor's preferences dialog.

		@param self: Reference to the ColorEditorManager instance.
		@type self: A ColorEditorManager object.
		"""
		self.emit("show-window")
		return

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the ColorEditorManager instance.
		@type self: A ColorEditorManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		from os.path import join
		glade_file = join(editor.get_current_folder(globals()), "SyntaxColorThemes.glade")
		from gtk.glade import XML
		self.__glade = XML(glade_file, "Window", "scribes")
		return

	def __get_glade(self):
		return self.__glade

	glade = property(__get_glade)

	def destroy(self):
		self.emit("destroy")
		del self
		self = None
		return
