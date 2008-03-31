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
from gobject import TYPE_PYOBJECT

class Manager(GObject):
	"""
	This class manages each component of the advanced configuration
	window. Communication between components are done via this classes
	instance.
	"""

	__gsignals__ = {
		"show-window": (SIGNAL_ACTION|SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"show-chooser-window": (SIGNAL_ACTION|SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"hide-chooser-window": (SIGNAL_ACTION|SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"destroy": (SIGNAL_ACTION|SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"selected-placeholder": (SIGNAL_ACTION|SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"selected-file": (SIGNAL_ACTION|SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"new-folder": (SIGNAL_ACTION|SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
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
		from ForkScribesCheckButton import CheckButton
		CheckButton(editor, self)
		from BracketSelectionColorButton import ColorButton
		ColorButton(editor, self)
		from UnsavedFolderComboBox import ComboBox
		ComboBox(editor, self)
		from Window import Window
		Window(editor, self)

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
		open_glade_file = join(current_folder, "FileChooser.glade")
		from gtk.glade import XML
		self.__glade = XML(glade_file, "Window", "scribes")
		self.__open_glade = XML(open_glade_file, "Window", "scribes")
		self.__signal_id_1 = None
		return

	def __get_glade(self):
		"""
		Private getter method (python property) for the glade GUI
		"""
		return self.__glade

	def __get_filechooser_glade(self):
		return self.__open_glade

	def __destroy(self):
		"""
		Destroy object.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		del self
		self = None
		return

	# Public API reference to the advanced configuration window GUI
	glade = property(__get_glade)
	filechooser_glade = property(__get_filechooser_glade)

	def show(self):
		"""
		Show advanced configuration window.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		self.emit("show-window")
		return

	def destroy(self):
		"""
		Destroy object.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		self.emit("destroy")
		self.__destroy()
		return
