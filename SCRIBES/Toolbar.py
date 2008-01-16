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
This module implements a class responsible for creating a toolbar object for
text editor instances.

GTKUIManager is not used because previous attempts have proven that it is
inflexible for the project's purposes.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import Toolbar

class ScribesToolbar(Toolbar):
	"""
	This class creates the toolbar object for text editor instances. The toolbar
	object houses toolitems, or toolbar buttons, that allow users to perform
	actions such as launching a new instance of the text editor, opening a
	document, or renaming a document, printing the contents of the text editor
	buffer and so on. It inherits from gtk.Toolbar.
	"""

	def __init__(self, editor):
		"""
		Initialize a toolbar object for the text editor and populate it with
		toolitems.

		@param self: Reference to the toolbar instance.
		@type self: A ScribesToolbar object.
		"""
		Toolbar.__init__(self)
		self.__init_attributes(editor)
		self.__set_properties()
		self.__populate_toolbar(editor)
		self.__set_toolbar_visibility()
		self.__signal_id_1 = editor.connect("close-document", self.__close_document_cb)
		self.__signal_id_2 = editor.connect("close-document-no-save", self.__close_document_cb)
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monitor_id_1 = monitor_add(self.__database_uri, MONITOR_FILE,
					self.__hide_toolbar_cb)

	def __get_visibility(self):
		return self.__is_visible

	is_visible = property(__get_visibility, doc="Whether or not the toolbar is visible")

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the Toolbar instance.
		@type self: A Toolbar object.
		"""
		self.__editor = editor
		# Initialize gconf, the gnome configuration system
		self.__is_visible = False
		self.__registration_id = editor.register_object()
		self.__signal_id_1 = self.__signal_id_2 = None
		from os.path import join
		preference_folder = join(editor.metadata_folder, "Preferences")
		database_path = join(preference_folder, "MinimalMode.gdb")
		from gnomevfs import get_uri_from_local_path
		self.__database_uri = get_uri_from_local_path(database_path)
		return

	def __set_properties(self):
		"""
		Setup the default properties of the toolbar for the text editor.

		@param self: Reference to the ScribesToolbar instance.
		@type self: A ScribesToolbar object.
		"""
		from gtk import ORIENTATION_HORIZONTAL, TOOLBAR_ICONS
		self.set_no_show_all(True)
		self.set_property("orientation", ORIENTATION_HORIZONTAL)
		self.set_property("toolbar-style", TOOLBAR_ICONS)
		self.set_property("show-arrow", True)
		return False

	def __populate_toolbar(self, editor):
		"""
		Populate the text editor's toolbar with toolitems.

		@param self: Reference to the ScribesToolbar instance.
		@type self: A ScribesToolbar object.
		"""
		from toolbuttons import NewToolButton, OpenToolButton, SaveToolButton
		from toolbuttons import PrintToolButton, UndoToolButton
		from toolbuttons import RedoToolButton, GotoToolButton, SearchToolButton
		from toolbuttons import ReplaceToolButton, PrefToolButton
		from toolbuttons import HelpToolButton
		# Create the new file toolbutton.
		self.insert(NewToolButton(editor), 0)

		# Create the open file toolbutton.
		self.insert(OpenToolButton(editor), 1)

		# Create the save file toolbutton.
		self.insert(SaveToolButton(editor), 2)

		# Create a toolbar separator.
		from gtk import SeparatorToolItem
		separator = SeparatorToolItem()
		separator.set_draw(True)
		self.insert(separator, 3)

		# Create the print toolbutton.
		self.insert(PrintToolButton(editor), 4)

		# Create a toolbar separator.
		separator = SeparatorToolItem()
		separator.set_draw(True)
		self.insert(separator, 5)

		# Create the undo toolbutton.
		self.insert(UndoToolButton(editor), 6)

		# Create the redo toolbutton.
		self.insert(RedoToolButton(editor), 7)

		# Create a separator.
		separator = SeparatorToolItem()
		separator.set_draw(True)
		self.insert(separator, 8)

		# Create the goto line toolbutton.
		self.insert(GotoToolButton(editor), 9)

		# Create the find toolbutton.
		self.insert(SearchToolButton(editor), 10)

		# Create the replace toolbutton.
		self.insert(ReplaceToolButton(editor), 11)

		# Create a separator.
		separator = SeparatorToolItem()
		separator.set_draw(True)
		self.insert(separator, 12)

		# Create the preferences menu toolbutton.
		self.insert(PrefToolButton(editor), 13)

		# Create the help toolbutton.
		self.insert(HelpToolButton(editor), 14)

		# Create a separator.
		separator = SeparatorToolItem()
		separator.set_expand(True)
		separator.set_draw(False)
		self.insert(separator, 15)

		# Create the Spinner.
		from Spinner import Spinner
		self.insert(Spinner(self.__editor), 16)
		return False

	def __destroy(self):
		"""
		Destroy instance of this class.

		@param self: Reference to the Store instance.
		@type self: A Store object.
		"""
		# Disconnect signals.
		self.__editor.disconnect_signal(self.__signal_id_1, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__editor)
		self.destroy()
		from gnomevfs import monitor_cancel
		if self.__monitor_id_1: monitor_cancel(self.__monitor_id_1)
		# Unregister object so that editor can quit.
		self.__editor.unregister_object(self.__registration_id)
		# Delete data attributes.
		del self
		self = None
		return

	def __close_document_cb(self, editor):
		"""
		Handles callback when the "close-document" signal is emitted.

		@param self: Reference to the Store instance.
		@type self: A Store object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__destroy()
		return

	def __set_toolbar_visibility(self):
		"""
		Determine whether to show the toolbar.

		@param self: Reference to the Toolbar instance.
		@type self: A Toolbar object.
		"""
		self.set_no_show_all(False)
		from MinimalModeMetadata import get_value
		hide_toolbar = get_value()
		if hide_toolbar:
			self.__is_visible = False
			self.hide_all()
		else:
			self.__is_visible = True
			self.show_all()
		self.set_no_show_all(True)
		return

	def __hide_toolbar_cb(self, *args):
		self.__set_toolbar_visibility()
		return
