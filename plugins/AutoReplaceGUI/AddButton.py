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
This module documents a class that creates a button to add words for
automatic replacement.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2006 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import Button

class AutoReplaceAddButton(Button):
	"""
	This class creates a button used to add words for automatic replacement
	to the automatic replacement dialog.
	"""

	def __init__(self, manager):
		"""
		Initialize the object.

		@param self: Reference to the AutoReplaceAddButton instance.
		@type self: An AutoReplaceAddButton object.

		@param manager: Reference to the AutoReplaceGUIManager instance.
		@type manager: An AutoReplaceGUIManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		from gtk import STOCK_ADD
		Button.__init__(self, stock=STOCK_ADD, use_underline=True)
		self.__init_attributes(manager)
		self.__signal_id_1 = self.__manager.connect("destroy", self.__button_destroy_cb)
		self.__signal_id_2 = self.connect("clicked", self.__button_clicked_cb)

	def __init_attributes(self, manager):
		"""
		Initialize data attributes.

		@param self: Reference to the AutoReplaceAddButton instance.
		@type self: An AutoReplaceAddButton object.

		@param manager: Reference to the AutoReplaceGUIManager instance.
		@type manager: An AutoReplaceGUIManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__manager = manager
		self.__signal_id_1 = None
		self.__signal_id_2 = None
		return

	def __button_destroy_cb(self, manager):
		"""
		Handles callback when "destroy" signal is emitted.

		@param self: Reference to the AutoReplaceAddButton instance.
		@type self: An AutoReplaceAddButton object.

		@param manager: Reference to the AutoReplaceGUIManager instance.
		@type manager: An AutoReplaceGUIManager object.
		"""
		from SCRIBES.utils import disconnect_signal, delete_attributes
		disconnect_signal(self.__signal_id_1, self.__manager)
		disconnect_signal(self.__signal_id_2, self)
		self.destroy()
		delete_attributes(self)
		del self
		self = None
		return

	def __button_clicked_cb(self, button):
		"""
		Handles callback when the "clicked" signal is emitted.

		@param self: Reference to the AutoReplaceAddButton instance.
		@type self: An AutoReplaceAddButton object.

		@param button: Reference to the AutoReplaceAddButton instance.
		@type button: An AutoReplaceAddButton object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		self.__manager.treeview.set_property("sensitive", True)
		model = self.__manager.treeview.get_model()
		iterator = model.append()
		path = model.get_path(iterator)
		column = self.__manager.treeview.get_column(0)
		self.__manager.treeview.set_cursor(path=path, focus_column=column, start_editing=True)
		return False
