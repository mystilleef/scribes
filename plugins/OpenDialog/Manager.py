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
This modules documents a class that manages essential components of the
open dialog file chooser.

@author: Lateef Alabi-Oki
@organization: Scribes
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_PYOBJECT

class Manager(GObject):
	"""
	This class manages the components of the filechooser window.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"show-window": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"hide-window": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"load-files": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"selected-file": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
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
		from thread import start_new_thread
		from OpenButton import Button
		start_new_thread(Button, (editor, self))
		from Window import Window
		start_new_thread(Window, (editor, self))
#		from CancelButton import Button
#		start_new_thread(Button, (editor, self))
		from FileChooser import FileChooser
		start_new_thread(FileChooser, (editor, self))

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
		glade_file = join(current_folder, "OpenDialog.glade")
		from gtk.glade import XML
		self.__glade = XML(glade_file, "Window", "scribes")
		return

	def __get_glade(self):
		return self.__glade

	glade = property(__get_glade)

	def show_dialog(self):
		"""
		Show the open file chooser dialog.

		@param self: Reference to the Manager instance.
		@type self: A Manager object.
		"""
		#self.emit("show-window")
		from thread import start_new_thread
		start_new_thread(self.emit, ("show-window",))
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
