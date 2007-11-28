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
This modules documents a class that creates triggers. Triggers are
actions that can be called globally to perform common user operations.
Triggers are usually associated with keyboard shortcuts.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE

class Trigger(GObject):
	"""
	This class creates an object associated with an operation or a
	keyboard shortcut.
	"""

	__gsignals__ = {
		"activate": (SIGNAL_RUN_LAST, TYPE_NONE, ())
	}

	def __init__(self, name, accelerator=None, description=None, error=True, removable=True):
		"""
		Initialize object.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.

		@param name: A name associated with a trigger.
		@type name: A String object.

		@param accelerator: An accelerator associated with a trigger.
		@type accelerator: A String object.

		@param description: A description associated with a trigger.
		@type description: A String object.

		@param error: If True, print an error message when a duplicate
			trigger is found. If False, try to remove the duplicate.
		@type error: A Boolean object.

		@param removable: In the event a duplicate trigger is found, True
			if this trigger should be removed or destroyed.
		@type removable: A Boolean object.
		"""
		self.__precompile_methods()
		GObject.__init__(self)
		self.__init_attributes(name, accelerator, description, error, removable)

	def __init_attributes(self, name, accelerator, description, error, removable):
		"""
		Initialize data attributes.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.

		@param name: A name associated with a trigger.
		@type name: A String object.

		@param accelerator: An accelerator associated with a trigger.
		@type accelerator: A String object.

		@param description: A description associated with a trigger.
		@type description: A String object.

		@param error: If True, print an error message when a duplicate
			trigger is found. If False, try to remove the duplicate.
		@type error: A Boolean object.

		@param removable: In the event a duplicate trigger is found, True
			if this trigger should be removed or destroyed.
		@type removable: A Boolean object.
		"""
		self.__name = name
		self.__accelerator = accelerator
		self.__description = description
		self.__error = error
		self.__removable = removable
		return

########################################################################
#
#					Getters For Public Porperties
#
########################################################################

	def __get_name(self):
		return self.__name

	def __get_accelerator(self):
		from operator import not_
		if not_(self.__accelerator): return None
		return self.__accelerator

	def __get_description(self):
		from operator import not_
		if not_(self.__description): return None
		return self.__description

	def __get_error(self):
		return self.__error

	def __get_removable(self):
		return self.__removable

########################################################################
#
#							Public API
#
########################################################################

	name = property(__get_name)
	accelerator = property(__get_accelerator)
	description = property(__get_description)
	error = property(__get_error)
	removable = property(__get_removable)

	def activate(self):
		"""
		Activate the trigger.

		Emits a signal to trigger a callback handler connected to this
		trigger object.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.
		"""
		self.emit("activate")
		return

	def destroy(self):
		"""
		Destroy object.

		@param self: Reference to the Trigger instance.
		@type self: A Trigger object.
		"""
		del self.__name, self.__description, self.__accelerator, self
		self = None
		return

	def __precompile_methods(self):
		try:
			from psyco import bind
			bind(self.__get_name)
			bind(self.__get_accelerator)
		except ImportError:
			pass
		return False
