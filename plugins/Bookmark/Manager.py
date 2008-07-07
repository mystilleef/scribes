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
This module documents a class that performs bookmark operations for the
text editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_PYOBJECT

class Manager(GObject):

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"toggle-bookmark": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"remove-all-bookmarks": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"marked-lines": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		from MarginDisplayer import Displayer
		Displayer(self, editor)
		from DatabaseUpdater import Updater
		Updater(self, editor)
		from BufferMonitor import Monitor
		Monitor(self, editor)
		from BufferMarker import Marker
		Marker(self, editor)

	def destroy(self):
		self.emit("destroy")
		del self
		self = None
		return

	def toggle_bookmark(self):
		self.emit("toggle-bookmark")
		return False

	def remove_bookmarks(self):
		self.emit("remove-all-bookmarks")
		return False
