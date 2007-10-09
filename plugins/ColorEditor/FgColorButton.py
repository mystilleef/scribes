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

class ForegroundButton(ColorButton):
	"""
	This class creates a color button for the text editor's color
	editor. The color button allows users to set the foreground color of
	text editor's buffer.
	"""

	def __init__(self, manager, editor):
		"""
		Initialize the button.

		@param self: Reference to the ForegroundButton instance.
		@type self: A ForegroundButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		ColorButton.__init__(self)
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__client.notify_add("/apps/scribes/fgcolor", self.__fgcolor_cb)
		self.__client.notify_add("/apps/scribes/use_theme_colors", self.__use_theme_colors_cb)
		self.__signal_id_1 = self.__manager.connect("destroy", self.__destroy_cb)
		self.__signal_id_2 = self.connect("color-set", self.__color_set_cb)

	def __init_attributes(self, manager, editor):
		"""
		Initialize the button's data attributes.

		@param self: Reference to the ForegroundButton instance.
		@type self: A ForegroundButton object.

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

		@param self: Reference to the ForegroundButton instance.
		@type self: A ForegroundButton object.
		"""
		fgcolor = "#000000"
		value = self.__client.get("/apps/scribes/fgcolor")
		from operator import truth
		if truth(value):
			fgcolor = self.__client.get_string("/apps/scribes/fgcolor")
		from gtk.gdk import color_parse
		fgcolor = color_parse(fgcolor)
		self.set_color(fgcolor)
		from i18n import msg0006
		self.set_title(msg0006)
		from SCRIBES.tooltips import foreground_button_tip
		self.__editor.tip.set_tip(self, foreground_button_tip)
		use_theme_colors = True
		value = self.__client.get("/apps/scribes/use_theme_colors")
		if truth(value):
			use_theme_colors = self.__client.get_bool("/apps/scribes/use_theme_colors")
		self.set_property("sensitive", not use_theme_colors)
		return

	def __fgcolor_cb(self, client, cnxn_id, entry, data):
		"""
		Handles callback when foreground color changes.

		@param self: Reference to the ForegroundButton instance.
		@type self: A ForegroundButton object.
		"""
		self.handler_block(self.__signal_id_2)
		fgcolor = client.get_string("/apps/scribes/fgcolor")
		color = self.get_color()
		color = self.__editor.convert_color_to_string(color)
		from operator import ne
		if ne(fgcolor, color):
			from gtk.gdk import color_parse
			self.set_color(color_parse(fgcolor))
		self.handler_unblock(self.__signal_id_2)
		return

	def __color_set_cb(self, button):
		"""
		Handles callback when the "toggled" signal is emitted.

		@param self: Reference to the ForegroundButton instance.
		@type self: A ForegroundButton object.

		@param button: Reference to the ForegroundButton.
		@type button: A ForegroundButton object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		fgcolor = self.get_color()
		fgcolor = self.__editor.convert_color_to_string(fgcolor)
		self.__client.set_string("/apps/scribes/fgcolor", fgcolor)
		self.__client.notify("/apps/scribes/fgcolor")
		return True

	def __use_theme_colors_cb(self, client, cnxn_id, entry, data):
		"""
		Handles callback when foreground color changes.

		@param self: Reference to the ForegroundButton instance.
		@type self: A ForegroundButton object.
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

		@param self: Reference to the ForegroundButton instance.
		@type self: A ForegroundButton object.

		@param manager: Reference to the ColorEditorManager instance.
		@type manager: A ColorEditorManager object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self.__manager)
		self.__editor.disconnect_signal(self.__signal_id_2, self)
		self.destroy()
		del self
		self = None
		return
