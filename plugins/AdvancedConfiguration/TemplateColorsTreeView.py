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
This module documents a class that implements the treeview widget for
changing template place holder colors.

@author: Lateef Alabi-Oki
@organization: Scribes
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

class TreeView(object):
	"""
	This class defines the behavior of the treeview when changing
	template colors.
	"""

	def __init__(self, editor, manager):
		"""
		Initialize object.

		@param self: Reference to the TreeView instance.
		@type self: A TreeView object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param manager: Object that manages all window components.
		@type manager: A Manager object.
		"""
		self.__init_attributes(editor, manager)
		self.__setup_treeview()
		self.__populate_model()
		self.__treeview.set_property("sensitive", True)

	def __init_attributes(self, editor, manager):
		"""
		Initialize data attributes.

		@param self: Reference to the TreeView instance.
		@type self: A TreeView object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param manager: Object that manages all window components.
		@type manager: A Manager object.
		"""
		self.__editor = editor
		self.__manager = manager
		self.__treeview = manager.glade.get_widget("TemplateColorsTreeView")
		self.__model = self.__create_model()
		return

	def __create_model(self):
		"""
		Create the model for the encoding dialog view.

		@param self: Reference to the EncodingSelectionWindow instance.
		@type self: A EncodingSelectionWindow object.
		"""
		from gtk import ListStore
		model = ListStore(str)
		return model

	def __setup_treeview(self):
		"""
		Setup the treeview.

		@param self: Reference to the TreeView instance.
		@type self: A TreeView object.
		"""
		from gtk import TreeView, TreeViewColumn
		from gtk import TREE_VIEW_COLUMN_AUTOSIZE, CellRendererText
		view = self.__treeview
		renderer = CellRendererText()
		from i18n import msg0001
		column = TreeViewColumn(msg0001, renderer, text=0)
		view.append_column(column)
		column.set_expand(True)
		column.set_sizing(TREE_VIEW_COLUMN_AUTOSIZE)
		view.set_model(self.__model)
		view.set_enable_search(True)
		view.columns_autosize()
		return

	def __populate_model(self):
		"""
		Populate treeview.

		@param self: Reference to the TreeView instance.
		@type self: A TreeView object.
		"""
		from i18n import msg0002, msg0003, msg0004, msg0005
		self.__model.clear()
		self.__model.append([msg0002])
		self.__model.append([msg0003])
		self.__model.append([msg0004])
		self.__model.append([msg0005])
		self.__treeview.columns_autosize()
		return
