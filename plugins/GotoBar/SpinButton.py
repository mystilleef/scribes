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
This module exposes a class responsible for creating the gotobar's spinbutton
object.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import SpinButton
from gobject import SIGNAL_RUN_LAST, TYPE_NONE

class GotoSpinButton(SpinButton):
	"""
	This class creates an object that allows users to jump to a specific line in
	the text editor's buffer. The object is gtk.SpinButton. This class defines
	the behavior and property of the gotobar's spinbutton object.
	"""

	__gsignals__ = {
		"delete": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize the gotobar's spinbutton.

		@param self: Reference to the GotoSpinButton instance.
		@type self: A GotoSpinButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		SpinButton.__init__(self)
		self.__init_attributes(editor)
		self.__set_properties()
		self.__signal_id_1 = self.__editor.connect("show-bar", self.__show_bar_cb)
		self.__signal_id_2 = self.connect("value-changed", self.__value_changed_cb)
		self.__signal_id_3 = self.connect("delete", self.__destroy_cb)
		self.__signal_id_5 = self.__editor.connect("hide-bar", self.__hide_bar_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the spinbutton's attributes

		@param self: Reference to the GotoSpinButton instance.
		@type self: A GotoSpinButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		from gtk import Adjustment
		self.__adjustment = Adjustment()
		self.__signal_id_1 = self.__signal_id_2 = None
		self.__signal_id_3 = self.__signal_id_4 = None
		self.__signal_id_5 = None
		return

	def __set_properties(self):
		"""
		Define the default properties of the spinbutton.

		@param self: Reference to the GotoSpinButton instance.
		@type self: A GotoSpinButton object.
		"""
		from gtk import UPDATE_IF_VALID
		self.set_update_policy(UPDATE_IF_VALID)
		self.set_numeric(True)
		self.set_wrap(False)
		self.set_snap_to_ticks(True)
		self.set_digits(0)
		self.set_property("xalign", 1)
		self.set_adjustment(self.__adjustment)
		return

	def __show_bar_cb(self, editor, bar):
		"""
		Handles callback when the "show-bar" signal is emitted.

		@param self: Reference to the GotoSpinButton instance.
		@type self: A GotoSpinButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param bar: The gotospinbutton.
		@type bar: A GotoSpinButton object.
		"""
		if bar.get_property("name") != "GotoBar": return
		self.__signal_id_4 = self.connect("key-press-event", self.__key_press_event_cb, bar)
		cursor_line = self.__editor.get_cursor_line()
		value = cursor_line + 1
		lower = 1
		upper =  self.__editor.textbuffer.get_line_count()
		step_increment = 1
		page_increment = 5
		page_size = 11
		self.__adjustment.set_all(value, lower, upper, step_increment,
								page_increment, page_size)
		self.__editor.move_view_to_cursor()
		self.grab_focus()
		return

	def __hide_bar_cb(self, editor, bar):
		"""
		Handles callback when the "hide-bar" signal is emitted.

		@param self: Reference to the GotoSpinButton instance.
		@type self: A GotoSpinButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param bar: Reference to the GotoBar.
		@type bar: A GotoBar object.
		"""
		if bar.get_property("name") != "GotoBar": return
		self.__editor.disconnect_signal(self.__signal_id_4, self)
		return

	def __value_changed_cb(self, spinbutton):
		"""
		Handles callback when the "value-changed" signal is emitted.

		@param self: Reference to the GotoSpinButton instance.
		@type self: A GotoSpinButton object.

		@param spinbutton: The gotobar's spinbutton.
		@type spinbutton: A GotoSpinButton object.
		"""
		line = spinbutton.get_value() - 1
		iterator = self.__editor.textbuffer.get_iter_at_line(int(line))
		self.__editor.textbuffer.place_cursor(iterator)
		self.__editor.move_view_to_cursor()
		from i18n import msg0005
		message = msg0005 % (line + 1)
		self.__editor.feedback.update_status_message(message, "succeed")
		return True

	def __key_press_event_cb(self, spinbutton, event, bar):
		"""
		Handles callback when the "key-press-event" signal is emitted.

		@param self: Reference to the GotoSpinButton instance.
		@type self: A GotoSpinButton object.

		@param spinbutton: The text editor's spinbutton.
		@type spinbutton: A GotoSpinButton object.

		@param event: An event that occurs when keys are pressed.
		@type event: A gtk.Event object.

		@param bar: The gotobar for the text editor.
		@type bar: A ScribesGotoBar object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		from gtk import keysyms
		if event.keyval == keysyms.Return:
			bar.hide_bar()
			return True
		return False

	def __destroy_cb(self, spinbutton):
		"""
		Handles callback when the "delete" signal is emitted.

		@param self: Reference to the SpinButton instance.
		@type self: A SpinButton object.

		@param spinbutton: Reference to the SpinButton instance.
		@type spinbutton: A SpinButton object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_2, self)
		self.__editor.disconnect_signal(self.__signal_id_3, self)
		self.__editor.disconnect_signal(self.__signal_id_4, self)
		self.__editor.disconnect_signal(self.__signal_id_5, self.__editor)
		self.destroy()
		del self
		self = None
		return
