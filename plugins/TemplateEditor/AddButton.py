# -*- coding: utf-8 -*-
# Copyright © 2007 Lateef Alabi-Oki
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
This module documents a class that defines the behavior of the edit
button on the template editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class AddButton(object):
	"""
	This class defines the behavior of the edit button.
	"""

	def __init__(self, manager, editor):
		"""
		Initialize object.

		@param self: Reference to the AddButton instance.
		@type self: An AddButton object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(manager, editor)
		self.__signal_id_1 = manager.connect("destroy", self.__destroy_cb)
		self.__signal_id_2 = manager.connect("language-selected", self.__language_selected_cb)
		self.__signal_id_3 = self.__button.connect("clicked", self.__clicked_cb)

	def __init_attributes(self, manager, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the AddButton instance.
		@type self: An AddButton object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__manager = manager
		self.__editor = editor
		self.__language = None
		self.__dialog = None
		self.__button = manager.glade.get_widget("AddButton")
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		return

	def __destroy_cb(self, manager):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the ExportButton instance.
		@type self: A ExportButton object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, manager)
		self.__editor.disconnect_signal(self.__signal_id_2, manager)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__button)
		self.__button.destroy()
		self = None
		del self
		return

	def __language_selected_cb(self, manager, language):
		"""
		Handles callback when the "language-selected" signal is emitted.

		@param self: Reference to the AddButton instance.
		@type self: An AddButton object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param data: Selection information.
		@type data: A Tuple object.
		"""
		self.__language = language
		return

	def __clicked_cb(self, button):
		"""
		Handles callback when the "clicked" signal is emitted.

		@param self: Reference to the AddButton instance.
		@type self: An AddButton object.

		@param button: Reference to the AddButton instance.
		@type button: An AddButton object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		try:
			self.__dialog.show()
		except AttributeError:
			from AddDialog import AddDialog
			self.__dialog = AddDialog(self.__manager, self.__editor, self.__language)
			self.__dialog.show()
		return True
