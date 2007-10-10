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

from gtk import Button

class FindStopButton(Button):
	"""
	This class creates the stop button for the text editor's findbar. It defines
	the behavior and default properties of the button.
	"""

	def __init__(self, findbar):
		"""
		Initialize the button.

		@param self: Reference to the ScribesFindStopButton instance.
		@type self: A ScribesFindStopButton object.

		@param findbar: The text editor's findbar.
		@type findbar: A ScribesFindBar object.
		"""
		from gtk import STOCK_STOP
		Button.__init__(self, stock=STOCK_STOP, use_underline=True)
		self.__init_attributes(findbar)
		self.__signal_id_1 = self.connect("clicked", self.__stopbutton_clicked_cb)
		self.__signal_id_2 = findbar.connect("delete", self.__destroy_cb)

	def __init_attributes(self, findbar):
		"""
		Initialize the button's attributes.

		@param self: Reference to the ScribesFindStopButton instance.
		@type self: A ScribesFindStopButton object.

		@param findbar: The text editor's findbar.
		@type findbar: A ScribesFindBar object.
		"""
		self.__editor = findbar.editor
		self.__searchmanager = findbar.search_replace_manager
		self.__signal_id_1 = self.__signal_id_2 = None
		return

	def __stopbutton_clicked_cb(self, button):
		"""
		Handles callback when the button's "clicked" signal is emitted.

		@param self: Reference to the ScribesFindStopButton instance.
		@type self: A ScribesFindStopButton object.

		@param button: The ScribesFindStopButton.
		@type button: A ScribesFindStopButton object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		self.__searchmanager.cancel()
		return True

	def __destroy_cb(self, findbar):
		"""
		Handles callback when the button's "destroy" signal is emitted

		@param self: Reference to the FindStopButton instance.
		@type self: A FindStopButton object.

		@param findbar: Reference to the FindBar instance.
		@type findbar: A FindBar object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self)
		self.__editor.disconnect_signal(self.__signal_id_2, findbar)
		self.destroy()
		del self
		self = None
		return
