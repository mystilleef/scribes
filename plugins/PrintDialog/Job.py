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
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""
This module exposes a class responsible for printing the content of the text
editor's buffer.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtksourceview import SourcePrintJob

class PrintJob(SourcePrintJob):
	"""
	This class creates an object responsible for printing the content of the
	text editor's buffer.
	"""

	def __init__(self, editor):
		"""
		Initialize the PrintJob object.

		@param self: Reference to the PrintJob instance.
		@type self: A PrintJob object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		from gnomeprint import config_default
		config = config_default()
		SourcePrintJob.__init__(self, config, editor.textbuffer)
		self.__init_attributes(editor)
		self.__set_properties()

	def get_job(self):
		"""
		Create a print job object.

		@param self: Reference to the PrintJob instance.
		@type self: A PrintJob object.
		"""
		job = self.print_()
		return job

	def __init_attributes(self, editor):
		"""
		Initialize the PrintJob's attributes

		@param self: Reference to the PrintJob instance.
		@type self: A PrintJob object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		from i18n import msg0003
		from urllib import url2pathname
		self.__header = msg0003 + str(url2pathname(editor.uri))
		return

	def __set_properties(self):
		"""
		Initialize the PrintJob's properties.

		@param self: Reference to the PrintJob instance.
		@type self: A PrintJob object.
		"""
		self.set_highlight(True)
		self.set_print_header(True)
		self.set_print_numbers(False)
		self.set_tabs_width(4)
		from gtk import WRAP_WORD
		self.set_wrap_mode(WRAP_WORD)
		self.set_header_format(self.__header, "", "", True)
		return

	def __destroy(self):
		del self
		self = None
		return

	def destroy(self):
		self.__destroy()
		return
