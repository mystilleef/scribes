# -*- coding: utf-8 -*-
# Copyright © 2007 Lateef Alabi-Oki
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
This module documents a class that creates the throbber for the text
editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import ToolItem

class Spinner(ToolItem):
	"""
	This class creates the throbber object for the text editor.
	"""

	def __init__(self, editor):
		"""
		Initialize the object.

		@param self: Reference to the Spinner instance.
		@type self: A Spinner object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		ToolItem.__init__(self)
		self.__init_attributes(editor)
		self.__set_properties()

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the Spinner instance.
		@type self: A Spinner object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__store_id = editor.store.add_object("Spinner", self)
		from utils import create_image, find_file
		from gtk.gdk import PixbufAnimation
		self.__animation = PixbufAnimation(find_file("throbber-active.gif"))
		self.__image = create_image("throbber-inactive.png")
		self.__pixbuf = self.__image.get_pixbuf()
		self.__call_count = 0
		self.__is_spinning = False
		return

########################################################################
#
#						Public APIs
#
########################################################################

	def start(self):
		"""
		Start the throbber.

		@param self: Reference to the Spinner instance.
		@type self: A Spinner object.
		"""
		self.__call_count += 1
		if self.__is_spinning: return
		self.__is_spinning = True
		self.__image.clear()
		self.__image.set_from_animation(self.__animation)
		self.__editor.response()
		return

	def stop(self):
		"""
		Stop the throbber.

		@param self: Reference to the Spinner instance.
		@type self: A Spinner object.
		"""
		if self.__is_spinning is False: return
		self.__call_count -= 1
		if self.__call_count: return
		self.__is_spinning = False
		self.__call_count = 0
		self.__image.clear()
		self.__image.set_from_pixbuf(self.__pixbuf)
		self.__editor.response()
		return

	def destroy_object(self):
		self.__destroy()
		return

########################################################################
#
#						Helper Methods
#
########################################################################

	def __set_properties(self):
		"""
		Set object properties.

		@param self: Reference to the Spinner instance.
		@type self: A Spinner object.
		"""
		self.add(self.__image)
		return

	def __destroy(self):
		"""
		Destroy instance of this class.

		@param self: Reference to the Spinner instance.
		@type self: A Spinner object.
		"""
		# Disconnect signals.
		self.destroy()
		self.__editor.store.remove_object("Spinner", self.__store_id)
		# Delete data attributes.
		del self
		self = None
		return
