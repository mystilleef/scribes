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
This module exposes a class that creates the text editor's fullscreen button.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import Button, STOCK_LEAVE_FULLSCREEN

class ScribesFullscreenButton(Button):
	"""
	This class creates the fullscreen button for the text editor. The fullscreen
	button exits fullscreen mode when it is clicked.
	"""

	def __init__(self, editor):
		"""
		Initialize the fullscreen button.

		@param self: Reference to the ScribesFullscreenButton instance.
		@type self: A ScribesFullscreenButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		Button.__init__(self, stock=STOCK_LEAVE_FULLSCREEN, use_underline=True)
		self.connect("clicked", self.__fsbutton_clicked_cb, editor)

	def __fsbutton_clicked_cb(self, button, editor):
		"""
		Handles callback when the "clicked" signal is emitted.

		This function exits the text editor's fullscreen mode.

		@param self: Reference to the ScribesFullscreenButton instance.
		@type self: A ScribesFullscreenButton object.

		@param button: A button used to exit fullscreen mode.
		@type button: A gtk.Button object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		editor.trigger("toggle_fullscreen")
		return True
