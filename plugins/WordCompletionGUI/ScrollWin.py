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
This module documents the the scrolled window object for the text editor's
completion window.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtk import ScrolledWindow

class CompletionScrollWin(ScrolledWindow):
	"""
	Scrolled window for the text editor's completion window.
	"""

	def __init__(self, manager):
		"""
		Initialize the scrolled window container object.

		@param self: Reference to the CompletionScrolledWindow instance.
		@type self: A CompletionScrolledWindow object.

		@param completion_view: The completion window's view.
		@type completion_view: A CompletionView object.
		"""
		ScrolledWindow.__init__(self)
		self.__init_attributes(manager)
		self.__set_properties()
		self.__signal_id_1 = manager.connect("destroy", self.__destroy_cb)
		self.__signal_id_2 = manager.connect("populated-model", self.__populated_model_cb)

	def __init_attributes(self, manager):
		"""
		Initialize the scrolled window container object.

		@param self: Reference to the CompletionScrolledWindow instance.
		@type self: A CompletionScrolledWindow object.

		@param completion_view: The completion window's view.
		@type completion_view: A CompletionView object.
		"""
		self.__manager = manager
		self.__signal_id_1 = self.__signal_id_2 = None
		return

	def __set_properties(self):
		"""
		Define the scrolled window's default properties.

		@param self: Reference to the CompletionScrolledWindow instance.
		@type self: A CompletionScrolledWindow object.
		"""
		from gtk import POLICY_NEVER, POLICY_ALWAYS
		self.set_policy(POLICY_NEVER, POLICY_NEVER)
		self.set_property("border-width", 2)
		return

	def __populated_model_cb(self, manager, view):
		"""
		Handles callback when the "populated-model" signal is emitted.

		This function determines what policy to use when showing the
		scrolled window depending on the size of the completion window's
		view.

		@param self: Reference to the CompletionScrolledWindow instance.
		@type self: A CompletionScrolledWindow object.

		@param view: The completion window's view.
		@type view: A CompletionView object.
		"""
		from gtk import POLICY_NEVER, POLICY_ALWAYS
		from operator import le, ge
		width, height = view.size_request()
		if le(width, 200) and le(height, 200):
			self.set_policy(POLICY_NEVER, POLICY_NEVER)
		elif ge(width, 200) and le(height, 200):
			self.set_policy(POLICY_NEVER, POLICY_NEVER)
		elif le(width, 200) and ge(height, 200):
			self.set_policy(POLICY_NEVER, POLICY_ALWAYS)
		else:
			self.set_policy(POLICY_NEVER, POLICY_ALWAYS)
		self.__manager.emit("show-window", view)
		return

	def __destroy_cb(self, manager):
		"""
		Destroy instance of this object.

		@param self: Reference to the CompletionTreeView instance.
		@type self: A CompletionTreeView object.

		@param manager: Reference to the CompletionManager instance.
		@type manager: A CompletionManager object.
		"""
		from SCRIBES.utils import delete_attributes, disconnect_signal
		disconnect_signal(self.__signal_id_1, manager)
		disconnect_signal(self.__signal_id_2, manager)
		self.destroy()
		delete_attributes(self)
		self = None
		del self
		return
