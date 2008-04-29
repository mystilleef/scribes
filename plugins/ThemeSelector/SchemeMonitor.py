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
This module documents a class that monitor color schemes in the

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

class Monitor(object):
	"""
	This class monitors the scheme folders in the user's home folder.
	"""

	def __init__(self, editor, manager):
		self.__init_attributes(editor, manager)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		# Monitor database for changes.
		from gnomevfs import monitor_add, MONITOR_DIRECTORY
		self.__monid1 = monitor_add(self.__uri1, MONITOR_DIRECTORY,
					self.__folder_changed_cb)
		self.__monid2 = monitor_add(self.__uri2, MONITOR_DIRECTORY,
					self.__folder_changed_cb)

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		from os.path import join
		scribes_path = join(self.__editor.home_folder, ".gnome2/scribes/styles")
		gedit_path = join(self.__editor.home_folder, ".gnome2/gedit/styles")
		from gnomevfs import get_uri_from_local_path
		self.__uri1 = get_uri_from_local_path(scribes_path)
		self.__uri2 = get_uri_from_local_path(gedit_path)
		self.__monid1 = self.__monid2 = self.__monid3 = None
		return

	def __folder_changed(self):
		self.__manager.emit("folder-changed")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		from gnomevfs import monitor_cancel
		if self.__monid1: monitor_cancel(self.__monid1)
		if self.__monid2: monitor_cancel(self.__monid2)
		if self.__monid3: monitor_cancel(self.__monid3)
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return

	def __folder_changed_cb(self, *args):
		self.__folder_changed()
		return True
