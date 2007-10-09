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
This module documents a class that switches Scribes' windows containing
documents.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2006 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE

class DocumentSwitcher(GObject):
	"""
	This class creates an object that switches windows.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def switch_window(self):
		uris = self.__editor.instance_manager.get_uris()
		from operator import not_
		if not_(uris):
			message = "No document found"
			self.__editor.feedback.update_status_message(message, "warning")
			return
		uri = self.__get_uri_to_focus(uris)
		self.__editor.instance_manager.focus_file(uri)
		return

	def __init__(self, editor):
		"""
		Initialize object.

		@param self: Reference to the DocumentSwitcher instance.
		@type self: A DocumentSwitcher object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		self.__signal_id_1 = self.connect("destroy", self.__switcher_destroy_cb)

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the DocumentSwitcher instance.
		@type self: A DocumentSwitcher object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__signal_id_1 = None
		return

	def __get_uri_to_focus(self, uris):
		try:
			uris.sort()
			if self.__editor.uri is None:
				raise ValueError
			index = uris.index(str(self.__editor.uri))
			uri = uris[index+1]
		except ValueError:
			return uris[0]
		except IndexError:
			return uris[0]
		return uri

	def __switcher_destroy_cb(self, switcher):
		self.__editor.disconnect_signal(self.__signal_id_1, self)
		del self
		self = None
		return
