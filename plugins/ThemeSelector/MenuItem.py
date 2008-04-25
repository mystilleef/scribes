# -*- coding: utf-8 -*-
# Copyright © 2006 Lateef Alabi-Oki
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
This module documents a class that adds/removes a menuitem that shows
the color editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2006 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class MenuItem_(object):
	"""
	This class creates an object that adds or removes a menuitem that
	shows the color editor.
	"""

	def __init__(self, editor):
		"""
		Initialize the object.

		@param self: Reference to the MenuItem_ instance.
		@type self: An MenuItem_ object.

		@param trigger: Reference to the ColorEditorTrigger instance.
		@type trigger: An ColorEditorTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(editor)
		self.__add_menuitem()
		self.__sigid1 = self.__menuitem.connect("activate", self.__menuitem_activate_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the object.

		@param self: Reference to the MenuItem_ instance.
		@type self: An MenuItem_ object.

		@param trigger: Reference to the ColorEditorTrigger instance.
		@type trigger: An ColorEditorTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__sigid1 = None
		from gtk import STOCK_SELECT_COLOR
		from i18n import msg1
		self.__menuitem = editor.create_menuitem(msg1, STOCK_SELECT_COLOR)
		return

	def __add_menuitem(self):
		"""
		Add menuitem to the editor's preference menu.

		@param self: Reference to the MenuItem_ instance.
		@type self: An MenuItem_ object.
		"""
		self.__editor.preference_menu.append(self.__menuitem)
		self.__editor.preference_menu.show_all()
		return

	def destroy(self):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the MenuItem_ instance.
		@type self: An MenuItem_ object.

		@param trigger: Reference to the ColorEditorTrigger instance.
		@type trigger: An ColorEditorTrigger object.
		"""
		self.__editor.disconnect_signal(self.__sigid1, self.__menuitem)
		self.__editor.preference_menu.remove(self.__menuitem)
		self.__menuitem.destroy()
		del self
		self = None
		return

	def __menuitem_activate_cb(self, menuitem):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the MenuItem_ instance.
		@type self: An MenuItem_ object.

		@param menuitem: Reference the the automatic replacement menuitem.
		@type menuitem: A gtk.MenuItem object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		self.__editor.trigger("show_theme_selector")
		return False
