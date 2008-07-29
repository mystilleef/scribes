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
This module documents a class that performs bookmark operations for the
text editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_PYOBJECT

class Manager(GObject):

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"show-window": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"hide-window": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"process-fileinfo": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"fileinfo": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		self.__init_attributes(editor)
		from FileInfo import FileInfo
		FileInfo(self, editor)
		from Window import Window
		Window(self, editor)
		from NameLabel import Label
		Label(self, editor)
		from TypeLabel import Label
		Label(self, editor)
		from SizeLabel import Label
		Label(self, editor)
		from LocationLabel import Label
		Label(self, editor)
		from MIMELabel import Label
		Label(self, editor)
		from LinesLabel import Label
		Label(self, editor)
		from WordsLabel import Label
		Label(self, editor)
		from CharactersLabel import Label
		Label(self, editor)
		from ModifiedLabel import Label
		Label(self, editor)
		from AccessedLabel import Label
		Label(self, editor)

	def __init_attributes(self, editor):
		from os.path import join
		current_folder = editor.get_current_folder(globals())
		glade_file = join(current_folder, "DocumentStatistics.glade")
		from gtk.glade import XML
		self.__glade = XML(glade_file, "Window", "scribes")
		return

	def __get_glade(self):
		return self.__glade

	glade = property(__get_glade)

	def show(self):
		self.emit("process-fileinfo")
		self.emit("show-window")
		return

	def destroy(self):
		self.emit("destroy")
		del self
		self = None
		return
