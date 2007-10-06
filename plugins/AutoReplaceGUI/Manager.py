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
This module documents a class that manages all GUI components of the
automatic replacement dialog.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2006 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_PYOBJECT

class AutoReplaceGUIManager(GObject):
	"""
	This class implements an object that manages the graphic components
	of the automatic replacement dialog.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize the object.

		@param self: Reference to the AutoReplaceGUIManager instance.
		@type self: An AutoReplaceGUIManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		self.__arrange_widgets()
		self.__signal_id_1 = self.connect("destroy", self.__manager_destroy_cb)
		self.__signal_id_2 = self.__close_button.connect("clicked", self.__manager_clicked_cb)

	def __get_treeview(self):
		return self.__treeview

	def __get_add_button(self):
		return self.__add_button

	def __get_edit_button(self):
		return self.__edit_button

	def __get_remove_button(self):
		return self.__remove_button

	treeview = property(__get_treeview, doc="Treeview for the auto replacement dialog.")
	add_button = property(__get_add_button, doc="Add button for the auto replacement dialog")
	edit_button = property(__get_edit_button, doc="Edit button for the auto replacement dialog")
	remove_button = property(__get_remove_button, doc="Remove button for the auto replacement dialog")

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the AutoReplaceGUIManager instance.
		@type self: An AutoReplaceGUIManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		from Window import AutoReplaceWindow
		self.__window = AutoReplaceWindow(self, editor)
		from Treeview import AutoReplaceTreeView
		self.__treeview = AutoReplaceTreeView(self, editor)
		from AddButton import AutoReplaceAddButton
		self.__add_button = AutoReplaceAddButton(self, editor)
		from EditButton import AutoReplaceEditButton
		self.__edit_button = AutoReplaceEditButton(self, editor)
		from RemoveButton import AutoReplaceRemoveButton
		self.__remove_button = AutoReplaceRemoveButton(self, editor)
		self.__enable_button = None
		self.__disable_button = None
		from gtk import STOCK_CLOSE, Button
		self.__close_button = Button(stock=STOCK_CLOSE, use_underline=True)
		self.__signal_id_1 = None
		self.__signal_id_2 = None
		return

	def __arrange_widgets(self):
		"""
		Arrange automatic replacement dialog GUI components.

		@param self: Reference to the AutoReplaceGUIManager instance.
		@type self: An AutoReplaceGUIManager object.
		"""
		from gtk import HBox, VBox
		scrolled_window = self.__editor.create_scrollwin()
		scrolled_window.add(self.__treeview)
		main_container = HBox(homogeneous=False, spacing=10)
		self.__window.main_area.pack_start(main_container, True, True, 0)
		main_container.pack_start(scrolled_window, True, True, 0)
		button_container = VBox(homogeneous=False, spacing=7)
		main_container.pack_start(button_container, False, False, 0)
		button_container.pack_start(self.__add_button, False, False, 0)
		button_container.pack_start(self.__edit_button, False, False, 0)
		button_container.pack_start(self.__remove_button, False, False, 0)
		self.__window.button_area.pack_start(self.__close_button, False, False, 0)
		return

	def __manager_destroy_cb(self, manager):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the AutoReplaceGUIManager instance.
		@type self: An AutoReplaceGUIManager object.

		@param manager: Reference to the AutoReplaceGUIManager instance.
		@type manager: An AutoReplaceGUIManager object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_2, self.__close_button)
		self.__editor.disconnect_signal(self.__signal_id_1, self)
		self.__close_button.destroy()
		del self
		self = None
		return

	def __manager_clicked_cb(self, button):
		"""
		Handles callback when the "clicked" signal is emitted.

		@param self: Reference to the AutoReplaceGUIManager instance.
		@type self: An AutoReplaceGUIManager object.

		@param button: Reference to the close button.
		@type button: A gtk.Button object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		self.__window.hide_dialog()
		return False

	def show(self):
		"""
		Show the automatic replacement dialog.

		@param self: Reference to the AutoReplaceGUIManager instance.
		@type self: An AutoReplaceGUIManager object.
		"""
		self.__window.show_dialog()
		return
