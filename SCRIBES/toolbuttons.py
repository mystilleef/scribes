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
This modules implements a base class for all toolbar buttons for the text
editor. All toolbar button objects should inherit from this class implemented
in this class to provide a consistent look, feel and behavior in the text
editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import ToolButton, ToolItem, MenuToolButton

class ScribesToolButton(ToolButton):
	"""
	This class creates toolbar buttons for the text editor. The class is
	implemented for the sole purpose of being inherited. It inherits
	from gtk.ToolButton. See the PyGTK, or GTK+, manual for more information.
	"""

	def __init__(self):
		"""
		Initialize a toolbar button for the text editor.

		@param self: Reference to the ScribesToolButton instance.
		@type self: A ScribesToolButton object.
		"""
		ToolButton.__init__(self)
		from tooltips import create_tooltips
		self.tooltips = create_tooltips()
		self.__set_properties()

	def __set_properties(self):
		"""
		Set the properties for the toolbar buttons for the text editor.

		@param self: Reference to the ScribesToolButton instance.
		@type self: A ScribesToolButton object.

		@return: True to call this function again, False otherwise.
		@rtype: A Boolean object.
		"""
		self.set_homogeneous(True)
		self.set_expand(False)
		self.set_use_drag_window(False)
		self.set_is_important(False)
		return False

class NewToolButton(ScribesToolButton):
	"""
	This class creates a toolbar button object responsible for launching new
	instances of the text editor.
	"""

	def __init__(self, editor):
		"""
		Initialize the new file toolbar button.

		@param self: Reference to the NewToolButton instance.
		@type self: A NewToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		ScribesToolButton.__init__(self)
		self.status_id = None
		from gtk import STOCK_NEW
		self.set_stock_id(STOCK_NEW)
		from tooltips import new_button_tip
		self.set_tooltip(self.tooltips, new_button_tip)
		self.connect("clicked", self.__toolbutton_clicked_cb, editor)

	def __toolbutton_clicked_cb(self, toolbutton, editor):
		"""
		Handles callback when the text editor's toolbutton "clicked" signal is
		emitted.

		This function spawns a new instance of the text editor.

		@param self: Reference to the NewToolButton instance.
		@type self: A NewToolButton object.

		@param toolbutton: Reference to the NewToolButton instance.
		@type toolbutton: A NewToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		editor.trigger("new_window")
		return True

class OpenToolButton(MenuToolButton):
	"""
	This class creates a toolbar button object responsible for displaying the
	text editor's open dialog.
	"""

	def __init__(self, editor):
		"""
		Initialize the open dialog toolbar button.

		@param self: Reference to the OpenToolButton instance.
		@type self: An OpenToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		from gtk import STOCK_OPEN
		MenuToolButton.__init__(self, STOCK_OPEN)
		from tooltips import open_button_tip, recent_menu_tip
		self.set_tooltip(editor.tip, open_button_tip)
		self.set_menu(editor.recent_menu)
		self.set_arrow_tooltip(editor.tip, recent_menu_tip, recent_menu_tip)
		self.connect("clicked", self.__toolbutton_clicked_cb, editor)

	def __toolbutton_clicked_cb(self, toolbutton, editor):
		"""
		Handles callback when the "clicked" signal is emitted.

		This function displays the text editor's open dialog. The dialog is used
		to select and load documents.

		@param self: Reference to the OpenToolButton instance.
		@type self: An OpenToolButton object.

		@param toolbutton: Reference to the OpenToolButton instance.
		@type toolbutton: An OpenToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		editor.trigger("show_open_dialog")
		return True

class SaveToolButton(ScribesToolButton):
	"""
	This class creates a toolbar button object responsible for displaying the
	text editor's save dialog.
	"""

	def __init__(self, editor):
		"""
		Initialize the save dialog toolbar button.

		@param self: Reference to the SaveToolButton instance.
		@type self: A SaveToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		ScribesToolButton.__init__(self)
		from gtk import STOCK_SAVE_AS
		self.set_stock_id(STOCK_SAVE_AS)
		from tooltips import save_button_tip
		self.set_tooltip(self.tooltips, save_button_tip)
		self.connect("clicked", self.__toolbutton_clicked_cb, editor)
		editor.connect("loading-document", self.__toolbutton_loading_document_cb)
		editor.connect("loaded-document", self.__toolbutton_loaded_document_cb)
		editor.connect("load-error", self.__toolbutton_load_error_cb)

	def __toolbutton_clicked_cb(self, toolbutton, editor):
		"""
		Handles callback when the "clicked" signal is emitted.

		This function displays the text editor's save dialog. The save dialog is
		used to rename a document.

		@param self: Reference to the SaveToolButton instance.
		@type self: A SaveToolButton object.

		@param toolbutton: Reference to the SaveToolButton instance.
		@type toolbutton: A SaveToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		editor.trigger("show_save_dialog")
		return True

	def __toolbutton_loading_document_cb(self, editor, uri):
		"""
		Handles callback when the "loading-document" signal is emitted.

		This function makes the save dialog toolbar button insensitive when the
		text editor is loading a document.

		@param self: Reference to the SaveToolButton instance.
		@type self: A SaveToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.set_property("sensitive", False)
		return

	def __toolbutton_loaded_document_cb(self, *args):
		"""
		Handles callback when the "loaded-document" signal is emitted.

		This function makes the save dialog toolbar button sensitive when the
		text editor successfully finished loading a document.

		@param self: Reference to the SaveToolButton instance.
		@type self: A SaveToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.set_property("sensitive", True)
		return

	def __toolbutton_load_error_cb(self, editor, uri):
		"""
		Handles callback when the "load-error" signal is emitted.

		@param self: Reference to the SaveToolButton instance.
		@type self: A SaveToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.set_property("sensitive", True)
		return

class PrintToolButton(ScribesToolButton):
	"""
	This class creates a toolbar button object responsible for displaying the
	text editor's print dialog.
	"""

	def __init__(self, editor):
		"""
		Initialize the print dialog toolbar button.

		@param self: Reference to the PrintToolButton instance.
		@type self: A PrintToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		ScribesToolButton.__init__(self)
		from gtk import STOCK_PRINT
		self.set_stock_id(STOCK_PRINT)
		from tooltips import print_button_tip
		self.set_tooltip(self.tooltips, print_button_tip)
		self.connect("clicked", self.__toolbutton_clicked_cb, editor)
		editor.connect("loading-document", self.__toolbutton_loading_document_cb)
		editor.connect("loaded-document", self.__toolbutton_loaded_document_cb)
		editor.connect("load-error", self.__toolbutton_load_error_cb)

	def __toolbutton_clicked_cb(self, toolbutton, editor):
		"""
		Handles callback when the "clicked" signal is emitted.

		This function shows the text editor's print dialog.

		@param self: Reference to the PrintToolButton instance.
		@type self: A PrintToolButton object.

		@param toolbutton: Reference to the PrintToolButton instance.
		@type toolbutton: A PrintToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		editor.trigger("show_print_dialog")
		return True

	def __toolbutton_loading_document_cb(self, editor, uri):
		"""
		Handles callback when the "loading-document" signal is emitted.

		This function makes the print dialog toolbar button insensitive when
		the text editor is loading a document.

		@param self: Reference to the PrintToolButton instance.
		@type self: A PrintToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.set_property("sensitive", False)
		return

	def __toolbutton_loaded_document_cb(self, *args):
		"""
		Handles callback when the "loaded-document" signal is emitted.

		@param self: Reference to the PrintToolButton instance.
		@type self: A PrintToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.set_property("sensitive", True)
		return

	def __toolbutton_load_error_cb(self, editor, uri):
		"""
		Handles callback when the "load-error" signal is emitted.

		@param self: Reference to the PrintToolButton instance.
		@type self: A PrintToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.set_property("sensitive", True)
		return

class UndoToolButton(ScribesToolButton):
	"""
	This class creates a toolbar button object responsible for undoing text
	operations.
	"""

	def __init__(self, editor):
		"""
		Initialize the undo toolbar button.

		@param self: Reference to the UndoToolButton instance.
		@type self: An UndoToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		ScribesToolButton.__init__(self)
		self.set_property("sensitive", False)
		from gtk import STOCK_UNDO
		self.set_stock_id(STOCK_UNDO)
		from tooltips import undo_button_tip
		self.set_tooltip(self.tooltips, undo_button_tip)
		self.connect("clicked", self.__toolbutton_clicked_cb, editor)
		editor.connect("enable-readonly", self.__toolbutton_enable_readonly_cb)
		editor.connect("disable-readonly", self.__toolbutton_disable_readonly_cb)
		editor.connect("gui-created", self.__toolbutton_gui_created_cb)

	def __toolbutton_clicked_cb(self, toolbutton, editor):
		editor.trigger("undo_action")
		return True

	def __toolbutton_enable_readonly_cb(self, editor):
		"""
		Handles callback when the "enable-readonly" signal is emitted.

		@param self: Reference to the UndoToolButton instance.
		@type self: An UndoToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.set_property("sensitive", False)
		return

	def __toolbutton_disable_readonly_cb(self, editor):
		"""
		Handles callback when the "disable-readonly" signal is emitted.

		@param self: Reference to the UndoToolButton instance.
		@type self: An UndoToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		if editor.textbuffer.can_undo():
			self.set_property("sensitive", True)
		else:
			self.set_property("sensitive", False)
		return

	def __toolbutton_gui_created_cb(self, editor):
		"""
		Handles callback when the "gui-created" signal is emitted.

		@param self: Reference to the RedoToolButton instance.
		@type self: A RedoToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		editor.textview.connect("undo", self.__toolbutton_undo_cb, editor)
		editor.textbuffer.connect("can-undo", self.__toolbutton_can_undo_cb, editor)
		return

	def __toolbutton_undo_cb(self, textview, editor):
		"""
		Handles callback when the "undo" signal is emitted.

		@param self: Reference to the UndoToolButton instance.
		@type self: An UndoToolButton object.

		@param textview: The text editor's buffer container, view.
		@type textview: A gtk.TextView object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		if editor.textbuffer.can_undo():
			self.set_property("sensitive", True)
		else:
			self.set_property("sensitive", False)
		return True

	def __toolbutton_can_undo_cb(self, textbuffer, can_undo, editor):
		"""
		Handles callback when the "can-undo" signal is emitted.

		@param textbuffer: The text editor's buffer.
		@type textbuffer: A gtk.TextBuffer object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		if editor.textbuffer.can_undo():
			self.set_property("sensitive", True)
		else:
			self.set_property("sensitive", False)
		return True

class RedoToolButton(ScribesToolButton):
	"""
	This class creates a toolbar button object responsible for redoing undone
	text operations.
	"""

	def __init__(self, editor):
		"""
		Initialize the redo toolbar button.

		@param self: Reference to the RedoToolButton instance.
		@type self: A RedoToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		ScribesToolButton.__init__(self)
		self.set_property("sensitive", False)
		from gtk import STOCK_REDO
		self.set_stock_id(STOCK_REDO)
		from tooltips import redo_button_tip
		self.set_tooltip(self.tooltips, redo_button_tip)
		self.connect("clicked", self.__toolbutton_clicked_cb, editor)
		editor.connect("enable-readonly", self.__toolbutton_enable_readonly_cb)
		editor.connect("disable-readonly", self.__toolbutton_disable_readonly_cb)
		editor.connect("gui-created", self.__toolbutton_gui_created_cb)

	def __toolbutton_clicked_cb(self, toolbutton, editor):
		editor.trigger("redo_action")
		return True

	def __toolbutton_gui_created_cb(self, editor):
		"""
		Handles callback when the "gui-created" signal is emitted.

		@param self: Reference to the RedoToolButton instance.
		@type self: A RedoToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		editor.textview.connect("redo", self.__toolbutton_redo_cb, editor)
		editor.textbuffer.connect("can-redo", self.__toolbutton_can_redo_cb, editor)
		return

	def __toolbutton_enable_readonly_cb(self, editor):
		"""
		Handles callback when the "enable-readonly" signal is emitted.

		@param self: Reference to the RedoToolButton instance.
		@type self: A RedoToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.set_property("sensitive", False)
		return

	def __toolbutton_disable_readonly_cb(self, editor):
		"""
		Handles callback when the "disable-readonly" signal is emitted.

		@param self: Reference to the RedoToolButton instance.
		@type self: A RedoToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		if editor.textbuffer.can_redo():
			self.set_property("sensitive", True)
		else:
			self.set_property("sensitive", False)
		return

	def __toolbutton_redo_cb(self, textview, editor):
		"""
		Handles callback when the "redo" signal is emitted.

		@param self: Reference to the RedoToolButton instance.
		@type self: A RedoToolButton object.

		@param textview: The text editor's buffer container, view.
		@type textview: A gtk.TextView object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		if editor.textbuffer.can_redo():
			self.set_property("sensitive", True)
		else:
			self.set_property("sensitive", False)
		return True

	def __toolbutton_can_redo_cb(self, textbuffer, can_redo, editor):
		"""
		Handles callback when the "can-redo" signal is emitted.

		@param self: Reference to the RedoToolButton instance.
		@type self: A RedoToolButton object.

		@param textbuffer: The text editor's buffer.
		@type textbuffer: A gtk.TextBuffer object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		if editor.textbuffer.can_redo():
			self.set_property("sensitive", True)
		else:
			self.set_property("sensitive", False)
		return True

class GotoToolButton(ScribesToolButton):
	"""
	This class creates a toolbar button object responsible for displaying the
	text editor's goto bar.
	"""

	def __init__(self, editor):
		"""
		Initialize the gotobar toolbutton.

		@param self: Reference to the GotoToolButton instance.
		@type self: A GotoToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		ScribesToolButton.__init__(self)
		from gtk import STOCK_JUMP_TO
		self.set_stock_id(STOCK_JUMP_TO)
		from tooltips import goto_button_tip
		self.set_tooltip(self.tooltips, goto_button_tip)
		self.connect("clicked", self.__toolbutton_clicked_cb, editor)
		editor.connect("loading-document", self.__toolbutton_loading_document_cb)
		editor.connect("loaded-document", self.__toolbutton_loaded_document_cb)
		editor.connect("load-error", self.__toolbutton_load_error_cb)

	def __toolbutton_clicked_cb(self, toolbutton, editor):
		editor.trigger("show_gotobar")
		return True

	def __toolbutton_loading_document_cb(self, editor, uri):
		"""
		Handles callback when the "loading-document" signal is emitted.

		@param self: Reference to the GotoToolButton instance.
		@type self: A GotoToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.set_property("sensitive", False)
		return

	def __toolbutton_loaded_document_cb(self, *args):
		"""
		Handles callback when the "loaded-document" signal is emitted.

		@param self: Reference to the GotoToolButton instance.
		@type self: A GotoToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.set_property("sensitive", True)
		return

	def __toolbutton_load_error_cb(self, editor, uri):
		"""
		Handles callback when the "load-error" signal is emitted.

		@param self: Reference to the GotoToolButton instance.
		@type self: A GotoToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.set_property("sensitive", True)
		return

class SearchToolButton(ScribesToolButton):
	"""
	This class creates a toolbar button object responsible for displaying the
	text editor's find bar.
	"""

	def __init__(self, editor):
		"""
		Initialize the findbar toolbutton.

		@param self: Reference to the SearchToolButton instance.
		@type self: A SearchToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		ScribesToolButton.__init__(self)
		from gtk import STOCK_FIND
		self.set_stock_id(STOCK_FIND)
		from tooltips import find_button_tip
		self.set_tooltip(self.tooltips, find_button_tip)
		self.connect("clicked", self.__toolbutton_clicked_cb, editor)
		editor.connect("loading-document", self.__toolbutton_loading_document_cb)
		editor.connect("loaded-document", self.__toolbutton_loaded_document_cb)
		editor.connect("load-error", self.__toolbutton_load_error_cb)

	def __toolbutton_clicked_cb(self, toolbutton, editor):
		editor.trigger("show_findbar")
		return True

	def __toolbutton_loading_document_cb(self, editor, uri):
		"""
		Handles callback when the "loading-document" signal is emitted.

		@param self: Reference to the SearchToolButton instance.
		@type self: A SearchToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.set_property("sensitive", False)
		return

	def __toolbutton_loaded_document_cb(self, *args):
		"""
		Handles callback when the "loaded-document" signal is emitted.

		@param self: Reference to the SearchToolButton instance.
		@type self: A SearchToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.set_property("sensitive", True)
		return

	def __toolbutton_load_error_cb(self, editor, uri):
		"""
		Handles callback when the "load-error" signal is emitted.

		@param self: Reference to the SearchToolButton instance.
		@type self: A SearchToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.set_property("sensitive", True)
		return

class ReplaceToolButton(ScribesToolButton):
	"""
	This class creates a toolbar button object responsible for displaying the
	text editor's replacebar.
	"""

	def __init__(self, editor):
		"""
		Initialize the replacebar toolbutton.

		@param self: Reference to the ReplaceToolButton instance.
		@type self: A ReplaceToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		ScribesToolButton.__init__(self)
		from gtk import STOCK_FIND_AND_REPLACE
		self.set_stock_id(STOCK_FIND_AND_REPLACE)
		from tooltips import replace_button_tip
		self.set_tooltip(self.tooltips, replace_button_tip)
		self.connect("clicked", self.__toolbutton_clicked_cb, editor)
		editor.connect("loading-document", self.__toolbutton_loading_document_cb)
		editor.connect("loaded-document", self.__toolbutton_loaded_document_cb)
		editor.connect("enable-readonly", self.__toolbutton_enable_readonly_cb)
		editor.connect("disable-readonly", self.__toolbutton_disable_readonly_cb)
		editor.connect("load-error", self.__toolbutton_load_error_cb)

	def __toolbutton_clicked_cb(self, toolbutton, editor):
		editor.trigger("show_replacebar")
		return True

	def __toolbutton_loading_document_cb(self, editor, uri):
		"""
		Handles callback when the "loading-document" signal is emitted.

		@param self: Reference to the ReplaceToolButton instance.
		@type self: A ReplaceToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.set_property("sensitive", False)
		return

	def __toolbutton_enable_readonly_cb(self, editor):
		"""
		Handles callback when the "enable-readonly" signal is emitted.

		@param self: Reference to the ReplaceToolButton instance.
		@type self: A ReplaceToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.set_property("sensitive", False)
		return

	def __toolbutton_disable_readonly_cb(self, editor):
		"""
		Handles callback when the "enable-readwrite" signal is emitted.

		@param self: Reference to the ReplaceToolButton instance.
		@type self: A ReplaceToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.set_property("sensitive", True)
		return

	def __toolbutton_loaded_document_cb(self, *args):
		"""
		Handles callback when the "loaded-document" signal is emitted.

		@param self: Reference to the ReplaceToolButton instance.
		@type self: A ReplaceToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.set_property("sensitive", True)
		return

	def __toolbutton_load_error_cb(self, editor, uri):
		"""
		Handles callback when the "load-error" signal is emitted.

		@param self: Reference to the ReplaceToolButton instance.
		@type self: A ReplaceToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.set_property("sensitive", True)
		return

class PrefToolButton(MenuToolButton):
	"""
	This class creates a toolbar button object responsible for displaying the
	text editor's preferences dialog.
	"""

	def __init__(self, editor):
		"""
		Initialize the preferences dialog toolbutton.

		@param self: Reference to the PrefToolButton instance.
		@type self: A PrefToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		from gtk import STOCK_PREFERENCES
		MenuToolButton.__init__(self, STOCK_PREFERENCES)
		from tooltips import pref_button_tip, arrow_button_tip
		self.set_tooltip(editor.tip, pref_button_tip)
		self.set_menu(editor.preference_menu)
		self.set_arrow_tooltip(editor.tip, arrow_button_tip, arrow_button_tip)
		self.connect("clicked", self.__toolbutton_clicked_cb, editor)
		editor.connect("loading-document", self.__toolbutton_loading_document_cb)
		editor.connect("loaded-document", self.__toolbutton_loaded_document_cb)
		editor.connect("load-error", self.__toolbutton_load_error_cb)

	def __toolbutton_clicked_cb(self, toolbutton, editor):
		editor.trigger("show_preference_dialog")
		return True

	def __toolbutton_loading_document_cb(self, editor, uri):
		"""
		Handles callback when the "loading-document" signal is emitted.

		@param self: Reference to the PrefToolButton instance.
		@type self: A PrefToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.set_property("sensitive", False)
		return

	def __toolbutton_loaded_document_cb(self, *args):
		"""
		Handles callback when the "loaded-document" signal is emitted.

		@param self: Reference to the PrefToolButton instance.
		@type self: A PrefToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.set_property("sensitive", True)
		return

	def __toolbutton_load_error_cb(self, editor, uri):
		"""
		Handles callback when the "load-error" signal is emitted.

		@param self: Reference to the PrefToolButton instance.
		@type self: A PrefToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.set_property("sensitive", True)
		return

class HelpToolButton(ScribesToolButton):
	"""
	This class creates a toolbar button object responsible for displaying the
	text editor's help toolbutton.
	"""

	def __init__(self, editor):
		"""
		Initialize the help browser toolbutton.

		@param self: Reference to the HelpToolButton instance.
		@type self: A HelpToolButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		ScribesToolButton.__init__(self)
		from gtk import STOCK_HELP
		self.set_stock_id(STOCK_HELP)
		from tooltips import help_button_tip
		self.set_tooltip(self.tooltips, help_button_tip)
		self.connect("clicked", self.__toolbutton_clicked_cb, editor)

	def __toolbutton_clicked_cb(self, toolbutton, editor):
		editor.trigger("show_user_guide")
		return True

class Spinner(ToolItem):
	"""
	This class creates the throbber for text editor.
	"""

	def __init__(self):
		ToolItem.__init__(self)
		self.__init_attributes()
		self.add(self.inactive_spinner_image)

	def __init_attributes(self):
		from utils import create_image, find_file
		self.active_spinner_file = find_file("throbber-active.gif")
		self.inactive_spinner_image = create_image("throbber-inactive.png")
		self.pixbuf = self.inactive_spinner_image.get_pixbuf()
		from gtk.gdk import PixbufAnimation
		self.animation = PixbufAnimation(self.active_spinner_file)
		return
