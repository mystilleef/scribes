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
This module documents a class that creates a trigger shows the recent
menu.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class RecentMenuTrigger(object):
	"""
	This class creates an object that shows the text editor's recent
	menu.
	"""

	def __init__(self, editor):
		"""
		Initialize the trigger.

		@param self: Reference to the RecentMenuTrigger instance.
		@type self: An RecentMenuTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(editor)
		self.__create_trigger()
		self.__signal_id_1 = self.__trigger.connect("activate", self.__show_recent_menu_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the trigger's attributes.

		@param self: Reference to the RecentMenuTrigger instance.
		@type self: A RecentMenuTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__trigger = None
		self.__signal_id_1 = None
		self.__is_shown = False
		return

	def __create_trigger(self):
		"""
		Create the trigger.

		@param self: Reference to the RecentMenuTrigger instance.
		@type self: A RecentMenuTrigger object.
		"""
		# Trigger to show the recent menu.
		from SCRIBES.Trigger import Trigger
		self.__trigger = Trigger("show_recent_menu", "ctrl - O")
		self.__editor.add_trigger(self.__trigger)
		return

	def __show_recent_menu_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the RecentMenuTrigger instance.
		@type self: A RecentMenuTrigger object.

		@param trigger: An object to show the document browser.
		@type trigger: A Trigger object.
		"""
		# This is a nasty hack. I have no choice.
		open_toolbutton = self.__editor.toolbar.get_nth_item(1)
		open_toolbutton.get_children()[0].get_children()[1].activate()
		return

	def destroy(self):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the RecentMenuTrigger instance.
		@type self: An RecentMenuTrigger object.

		@param trigger: Reference to the RecentMenuTrigger instance.
		@type trigger: An RecentMenuTrigger object.
		"""
		from SCRIBES.utils import disconnect_signal, delete_attributes
		disconnect_signal(self.__signal_id_1, self.__trigger)
		self.__editor.remove_trigger(self.__trigger)
		delete_attributes(self)
		del self
		self = None
		return
