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

	def __init__(self, editor, name, accelerator=None, description=None, error=True, removable=True):
		GObject.__init__(self)
		self.__init_attributes(editor, name, accelerator, description, error, removable)
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=9999)

	def __init_attributes(self, editor, name, accelerator, description, error, removable):
		self.__editor = editor
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
		if not (self.__accelerator): return None
		return self.__accelerator

	def __get_description(self):
		if not (self.__description): return None
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
		self.__editor.refresh(False)
		self.__editor.set_vm_interval(False)
		self.emit("activate")
		self.__editor.set_vm_interval(True)
		self.__editor.refresh(False)
		return

	def destroy(self):
		del self.__name, self.__description, self.__accelerator, self
		self = None
		return

	def __precompile_methods(self):
		methods = (self.activate, self.__get_name, self.__get_accelerator)
		self.__editor.optimize(methods)
		return False

