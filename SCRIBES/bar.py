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
This modules exposes a class that creates the text editor's bar object.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import Table

class ScribesBar(Table):
	"""
	This class creates the text editor's bar object. The bar object is a
	container that appears above the above the statusbar area. This class
	defines the behavior of the bar object which can be used to house other
	widgets.
	"""

	def __init__(self, editor):
		"""
		Initialize the bar object.

		@param self: Reference to the ScribesBar instance.
		@type self: A ScribesBar object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		Table.__init__(self)
		self.__init_attributes(editor)
		#self.__set_properties()
		self.connect("key-press-event", self.__key_press_event_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the bar object's attributes.

		@param self: Reference to the ScribesBar instance.
		@type self: A ScribesBar object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.editor = editor
		return

	def __set_properties(self):
		"""
		Define the property of the bar object.

		@param self: Reference to the ScribesBar instance.
		@type self: A ScribesBar object.
		"""
		self.set_property("receives-default", True)
		return

	def show_bar(self):
		"""
		Show the bar object.

		@param self: Reference to the ScribesBar instance.
		@type self: A ScribesBar object.
		"""
		self.editor.emit("show-bar", self)
		return

	def hide_bar(self):
		"""
		Hide the bar object.

		@param self: Reference to the ScribesBar instance.
		@type self: A ScribesBar object.
		"""
		self.editor.emit("hide-bar", self)
		return

	def __key_press_event_cb(self, table, event):
		from gtk import keysyms
		from gtk.gdk import SHIFT_MASK
		from operator import eq
		# Disable tabbing.
		if eq(event.keyval, keysyms.Tab): return True
		# Disable shift tabbing.
		if eq(event.keyval, keysyms.ISO_Left_Tab): return True
		return False
