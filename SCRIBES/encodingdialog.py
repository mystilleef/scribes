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
This module exposes a class that implements an encoding dialog for the text
editor. The encoding dialog allows users to add or remove encodings to a list.
The encodings in the list can then be used to open or save files.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from dialog import ScribesDialog

class ScribesEncodingDialog(ScribesDialog):
	"""
	This class produces an object that represents an encoding dialog. The dialog
	is a simple front end that enables users add or remove encodings in an
	encoding list in the text editor's GConf database. The dialog inherits its
	base behavior and properties from ScribesDialog. See the dialog.py module
	for implementation details.
	"""

	def __init__(self, editor):
		"""
		Initialize the encoding dialog behavior and properties.

		@param self: Reference to the ScribesEncodingDialog instance.
		@type self: A ScribesEncodingDialog object.

		@param editor: Reference to a text editor instance.
		@type editor: An Editor object.
		"""
		ScribesDialog.__init__(self, editor)
		self.__init_attributes(editor)
		self.__set_properties()
		self.__arrange_dialog_widgets()

	def __init_attributes(self, editor):
		"""
		Initialize the dialog's attributes.

		@param self: Reference to the ScribesEncodingDialog instance.
		@type self: A ScribesEncodingDialog object.

		@param parent_window: Reference to the text editor's window.
		@type parent_window: A gtk.Window object.
		"""
		self.editor = editor
		self.client = editor.gconf_client
		from utils import generate_encodings
		self.encodings = generate_encodings()
		self.model = self.__create_encoding_model()
		self.view = self.__create_encoding_view()
		return

	def __set_properties(self):
		"""
		Initialize the dialog's properties.

		@param self: Reference to the ScribesEncodingDialog instance.
		@type self: A ScribesEncodingDialog object.
		"""
		from utils import calculate_resolution_independence
		width, heigth = calculate_resolution_independence(self.editor.window,
														1.6, 1.6)
		from internationalization import msg0160
		self.set_property("title", msg0160)
		self.set_property("role", "encoding_dialog")
		self.set_property("name", "encodingdialog")
		self.set_property("default-width", width)
		self.set_property("default-height", heigth)
		self.set_property("icon-name", "text-editor")
		self.set_property("border-width", 10)
		self.vbox.set_spacing(10)
		from gtk import STOCK_CLOSE, RESPONSE_CLOSE
		self.add_button(STOCK_CLOSE, RESPONSE_CLOSE)
		return

	def __arrange_dialog_widgets(self):
		"""
		Pack widgets appropriately into the dialog.

		@param self: Reference to the ScribesEncodingDialog instance.
		@type self: A ScribesEncodingDialog object.
		"""
		from utils import create_scrollwin
		scrollwin = create_scrollwin()
		scrollwin.add(self.view)
		self.vbox.pack_start(scrollwin, True, True, 0)
		return

	def show_dialog(self):
		self.show_all()
		self.run()
		self.hide()
		return

################################################################################
#
#								ListStore/Model
#
################################################################################

	def __create_encoding_model(self):
		"""
		Create the model for the encoding dialog view.

		@param self: Reference to the ScribesEncodingDialog instance.
		@type self: A ScribesEncodingDialog object.
		"""
		from gtk import ListStore
		from gobject import TYPE_BOOLEAN
		model = ListStore(TYPE_BOOLEAN, str, str)
		return model

	def __populate_encoding_model(self):
		"""
		Populate the encoding model with encoding information.

		@param self: Reference to the ScribesEncodingDialog instance.
		@type self: A ScribesEncodingDialog object.
		"""
		from gconf import VALUE_STRING
		encoding_list = self.client.get_list("/apps/scribes/encodings",
											VALUE_STRING)
		for encoding in self.encodings:
			if encoding[0] in encoding_list:
				select = True
			else:
				select = False
			self.model.append([select, encoding[0], encoding[2]])
		return

################################################################################
#
#							Encoding View
#
################################################################################

	def __create_encoding_view(self):
		"""
		Create the view for the encoding dialog.

		@param self: Reference to the ScribesEncodingDialog instance.
		@type self: A ScribesEncodingDialog object.

		@return: A view holding encodings and associated information.
		@rtype: A gtk.TreeView object.
		"""
		from gtk import TreeView, CellRendererToggle, TreeViewColumn
		from gtk import TREE_VIEW_COLUMN_AUTOSIZE, CellRendererText
		from gtk import SORT_DESCENDING
		from internationalization import msg0163, msg0162, msg0161
		view = TreeView()
		# Create the renderer for the select column.
		renderer = CellRendererToggle()
		renderer.connect("toggled", self.__toggled_cb)
		renderer.set_property("activatable", True)
		# Create a column for selecting encodings.
		column = TreeViewColumn(msg0163, renderer)
		view.append_column(column)
		column.set_expand(False)
		column.set_sizing(TREE_VIEW_COLUMN_AUTOSIZE)
		column.add_attribute(renderer, "active", 0)
		column.set_sort_indicator(True)
		column.set_sort_order(SORT_DESCENDING)
		column.set_sort_column_id(0)
		# Create a renderer for the character encoding column.
		renderer = CellRendererText()
		# Create a column for character encoding.
		column = TreeViewColumn(msg0162, renderer, text=1)
		view.append_column(column)
		column.set_expand(True)
		column.set_sizing(TREE_VIEW_COLUMN_AUTOSIZE)
		column.set_sort_indicator(True)
		column.set_sort_order(SORT_DESCENDING)
		column.set_sort_column_id(1)
		# Create the renderer for the Language column
		renderer = CellRendererText()
		# Create a column for Language and Region and set the column's properties.
		column = TreeViewColumn(msg0161, renderer, text=2)
		view.append_column(column)
		column.set_expand(True)
		column.set_sizing(TREE_VIEW_COLUMN_AUTOSIZE)
		column.set_sort_indicator(True)
		column.set_sort_order(SORT_DESCENDING)
		column.set_sort_column_id(2)
		# Set treeview properties
		self.__populate_encoding_model()
		view.set_model(self.model)
		view.columns_autosize()
		view.set_enable_search(True)
		view.set_property("rules-hint", True)
		view.connect("map-event", self.__view_map_event_cb)
		return view

	def __toggled_cb(self, renderer, path):
		"""
		Handles callback when toggle button in the select column is toggled on
		or off.

		@param self: Reference to the ScribesEncodingDialog instance.
		@type self: A ScribesEncodingDialog object.

		@param renderer: A renderer containing a toggle button.
		@type renderer: A CellRendererToggle object.

		@param path: A row in treeview
		@type path: A gtk.Path object.
		"""
		from gconf import VALUE_STRING
		encoding_list = self.client.get_list("/apps/scribes/encodings",
											VALUE_STRING)
		# Toggle the check button in the select column
		self.model[path][0] = not self.model[path][0]
		# If the check button is toggled on, add the character encoding on that
		# row # to GConf's encoding database, otherwise remove the encoding on
		# that row from GConf's encoding database.
		if self.model[path][0]:
			# Add liststore to gconf database
			encoding_list.append(self.model[path][1])
			self.client.set_list("/apps/scribes/encodings", VALUE_STRING,
								encoding_list)
		else:
			# Remove liststore from gconf database
			if self.model[path][1] in encoding_list:
				encoding_list.remove(self.model[path][1])
				self.client.set_list("/apps/scribes/encodings", VALUE_STRING,
									encoding_list)
		self.client.notify("/apps/scribes/encodings")
		return True

	def __view_map_event_cb(self, view, event):
		view.grab_focus()
		return True
