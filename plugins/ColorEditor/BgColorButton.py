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
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
# USA

"""
This module documents a class that creates the foreground color button
for the text editor's color editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import ColorButton

class BackgroundButton(ColorButton):
	"""
	This class creates a color button for the text editor's color
	editor. The color button allows users to set the foreground color of
	text editor's buffer.
	"""

	def __init__(self, manager, editor):
		"""
		Initialize the button.

		@param self: Reference to the BackgroundButton instance.
		@type self: A BackgroundButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		ColorButton.__init__(self)
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__client.notify_add("/apps/scribes/bgcolor", self.__bgcolor_cb)
		self.__client.notify_add("/apps/scribes/use_theme_colors", self.__use_theme_colors_cb)
		self.__signal_id_1 = self.__manager.connect("destroy", self.__destroy_cb)
		self.__signal_id_2 = self.connect("color-set", self.__color_set_cb)

	def __init_attributes(self, manager, editor):
		"""
		Initialize the button's data attributes.

		@param self: Reference to the BackgroundButton instance.
		@type self: A BackgroundButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__client = editor.gconf_client 
		self.__manager = manager
		self.__signal_id_1 = self.__signal_id_2 = None
		return

	def __set_properties(self):
		"""
		Define the default behavior of the button.

		@param self: Reference to the BackgroundButton instance.
		@type self: A BackgroundButton object.
		"""
		bgcolor = "#ffffff"
		value = self.__client.get("/apps/scribes/bgcolor")
		from operator import truth
		if truth(value):
			bgcolor = self.__client.get_string("/apps/scribes/bgcolor")
		from gtk.gdk import color_parse
		bgcolor = color_parse(bgcolor)
		self.set_color(bgcolor)
		from i18n import msg0011
		self.set_title(msg0011)
		from SCRIBES.tooltips import background_button_tip
		self.__editor.tip.set_tip(self, background_button_tip)
		use_theme_colors = True
		value = self.__client.get("/apps/scribes/use_theme_colors")
		if truth(value):
			use_theme_colors = self.__client.get_bool("/apps/scribes/use_theme_colors")
		self.set_property("sensitive", not use_theme_colors)
		return

	def __bgcolor_cb(self, client, cnxn_id, entry, data):
		"""
		Handles callback when foreground color changes.

		@param self: Reference to the BackgroundButton instance.
		@type self: A BackgroundButton object.
		"""
		self.handler_block(self.__signal_id_2)
		bgcolor = client.get_string("/apps/scribes/bgcolor")
		color = self.get_color()
		from SCRIBES.utils import convert_color_to_spec
		color = convert_color_to_spec(color)
		from operator import ne
		if ne(bgcolor, color):
			from gtk.gdk import color_parse
			self.set_color(color_parse(bgcolor))
		self.handler_unblock(self.__signal_id_2)
		return

	def __color_set_cb(self, button):
		"""
		Handles callback when the "toggled" signal is emitted.

		@param self: Reference to the BackgroundButton instance.
		@type self: A BackgroundButton object.

		@param button: Reference to the BackgroundButton.
		@type button: A BackgroundButton object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		bgcolor = self.get_color()
		from SCRIBES.utils import convert_color_to_spec
		bgcolor = convert_color_to_spec(bgcolor)
		self.__client.set_string("/apps/scribes/bgcolor", bgcolor)
		self.__client.notify("/apps/scribes/bgcolor")
		return True

	def __use_theme_colors_cb(self, client, cnxn_id, entry, data):
		"""
		Handles callback when foreground color changes.

		@param self: Reference to the BackgroundButton instance.
		@type self: A BackgroundButton object.
		"""
		use_theme_colors = True
		value = self.__client.get("/apps/scribes/use_theme_colors")
		from operator import truth, not_
		if truth(value):
			use_theme_colors = self.__client.get_bool("/apps/scribes/use_theme_colors")
		if truth(use_theme_colors):
			if truth(self.get_property("sensitive")):
				self.set_property("sensitive", False)
		else:
			if not_(self.get_property("sensitive")):
				self.set_property("sensitive", True)
		return

	def __destroy_cb(self, manager):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the BackgroundButton instance.
		@type self: A BackgroundButton object.

		@param manager: Reference to the ColorEditorManager instance.
		@type manager: A ColorEditorManager object.
		"""
		from SCRIBES.utils import disconnect_signal, delete_attributes
		disconnect_signal(self.__signal_id_1, self.__manager)
		disconnect_signal(self.__signal_id_2, self)
		self.destroy()
		delete_attributes(self)
		del self
		self = None
		return
