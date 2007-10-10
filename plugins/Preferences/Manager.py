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
Documents a class that shows the editor's preferences dialog.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2006 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import SIGNAL_RUN_LAST, TYPE_NONE, GObject

class PreferencesManager(GObject):
	"""
	This class is the GUI manager for the preferences dialog.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize instance of this class.

		@param self: Reference to the PreferencesManager instance.
		@type self: A PreferencesManager object.

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

		@param self: Reference to the PreferencesManager instance.
		@type self: A PreferencesManager object.
		"""
		self.__window.show_dialog()
		return

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the PreferencesManager instance.
		@type self: A PreferencesManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		from Window import PreferencesWindow
		self.__window = PreferencesWindow(self, editor)  # (Done)
		from gtk import STOCK_CLOSE, Button
		self.__close_button = Button(stock=STOCK_CLOSE, use_underline=True) # (Done)
		self.__label = self.__create_labels()
		from FontButton import PreferencesFontButton
		self.__font_button = PreferencesFontButton(self, editor) # (Done)
		from TabSpinButton import TabSpinButton
		self.__tab_spin_button = TabSpinButton(self, editor) # (Done)
		from TabCheckButton import TabCheckButton
		self.__tab_check_button = TabCheckButton(self, editor) # (Done)
		from WrapCheckButton import TextWrapCheckButton
		self.__text_wrap_check_button = TextWrapCheckButton(self, editor) # (Done)
		from MarginCheckButton import MarginCheckButton
		self.__margin_check_button = MarginCheckButton(self, editor) # (Done)
		from SpellCheckButton import SpellCheckButton
		self.__spell_check_button = SpellCheckButton(self, editor) # (Done)
		from MarginSpinButton import MarginSpinButton
		self.__margin_spin_button = MarginSpinButton(self, editor)
		self.__signal_id_1 = self.__signal_id_2 = None
		return

	def __arrange_widgets(self):
		"""
		Arrange the widgets of the preferences dialog.

		@param self: Reference to the PreferenceDialog instance.
		@type self: A PreferenceDialog object.
		"""
		self.__window.main_area.set_spacing(10)
		from gtk import Alignment, HBox
		alignment = Alignment(xalign=0.0)
		alignment.add(self.__label[0])
		self.__window.main_area.pack_start(alignment, False, False, 0)

		hbox = HBox(homogeneous=False, spacing=10)
		alignment = Alignment(xalign=0.4, yalign=0.0, xscale=0.7, yscale=0.0)
		alignment.add(hbox)
		hbox.pack_start(self.__label[1], False, False, 0)
		hbox.pack_start(self.__font_button, True, True, 0)
		self.__label[1].set_mnemonic_widget(self.__font_button)
		self.__window.main_area.pack_start(alignment, False, False, 0)

		alignment = Alignment(xalign=0.0)
		alignment.add(self.__label[2])
		self.__window.main_area.pack_start(alignment, False, False, 0)

		hbox = HBox(homogeneous=False, spacing=10)
		alignment = Alignment(xalign=0.1, yalign=0.0, xscale=0.0, yscale=0.0)
		alignment.add(hbox)
		hbox.pack_start(self.__label[3], False, False, 0)
		hbox.pack_start(self.__tab_spin_button, False, False, 0)
		self.__label[3].set_mnemonic_widget(self.__tab_spin_button)
		self.__window.main_area.pack_start(alignment, False, False, 0)

		hbox = HBox(homogeneous=False, spacing=10)
		alignment = Alignment(xalign=0.12, yalign=0.0, xscale=0.0, yscale=0.0)
		alignment.add(hbox)
		hbox.pack_start(self.__tab_check_button, False, False, 0)
		self.__window.main_area.pack_start(alignment, False, False, 0)

		alignment = Alignment(xalign=0.0, yalign=0.0, xscale=0.0, yscale=0.0)
		alignment.add(self.__label[4])
		self.__window.main_area.pack_start(alignment, False, False, 0)

		hbox = HBox(homogeneous=False, spacing=10)
		alignment = Alignment(xalign=0.1, yalign=0.0, xscale=0.0, yscale=0.0)
		alignment.add(hbox)
		hbox.pack_start(self.__text_wrap_check_button, False, False, 0)
		self.__window.main_area.pack_start(alignment, False, False, 0)

		alignment = Alignment(xalign=0.0, yalign=0.0, xscale=0.0, yscale=0.0)
		alignment.add(self.__label[5])
		self.__window.main_area.pack_start(alignment, True, False, 0)

		hbox = HBox(homogeneous=False, spacing=10)
		alignment = Alignment(xalign=0.1, yalign=0.0, xscale=0.0, yscale=0.0)
		alignment.add(hbox)
		hbox.pack_start(self.__margin_check_button, False, False, 0)
		self.__window.main_area.pack_start(alignment, False, False, 0)

		hbox = HBox(homogeneous=False, spacing=10)
		alignment = Alignment(xalign=0.15, yalign=0.0, xscale=0.0, yscale=0.0)
		alignment.add(hbox)
		hbox.pack_start(self.__label[6], False, False, 0)
		hbox.pack_start(self.__margin_spin_button, False, False, 0)
		self.__label[6].set_mnemonic_widget(self.__margin_spin_button)
		self.__window.main_area.pack_start(alignment, False, False, 0)

		alignment = Alignment(xalign=0.0, yalign=0.0, xscale=0.0, yscale=0.0)
		alignment.add(self.__label[7])
		self.__window.main_area.pack_start(alignment, True, False, 0)

		hbox = HBox(homogeneous=False, spacing=10)
		alignment = Alignment(xalign=0.1, yalign=0.0, xscale=0.0, yscale=0.0)
		alignment.add(hbox)
		hbox.pack_start(self.__spell_check_button, False, False, 0)
		self.__window.main_area.pack_start(alignment, False, False, 0)

		self.__window.button_area.pack_start(self.__close_button, False, False, 0)
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

		@param self: Reference to the PreferencesManager instance.
		@type self: A PreferencesManager object.

		@param manager: Reference to the PreferencesManager instance.
		@type manager: A PreferencesManager object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self.__close_button)
		self.__editor.disconnect_signal(self.__signal_id_2, self)
		self.__label.clear()
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
		from i18n import msg0001, msg0002, msg0003
		from i18n import msg0004, msg0005, msg0006
		from i18n import msg0007, msg0008
		from collections import deque
		string_list = deque([msg0001, msg0001, msg0003, msg0004, msg0005, msg0006,
						msg0007, msg0008])
		labels = map(self.__convert_string_to_label, string_list)
		return deque(labels)

	def __convert_string_to_label(self, string):
		from gtk import Label
		label = Label(string)
		label.set_use_underline(True)
		label.set_use_markup(True)
		return label
