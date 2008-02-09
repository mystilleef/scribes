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
This module documents a class responsible for managing each component of
the advanced configuration window.

@author: Lateef Alabi-Oki
@organization: Scribes
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

from gobject import SIGNAL_ACTION, SIGNAL_RUN_LAST, TYPE_NONE, GObject

class Manager(GObject):
	"""
	This class manages each component of the advanced configuration
	window. Communication between components are doing via the object
	of this class.
	"""

	__gsignals__ = {
		"show-window": (SIGNAL_ACTION|SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"destroy": (SIGNAL_ACTION|SIGNAL_RUN_LAST, TYPE_NONE, ()),
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
		from Window import Window
		Window(editor, self)
		from thread import start_new_thread
		from ForkScribesCheckButton import CheckButton
		start_new_thread(CheckButton, (editor, self))
		from BracketSelectionColorButton import ColorButton
		start_new_thread(ColorButton, (editor, self))
		from TemplateColorsTreeView import TreeView
		start_new_thread(TreeView, (editor, self))

	def __init_attributes(self, editor):
		"""
		Initialize object's attributes.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		self.__editor = editor
		from os.path import join, split
		current_folder = split(globals()["__file__"])[0]
		glade_file = join(current_folder, "AdvancedConfigurationWindow.glade")
		from gtk.glade import XML
		self.__glade = XML(glade_file, "Window", "scribes")
		self.__signal_id_1 = None
		return

	def __get_glade(self):
		return self.__glade

	def __destroy(self):
		del self
		self = None
		return

	glade = property(__get_glade)

	def show(self):
		self.emit("show-window")
		return

	def destroy(self):
		self.emit("destroy")
		self.__destroy()
		return
