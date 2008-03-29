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
This module documents a class that manages the components of a file
chooser object.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

class Manager(object):
	"""
	This class manages components of the file chooser objec.t
	"""

	def __init__(self, editor, manager):
		"""
		Initialize object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param manager: Object that manages components of the advanced configuration window.
		@type manager: A Manager object.
		"""
		self.__init_attributes(editor, manager)
#		from FileChooserOpenButton import Button
#		Button(editor, manager)
#		from FileChooser import FileChooser
#		FileChooser(editor, manager)
#		from FileChooserCancelButton import Button
#		Button(editor, manager)
		from FileChooserWindow import Window
		Window(editor, manager)

	def __init_attributes(self, editor, manager):
		"""
		Initialize attributes.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param manager: Object that manages components of the advanced configuration window.
		@type manager: A Manager object.
		"""
		self.__editor = editor
		self.__manager = manager
		return

	def show(self):
		self.__manager.emit("show-chooser-window")
		return
