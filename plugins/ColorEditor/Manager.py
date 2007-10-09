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
Documents a class that shows the editor's color editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2006 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import SIGNAL_RUN_LAST, TYPE_NONE, GObject

class ColorEditorManager(GObject):
	"""
	This class is the GUI manager for the color editor.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"populate": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize instance of this class.

		@param self: Reference to the ColorEditorManager instance.
		@type self: A ColorEditorManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		self.__arrange_widgets()
		self.__signal_id_1 = self.__close_button.connect("clicked", self.__clicked_cb)
		self.__signal_id_2 = self.connect("destroy", self.__destroy_cb)

	def show_dialog(self):
		"""
		Show the editor's preferences dialog.

		@param self: Reference to the ColorEditorManager instance.
		@type self: A ColorEditorManager object.
		"""
		self.emit("populate")
		self.__window.show_dialog()
		return

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the ColorEditorManager instance.
		@type self: A ColorEditorManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		from Window import ColorEditorWindow
		self.__window = ColorEditorWindow(self, editor)
		from ThemeCheckButton import ThemeCheckButton
		self.__theme_check_button = ThemeCheckButton(self, editor)
		from FgColorButton import ForegroundButton
		self.__foreground_color_button = ForegroundButton(self, editor)
		from BgColorButton import BackgroundButton
		self.__background_color_button = BackgroundButton(self, editor)
		from TreeView import ColorEditorTreeView
		self.__treeview = ColorEditorTreeView(self, editor)
		from FgSyntaxButton import ForegroundSyntaxButton
		self.__foreground_syntax_color_button = ForegroundSyntaxButton(editor, self)
		from BgSyntaxButton import BackgroundSyntaxButton
		self.__background_syntax_color_button = BackgroundSyntaxButton(editor, self)
		from BoldCheckButton import BoldCheckButton
		self.__bold_check_button = BoldCheckButton(editor, self)
		from ItalicCheckButton import ItalicCheckButton
		self.__italic_check_button = ItalicCheckButton(editor, self)
		from UnderlineCheckButton import UnderlineCheckButton
		self.__underline_check_button = UnderlineCheckButton(editor, self)
		from ResetButton import ResetButton
		self.__reset_button = ResetButton(editor, self)
		from gtk import STOCK_CLOSE, Button
		self.__close_button = Button(stock=STOCK_CLOSE, use_underline=True) # (Done)
		self.__label = self.__create_labels()
		self.__signal_id_1 = self.__signal_id_2 = None
		return

	def __get_treeview(self):
		return self.__treeview

	treeview = property(__get_treeview)

	def __arrange_widgets(self):
		"""
		Arrange the widgets of the preferences dialog.

		@param self: Reference to the PreferenceDialog instance.
		@type self: A PreferenceDialog object.
		"""
		self.__window.main_area.set_spacing(10)
		self.__window.main_area.pack_start(self.__theme_check_button, False, False, 0)
		from gtk import HBox, VBox, Label, Alignment
		maincontainer = HBox(homogeneous=False, spacing=10)
		self.__window.main_area.pack_start(maincontainer, False, False, 0)
		container = HBox(homogeneous=False, spacing=10)
		container.pack_start(self.__label[0], False, False, 0)
		container.pack_start(self.__foreground_color_button, True, True, 0)
		maincontainer.pack_start(container, True, True, 0)
		self.__window.button_area.pack_start(self.__close_button, False, False, 0)
		container = HBox(homogeneous=False, spacing=10)
		container.pack_start(self.__label[1], False, False, 0)
		container.pack_start(self.__background_color_button, True, True, 0)
		maincontainer.pack_start(container, True, True, 0)
		scrollwin = self.__editor.create_scrollwin()
		scrollwin.add(self.__treeview)
		container = HBox(homogeneous=False, spacing=10)
		self.__window.main_area.pack_start(container, True, True, 0)
		container.pack_start(scrollwin, True, True, 0)
		vcontainer = VBox(homogeneous=False, spacing=10)
		alignment = Alignment(yalign=0.5)
		alignment.add(vcontainer)
		container.pack_start(alignment, False, False, 0)
		container = HBox(homogeneous=False, spacing=10)
		container.pack_start(self.__label[2], False, False, 0)
		container.pack_start(self.__foreground_syntax_color_button, False, False, 0)
		vcontainer.pack_start(container, False, False, 0)
		container = HBox(homogeneous=False, spacing=10)
		container.pack_start(self.__label[3], False, False, 0)
		container.pack_start(self.__background_syntax_color_button, False, False, 0)
		vcontainer.pack_start(container, False, False, 0)
		vcontainer.pack_start(self.__bold_check_button, False, False, 0)
		vcontainer.pack_start(self.__italic_check_button, False, False, 0)
		vcontainer.pack_start(self.__underline_check_button, False, False, 0)
		vcontainer.pack_start(self.__reset_button, False, False, 0)
		return

	def __clicked_cb(self, button):
		"""
		Handles callback when the "clicked" signal is emitted.

		@param self: Reference to the PreferenceDialog instance.
		@type self: A PreferenceDialog object.

		@param button: The close button.
		@type button: A Button object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		self.__window.hide_dialog()
		return True

	def __destroy_cb(self, manager):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the ColorEditorManager instance.
		@type self: A ColorEditorManager object.

		@param manager: Reference to the ColorEditorManager instance.
		@type manager: A ColorEditorManager object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self.__close_button)
		self.__editor.disconnect_signal(self.__signal_id_2, self)
		self.__close_button.destroy()
		del self
		self = None
		return

	def __create_labels(self):
		"""
		Create all labels for the preferences dialog.

		@param self: Reference to the PreferenceDialog instance.
		@type self: A PreferenceDialog object.

		@return: A list of labels for the dialog.
		@rtype: A List object.
		"""
		from i18n import msg0007, msg0008, msg0009, msg0010
		from collections import deque
		string_list = deque([msg0007, msg0008, msg0009, msg0010])
		labels = map(self.__convert_string_to_label, string_list)
		return deque(labels)

	def __convert_string_to_label(self, string):
		from gtk import Label
		label = Label(string)
		label.set_use_underline(True)
		label.set_use_markup(True)
		return label
