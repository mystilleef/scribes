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
This module documents a class that loads the advanced configuration
window plugin.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

name = "Advanced configuration plugin"
authors = ["Lateef Alabi-Oki <mystilleef@gmail.com>"]
version = 0.1
autoload = True
class_name = "AdvancedConfigurationPlugin"
short_description = "Shows the advanced configuration window."
long_description = """Shows the advanced configuration window. The
window allows user to configure advanced options provided by the
editor."""

class AdvancedConfigurationPlugin(object):
	"""
	This class loads a plugin that shows the advanced configuration
	window.
	"""

	def __init__(self, editor):
		"""
		Initialize object.

		@param self: Reference to the AdvancedConfigurationPlugin instance.
		@type self: A AdvancedConfigurationPlugin object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__trigger = None

	def load(self):
		"""
		Load advanced configuration window.

		@param self: Reference to the AdvancedConfigurationPlugin instance.
		@type self: An AdvancedConfigurationPlugin object.
		"""
		from AdvancedConfiguration.Trigger import Trigger
		self.__trigger = Trigger(self.__editor)
		return

	def unload(self):
		"""
		Unload advanced configuration window.

		@param self: Reference to the AdvancedConfigurationPlugin instance.
		@type self: An AdvancedConfigurationPlugin object.
		"""
		self.__trigger.destroy()
		return
