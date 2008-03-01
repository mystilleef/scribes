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

class EncodingSelectionWindow(object):
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
		self.__init_attributes(editor)
		self.__setup_treeview()
		self.__populate_model()
		self.__sig_id_1 = self.__treeview.connect("map-event", self.__map_event_cb)
		self.__sig_id_2 = self.__window.connect("delete-event", self.__delete_event_cb)
		self.__sig_id_3 = self.__window.connect("key-press-event", self.__key_press_event_cb)
		self.__sig_id_4 = self.__renderer.connect("toggled", self.__toggled_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the dialog's attributes.

		@param self: Reference to the ScribesEncodingDialog instance.
		@type self: A ScribesEncodingDialog object.

		@param parent_window: Reference to the text editor's window.
		@type parent_window: A gtk.Window object.
		"""
		self.__editor = editor
		from os.path import join
		glade_file = join(editor.scribes_data_folder, "EncodingSelectionWindow.glade")
		from gtk.glade import XML
		glade = XML(glade_file, "EncodingSelectionWindow")
		self.__window = glade.get_widget("EncodingSelectionWindow")
		self.__treeview = glade.get_widget("EncodingSelectionWindowTreeView")
		self.__model = self.__create_model()
		from utils import generate_encodings
		self.__encodings = generate_encodings()
		from gtk import CellRendererToggle
		self.__renderer = CellRendererToggle()
		return

	def show(self):
		"""
		Show window.

		@param self: Reference to the EncodingSelectionWindow instance.
		@type self: An EncodingSelectionWindow object.
		"""
		self.__window.show_all()
		return

	def hide(self):
		"""
		Hide window.

		@param self: Reference to the EncodingSelectionWindow instance.
		@type self: An EncodingSelectionWindow object.
		"""
		self.__window.hide()
		return

	def destroy(self):
		"""
		Destroy object.

		@param self: Reference to the EncodingSelectionWindow instance.
		@type self: An EncodingSelectionWindow object.
		"""
		self.__editor.disconnect_signal(self.__sig_id_1, self.__treeview)
		self.__editor.disconnect_signal(self.__sig_id_2, self.__window)
		self.__editor.disconnect_signal(self.__sig_id_3, self.__window)
		self.__editor.disconnect_signal(self.__sig_id_3, self.__renderer)
		self.__treeview.destroy()
		self.__window.destroy()
		del self
		self = None
		return

	def __set_properties(self):
		"""
		Initialize the dialog's properties.

		@param self: Reference to the ScribesEncodingDialog instance.
		@type self: A ScribesEncodingDialog object.
		"""
		width, heigth = self.__editor.calculate_resolution_independence(self.__editor.window,
														1.6, 1.6)
		self.__window.set_property("default-width", width)
		self.__window.set_property("default-height", heigth)
		self.__window.set_transient_for_window(self.__editor.window)
		return

########################################################################
#
#								ListStore/Model
#
########################################################################

	def __create_model(self):
		"""
		Create the model for the encoding dialog view.

		@param self: Reference to the EncodingSelectionWindow instance.
		@type self: A EncodingSelectionWindow object.
		"""
		from gtk import ListStore
		from gobject import TYPE_BOOLEAN
		model = ListStore(TYPE_BOOLEAN, str, str)
		return model

	def __populate_model(self):
		"""
		Populate the encoding model with encoding information.

		@param self: Reference to the ScribesEncodingDialog instance.
		@type self: A ScribesEncodingDialog object.
		"""
		from EncodingMetadata import get_value
		encoding_list = get_value()
		for encoding in self.__encodings:
			select = True if encoding[0] in encoding_list else False
			self.__model.append([select, encoding[0], encoding[2]])
		return

################################################################################
#
#							Encoding View
#
################################################################################

	def __setup_treeview(self):
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
		view = self.__treeview
		self.__renderer.set_property("activatable", True)
		# Create a column for selecting encodings.
		column = TreeViewColumn(msg0163, self.__renderer)
		view.append_column(column)
		column.set_expand(False)
		column.set_sizing(TREE_VIEW_COLUMN_AUTOSIZE)
		column.add_attribute(self.__renderer, "active", 0)
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
		view.set_model(self.__model)
		view.columns_autosize()
		#view.set_enable_search(True)
		return

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
		from EncodingMetadata import get_value, set_value
		encoding_list = get_value()
		# Toggle the check button in the select column
		self.__model[path][0] = not self.__model[path][0]
		# If the check button is toggled on, add the character encoding on that
		# row # to GConf's encoding database, otherwise remove the encoding on
		# that row from GConf's encoding database.
		if self.__model[path][0]:
			# Add liststore to gconf database
			encoding_list.append(self.__model[path][1])
			set_value(encoding_list)
		else:
			# Remove liststore from gconf database
			if self.__model[path][1] in encoding_list:
				encoding_list.remove(self.__model[path][1])
				set_value(encoding_list)
		return True

	def __map_event_cb(self, *args):
		"""
		Handles callback when "map-event" is emitted.

		@param self: Reference to the EncodingSelectionWindow instance.
		@type self: An EncodingSelectionWindow object.
		"""
		self.__treeview.grab_focus()
		return True

	def __delete_event_cb(self, *args):
		"""
		Handles callback when "delete-event" is emitted.

		@param self: Reference to the EncodingSelectionWindow instance.
		@type self: An EncodingSelectionWindow object.
		"""
		self.hide()
		return True

	def __key_press_event_cb(self, window, event):
		"""
		Handles callback when the "key-press-event" is emitted.

		@param self: Reference to the EncodingSelectionWindow instance.
		@type self: An EncodingSelectionWindow object.

		@param window: The encoding selection window.
		@type window: A gtk.Window object.

		@param event: An event.
		@type event: A gtk.Event object.
		"""
		# Hide window when escape key is pressed.
		from gtk import keysyms
		if (event.keyval == keysyms.Escape): self.hide()
		return False
