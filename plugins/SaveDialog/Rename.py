# -*- coding: utf-8 -*-
# Copyright © 2005 Lateef Alabi-Oki
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
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
This module exposes a class responsible for changing the name associated with a
document.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class NameChangeProcessor(object):
	"""
	This class creates an object that changes the name associated with a
	document. It ensures that the state and integrity of the text editor remain
	valid regardless of the outcome of the renaming operation.
	"""

	def __init__(self, editor, newuri):
		"""
		Initialize the NameChangeProcessor object and begin the process of
		changing the text editor's name and state.

		@param self: Reference to the NameChangeProcessor instance.
		@type self: A NameChangeProcessor object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param newuri: The new URI to associate with the document.
		@type newuri: A String object.
		"""
		self.__init_attributes(editor, newuri)
		self.__rename_document()

	def __init_attributes(self, editor, newuri):
		"""
		Initialize the objects attributes

		@param self: Reference to the NameChangeProcessor instance.
		@type self: A NameChangeProcessor object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param newuri: The new URI to associate with the document.
		@type newuri: A String object.
		"""
		self.editor = editor
		self.newuri = newuri
		self.olduri = editor.uri
		return

	def __rename_document(self):
		"""
		Save the new document.

		@param self: Reference to the NameChangeProcessor instance.
		@type self: A NameChangeProcessor object.
		"""
		self.editor.emit("renamed-document", self.newuri)
		if self.editor.is_readonly: self.editor.trigger("toggle_readonly")
		self.editor.trigger("save_file")
		self.destroy()
		return

	def destroy(self):
		"""
		Destroy the name changing object.

		@param self: Reference to the NameChangeProcessor instance.
		@type self: A NameChangeProcessor object.
		"""
		del self
		self = None
		return
