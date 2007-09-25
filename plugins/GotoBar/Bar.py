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
The modules exposes a class responsible for creating the gotobar. The gotobar
allows users to move the cursor to a specific line.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from SCRIBES.bar import ScribesBar
from gobject import SIGNAL_RUN_LAST, TYPE_NONE

class GotoBar(ScribesBar):
	"""
	This class creates a gotobar object. The gotobar allows users to move the
	cursor to a specific line in the document contained by the text editor.
	"""

	__gsignals__ = {
		"delete": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize the gotobar object.

		@param self: Reference to the GotoBar instance.
		@type self: A GotoBar object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		ScribesBar.__init__(self, editor)
		self.__init_attributes(editor)
		self.__set_properties()
		self.__arrange_widgets()
		self.__signal_id_1 = self.__editor.connect("show-bar", self.__show_bar_cb)
		self.__signal_id_2 = self.__editor.connect("hide-bar", self.__hide_bar_cb)
		self.__signal_id_3 = self.connect("delete", self.__destroy_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the gotobar's attributes.

		@param self: Reference to the GotoBar instance.
		@type self: A GotoBar object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__status_id = None
		self.__bar_is_visible = False
		self.__label = self.__create_labels()
		from SpinButton import GotoSpinButton
		self.__spinbutton = GotoSpinButton(self.__editor)
		self.__signal_id_1 = self.__signal_id_2 = None
		self.__signal_id_3 = None
		return

	def __set_properties(self):
		"""
		Define the bar's properties.

		@param self: Reference to the GotoBar instance.
		@type self: A GotoBar object.
		"""
		self.resize(rows=1, columns=3)
		self.set_property("name", "GotoBar")
		return

	def __arrange_widgets(self):
		"""
		Arrange the gotobar widgets.

		@param self: Reference to the GotoBar instance.
		@type self: A GotoBar object.
		"""
		from gtk import SHRINK, FILL, EXPAND
		self.attach(child=self.__label[0],
					left_attach=0,
					right_attach=1,
					top_attach=0,
					bottom_attach=1,
					xoptions=SHRINK|FILL,
					yoptions=EXPAND,
					xpadding=7,
					ypadding=0)

		self.attach(child=self.__spinbutton,
					left_attach=1,
					right_attach=2,
					top_attach=0,
					bottom_attach=1,
					xoptions=SHRINK|FILL,
					yoptions=EXPAND,
					xpadding=0,
					ypadding=0)

		self.attach(child=self.__label[1],
					left_attach=2,
					right_attach=3,
					top_attach=0,
					bottom_attach=1,
					xoptions=SHRINK|FILL,
					yoptions=EXPAND,
					xpadding=0,
					ypadding=0)
		return

	def show_bar(self):
		"""
		Show the gotobar.

		@param self: Reference to the GotoBar instance.
		@type self: A GotoBar object.
		"""
		if self.__bar_is_visible:
			return
		ScribesBar.show_bar(self)
		self.__bar_is_visible = True
		from i18n import msg0001
		self.__status_id = self.__editor.feedback.set_modal_message(msg0001, "goto")
		return

	def hide_bar(self):
		"""
		Hide the gotobar.

		@param self: Reference to the GotoBar instance.
		@type self: A GotoBar object.
		"""
		if self.__bar_is_visible is False:
			return
		ScribesBar.hide_bar(self)
		self.__bar_is_visible = False
		self.__editor.feedback.unset_modal_message(self.__status_id, False)
		from i18n import msg0002
		self.__editor.feedback.update_status_message(msg0002, "info", 3)
		return

	def __create_labels(self):
		"""
		Create labels for the gotobar widget.

		@param self: Reference to the GotoBar instance.
		@type self: A GotoBar object.

		@return: A list of labels for the gotobar.
		@rtype: A List object.
		"""
		from i18n import msg0003, msg0004
		strings = [msg0004, msg0003]
		labels = []
		from gtk import Label
		for string in strings:
			label = Label(string)
			label.set_use_underline(True)
			label.set_use_markup(True)
			labels.append(label)
		return labels

	def __show_bar_cb(self, editor, bar):
		"""
		Handles callback when the "show-bar" signal is emitted.

		@param self: Reference to the GotoBar instance.
		@type self: A GotoBar object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param gotobar: The text editor's gotobar.
		@type gotobar: A GotoBar object.
		"""
		self.__bar_is_visible = True
		from i18n import msg0003
		message = msg0003 % self.__editor.textbuffer.get_line_count()
		self.__label[1].set_label(message)
		return

	def __hide_bar_cb(self, editor, bar):
		"""
		Handles callback when the "hide-bar" signal is emitted.

		@param self: Reference to the GotoBar instance.
		@type self: A GotoBar object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param gotobar: The text editor's gotobar.
		@type gotobar: A GotoBar object.
		"""
		self.__bar_is_visible = False
		return

	def __destroy_cb(self, bar):
		"""
		Handles callback when the "delete" signal is emitted.

		@param self: Reference to the GotoBar instance.
		@type self: A GotoBar object.

		@param bar: Reference to the GotoBar instance.
		@type bar: A GotoBar object.
		"""
		from SCRIBES.utils import disconnect_signal, delete_attributes
		from SCRIBES.utils import delete_list
		disconnect_signal(self.__signal_id_1, self.__editor)
		disconnect_signal(self.__signal_id_2, self.__editor)
		disconnect_signal(self.__signal_id_3, self)
		delete_list(self.__label)
		if self.__spinbutton:
			self.__spinbutton.emit("delete")
		self.destroy()
		delete_attributes(self)
		del self
		self = None
		return
