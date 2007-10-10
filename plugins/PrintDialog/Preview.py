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
The modules exposes a class that creates a print preview window object.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gnomeprint.ui import JobPreview

class PrintPreview(JobPreview):
	"""
	This class creates an object that allows users to preview the content of
	the text editor before printing it.
	"""

	def __init__(self, printdialog, job):
		"""
		Initialize the JobPreview object.

		@param self: Reference to the ScribesJobPreview instance.
		@type self: A ScribesJobPreview object.

		@param printdialog: A print dialog associated with the preview window.
		@type printdialog: A gnomeprint.ui.Dialog object.
		"""
		self.__init_attributes(printdialog, job)
		from i18n import msg0004
		JobPreview.__init__(self, self.__job, msg0004)
		self.__set_properties()
		self.show_all()

	def __init_attributes(self, printdialog, job):
		"""
		Initialize the preview object's attributes.

		@param self: Reference to the ScribesJobPreview instance.
		@type self: A ScribesJobPreview object.

		@param printdialog: A print dialog associated with the preview window.
		@type printdialog: A gnomeprint.ui.Dialog object.
		"""
		self.__dialog = printdialog
		self.__job = job
		return

	def __set_properties(self):
		"""
		Set the preview object's properties.

		@param self: Reference to the ScribesJobPreview instance.
		@type self: A ScribesJobPreview object.
		"""
		self.set_icon_name("stock_print")
		self.set_transient_for(self.__dialog)
		return

	def __destroy(self):
		del self
		self = None
		return

	def destroy(self):
		self.__destroy()
		return
