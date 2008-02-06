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
This module documents a class that defines the behavior of the bracket
selection color button.

@author: Lateef Alabi-Oki
@organization: Scribes
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

class ColorButton(object):
	"""
	This class defines the behavior of the bracket selection color
	button.
	"""

	def __init__(self, editor, manager):
		"""
		Initialize object.

		@param self: Reference to the ColorButton instance.
		@type self: A ColorButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param manager: Object that manages GUI components
		@type manager: A Manager object.
		"""
		self.__init_attributes(editor, manager)
		self.__set_properties()
		self.__sig_id1 = self.__button.connect("color-set", self.__color_set_cb)
		self.__sig_id2 = manager.connect("destroy", self.__destroy_cb)
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monitor_id_1 = monitor_add(self.__database_uri, MONITOR_FILE, self.__database_changed_cb)
		self.__button.set_property("sensitive", True)

	def __init_attributes(self, editor, manager):
		"""
		Initialize data attributes.

		@param self: Reference to the ColorButton instance.
		@type self: A ColorButton object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param manager: Object that manages GUI components
		@type manager: A Manager object.
		"""
		self.__editor = editor
		self.__manager = manager
		self.__button = manager.glade.get_widget("BracketSelectionColorButton")
		from os.path import join
		preference_folder = join(editor.metadata_folder, "PluginPreferences")
		database_path = join(preference_folder, "LexicalScopeHighlight.gdb")
		from gnomevfs import get_uri_from_local_path
		self.__database_uri = get_uri_from_local_path(database_path)
		self.__sig_id1 = self.__sig_id2 = self.__monitor_id_1 = None
		return

	def __set_properties(self):
		"""
		Set default properties for color button.

		@param self: Reference to the ColorButton instance.
		@type self: A ColorButton object.
		"""
		from LexicalScopeHighlightMetadata import get_value
		from gtk.gdk import color_parse
		color = color_parse(get_value())
		self.__button.set_color(color)
		return

	def __destroy(self):
		"""
		Destroy object.

		@param self: Reference to the ColorButton instance.
		@type self: A ColorButton object.
		"""
		from gnomevfs import monitor_cancel
		if self.__monitor_id_1: monitor_cancel(self.__monitor_id_1)
		self.__editor.disconnect_signal(self.__sig_id1, self.__button)
		self.__editor.disconnect_signal(self.__sig_id2, self.__manager)
		self.__button.destroy()
		del self
		self = None
		return

	def __color_set_cb(self, *args):
		"""
		Handles callback when the "color-set" signal is emitted.

		@param self: Reference to the ColorButton instance.
		@type self: A ColorButton object.
		"""
		from LexicalScopeHighlightMetadata import set_value
		color = self.__button.get_color().to_string()
		set_value(color)
		return True

	def __destroy_cb(self, *args):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the ColorButton instance.
		@type self: A ColorButton object.
		"""
		self.__destroy()
		return True

	def __database_changed_cb(self, *args):
		"""
		Handles callback when database changes.

		@param self: Reference to the ColorButton instance.
		@type self: A ColorButton object.
		"""
		self.__button.handler_block(self.__sig_id1)
		from LexicalScopeHighlightMetadata import get_value
		from gtk.gdk import color_parse
		color = color_parse(get_value())
		self.__button.set_color(color)
		self.__button.handler_unblock(self.__sig_id1)
		return True
