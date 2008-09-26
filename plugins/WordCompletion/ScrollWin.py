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
		ScrolledWindow.__init__(self)
		self.__init_attributes(manager)
		self.__set_properties()
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("populated-model", self.__populated_model_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		return

	def __set_properties(self):
		from gtk import POLICY_NEVER, POLICY_ALWAYS
		self.set_policy(POLICY_NEVER, POLICY_NEVER)
		return

	def __populated_model_cb(self, manager, view):
		from gtk import POLICY_NEVER, POLICY_ALWAYS
		width, height = view.size_request()
		if width < 200 and height < 200:
			self.set_policy(POLICY_NEVER, POLICY_NEVER)
		elif (width > 200) and (height < 200):
			self.set_policy(POLICY_NEVER, POLICY_NEVER)
		elif (width < 200) and (height > 200):
			self.set_policy(POLICY_NEVER, POLICY_ALWAYS)
		else:
			self.set_policy(POLICY_NEVER, POLICY_ALWAYS)
		self.__manager.emit("show-window", view)
		return

	def __destroy_cb(self, manager):
		from SCRIBES.Utils import disconnect_signal
		disconnect_signal(self.__sigid1, manager)
		disconnect_signal(self.__sigid2, manager)
		self.destroy()
		del self
		self = None
		return
