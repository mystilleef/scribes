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
This module documents a class that manages the open dialog for adding new
color themes

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

from gobject import SIGNAL_RUN_LAST, TYPE_NONE, GObject, TYPE_PYOBJECT

class Manager(GObject):
	"""
	This class manages the open dialog for adding new color themes
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"show": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"hide": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"selected-file": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
		"load-schemes": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		self.__init_attributes(editor)
		from DialogWindow import Window
		Window(editor, self)
		from FileChooser import FileChooser
		FileChooser(editor, self)

	def __init_attributes(self, editor):
		self.__editor = editor
		from os.path import join
		glade_file = join(editor.get_current_folder(globals()), "Dialog.glade")
		from gtk.glade import XML
		self.__glade = XML(glade_file, "Window", "scribes")
		return

	def __get_glade(self):
		return self.__glade

	glade = property(__get_glade)

	def show(self):
		self.emit("show")
		return

	def destroy(self):
		self.emit("destroy")
		del self
		self = None
		return

