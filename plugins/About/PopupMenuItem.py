# -*- coding: utf-8 -*-
# Copyright © 2008 Lateef Alabi-Oki
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
This modules documents a class that implements the about dialog popup
menu item.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

from gtk import ImageMenuItem

class PopupMenuItem(ImageMenuItem):
	"""
	This class creates the about popup menu item for the text editor.
	"""

	def __init__(self, editor):
		"""
		Initialize the popup menu item.

		@param self: Reference to the ScribesAboutMenuItem instance.
		@type self: A ScribesAboutMenuItem object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		from gtk import STOCK_ABOUT
		ImageMenuItem.__init__(self, STOCK_ABOUT)
		self.__init_attributes(editor)
		self.__signal_id_1 = self.connect("activate", self.__popup_activate_cb)
		self.__signal_id_2 = self.__editor.textview.connect("focus-in-event", self.__focus_in_event_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the popup menu item's attributes.

		@param self: Reference to the PopupMenuItem instance.
		@type self: A PopupMenuItem object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__signal_id_1 = None
		self.__signal_id_2 = None
		return

	def __popup_activate_cb(self, *args):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the PopupMenuItem instance.
		@type self: A PopupMenuItem object.
		"""
		self.__editor.trigger("show_about_dialog")
		return True

	def __focus_in_event_cb(self, *args):
		"""
		Handles callback when the "focus-in-event" signal is emitted.

		@param self: Reference to the PopupMenuItem instance.
		@type self: An PopupMenuItem object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__editor.textview)
		self.destroy()
		del self
		self = None
		from gc import collect
		collect()
		return False
