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

class ReplaceStopButton(Button):
	"""
	This class creates the stop button for the text editor's replacebar.
	It defines the behavior and default properties of the button.
	"""

	def __init__(self, replacebar):
		"""
		Initialize the button.

		@param self: Reference to the ScribesReplaceStopButton instance.
		@type self: A ScribesReplaceStopButton object.

		@param findbar: The text editor's findbar.
		@type findbar: A ScribesFindBar object.
		"""
		from gtk import STOCK_STOP
		Button.__init__(self, stock=STOCK_STOP, use_underline=True)
		self.__init_attributes(replacebar)
		self.__signal_id_1 = self.connect("clicked", self.__stopbutton_clicked_cb)
		self.__signal_id_2 = replacebar.connect("delete", self.__destroy_cb)

	def __init_attributes(self, replacebar):
		"""
		Initialize the button's attributes.

		@param self: Reference to the ScribesReplaceStopButton instance.
		@type self: A ScribesReplaceStopButton object.

		@param findbar: The text editor's findbar.
		@type findbar: A ScribesFindBar object.
		"""
		self.__replacemanager = replacebar.search_replace_manager
		return

	def __stopbutton_clicked_cb(self, button):
		"""
		Handles callback when the button's "clicked" signal is emitted.

		@param self: Reference to the ScribesReplaceStopButton instance.
		@type self: A ScribesReplaceStopButton object.

		@param button: The ScribesReplaceStopButton.
		@type button: A ScribesReplaceStopButton object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		self.__replacemanager.cancel()
		return True

	def __destroy_cb(self, replacebar):
		from SCRIBES.utils import disconnect_signal, delete_attributes
		disconnect_signal(self.__signal_id_1, self)
		disconnect_signal(self.__signal_id_2, replacebar)
		self.destroy()
		delete_attributes(self)
		del self
		self = None
		return
