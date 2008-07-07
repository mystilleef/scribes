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
Bookmark actions for the text editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class Trigger(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = editor.textview.connect_after("populate-popup", self.__popup_cb)
		self.__sigid2 = self.__trigger1.connect("activate", self.__toggle_bookmark_cb)
		self.__sigid3 = self.__trigger2.connect("activate", self.__remove_all_bookmarks_cb)
		self.__sigid4 = self.__trigger3.connect("activate", self.__show_browser_cb)

	def __init_attributes(self, editor):
		from Manager import Manager
		self.__manager = Manager(editor)
		self.__editor = editor
		self.__trigger1 = self.__create_trigger("toggle-bookmark", "ctrl - d")
		self.__trigger2 = self.__create_trigger("remove-all-bookmarks", "ctrl - B")
		self.__trigger3 = self.__create_trigger("show-bookmark-browser", "ctrl - b")
		return

	def __create_trigger(self, name, shortcut):
		trigger = self.__editor.create_trigger(name, shortcut)
		self.__editor.add_trigger(trigger)
		return trigger

	def destroy(self):
		triggers = (self.__trigger1, self.__trigger2, self.__trigger3)
		self.__editor.remove_triggers(triggers)
		self.__editor.disconnect_signal(self.__sigid1, self.__editor.textview)
		self.__editor.disconnect_signal(self.__sigid2, self.__trigger1)
		self.__editor.disconnect_signal(self.__sigid3, self.__trigger2)
		self.__editor.disconnect_signal(self.__sigid4, self.__trigger3)
		del self
		self = None
		return

	def __popup_cb(self, textview, menu):
#		from PopupMenuItem import BookmarkPopupMenuItem
#		menu.prepend(BookmarkPopupMenuItem(self.editor, self.__manager))
#		menu.show_all()
		return False

	def __toggle_bookmark_cb(self, *args):
		self.__manager.toggle_bookmark()
		return False

	def __remove_all_bookmarks_cb(self, *args):
		self.__manager.remove_bookmarks()
		return False

	def __show_browser_cb(self, *args):
		return False
