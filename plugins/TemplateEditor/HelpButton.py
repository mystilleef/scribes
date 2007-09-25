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
This modules documents a class the defines the behavior of the help
button in the template editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class HelpButton(object):
	"""
	This class defines the behavior of the help button.
	"""

	def __init__(self, manager):
		"""
		Initialize object.

		@param self: Reference to the HelpButton instance.
		@type self: A HelpButton object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.
		"""
		self.__init_attributes(manager)
		self.__signal_id_1 = manager.connect("destroy", self.__destroy_cb)
		self.__signal_id_2 = self.__button.connect("clicked", self.__clicked_cb)

	def __init_attributes(self, manager):
		"""
		Initialize data attributes.

		@param self: Reference to the HelpButton instance.
		@type self: A HelpButton object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.
		"""
		self.__manager = manager
		self.__button = manager.glade.get_widget("HelpButton")
		self.__signal_id_1 = self.__signal_id_2 = None
		return

	def __destroy_cb(self, manager):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the HelpButton instance.
		@type self: A HelpButton object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.
		"""
		from SCRIBES.utils import delete_attributes, disconnect_signal
		disconnect_signal(self.__signal_id_1, manager)
		disconnect_signal(self.__signal_id_2, self.__button)
		self.__button.destroy()
		delete_attributes(self)
		self = None
		del self
		return

	def __clicked_cb(self, button):
		"""
		Handles callback when the "clicked" signal is emitted.

		@param self: Reference to the HelpButton instance.
		@type self: A HelpButton object.

		@param button: Reference to the help button.
		@type button: A gtk.Button object.
		"""
		from gnome import help_display
		help_display("/scribes.xml", "scribes-templates")
		return
