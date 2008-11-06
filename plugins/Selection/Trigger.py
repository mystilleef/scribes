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
This module documents a class that creates triggers to perform selection
operations.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2006 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class Trigger(object):
	"""
	Creates triggers that perform selection operations. Triggers map 
	keyboard shortcuts to operations.
	"""

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = self.__trigger1.connect("activate", self.__word_cb)
		self.__sigid2 = self.__trigger2.connect("activate", self.__statement_cb)
		self.__sigid3 = self.__trigger3.connect("activate", self.__line_cb)
		self.__sigid4 = self.__trigger4.connect("activate", self.__paragraph_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__manager = None
		self.__trigger1 = self.__create_trigger("select_word", "alt+w")
		self.__trigger2 = self.__create_trigger("select_statement", "alt+s")
		self.__trigger3 = self.__create_trigger("select_line", "al+l")
		self.__trigger4 = self.__create_trigger("select_paragraph", "alt+p")
		return

	def __get_manager(self):
		if self.__manager: return self.__manager
		from Manager import Manager
		self.__manager = Manager(self.__editor)
		return self.__manager

	def __create_trigger(self, name, shortcut):
		trigger = self.__editor.create_trigger(name, shortcut)
		self.__editor.add_trigger(trigger)
		return trigger

	def __word_cb(self, *args):
		self.__get_manager().select_word()
		return False

	def __statement_cb(self, *args):
		self.__get_manager().select_statement()
		return False

	def __line_cb(self, *args):
		self.__get_manager().select_line()
		return False

	def __paragraph_cb(self, *args):
		self.__get_manager().select_paragraph()
		return False

	def __destroy(self):
		if self.__manager: self.__manager.destroy()
		self.__editor.remove_triggers((self.__trigger1, self.__trigger2,
		self.__trigger3, self.__trigger4))
		self.__editor.disconnect_signal(self.__sigid1, self.__trigger1)
		self.__editor.disconnect_signal(self.__sigid2, self.__trigger2)
		self.__editor.disconnect_signal(self.__sigid3, self.__trigger3)
		self.__editor.disconnect_signal(self.__sigid4, self.__trigger4)
		del self
		self = None
		return

	def destroy(self):
		self.__destroy()
		return False
