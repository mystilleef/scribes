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
This modules exposes a class responsible for creating the text editor's
print dialog.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class PrintDialog(object):
	"""
	This class creates the print dialog for the text editor.
	"""

	def __init__(self, editor):
		"""
		Initialize the print dialog.

		@param self: Reference to the ScribesPrintDialog instance.
		@type self: A ScribesPrintDialog object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(editor)
		self.__set_properties()
		self.__signal_id_1 = self.__dialog.connect("response", self.__printdialog_response_cb)
		self.__show_dialog()

	def __init_attributes(self, editor):
		"""
		Initialize the Dialog's attributes.

		@param self: Reference to the ScribesPrintDialog instance.
		@type self: A ScribesPrintDialog object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__status_id = None
		from Job import PrintJob
		self.__printjob  = PrintJob(editor)
		self.__job = self.__printjob.get_job()
		from gnomeprint.ui import Dialog, DIALOG_RANGE
		from i18n import msg0001
		self.__dialog = Dialog(self.__job, msg0001, DIALOG_RANGE)
		self.__signal_id_1 = None
		self.__preview = None
		return

	def __set_properties(self):
		"""
		Set the dialog's properties.

		@param self: Reference to the ScribesPrintDialog instance.
		@type self: A ScribesPrintDialog object.
		"""
		width, height = self.__editor.calculate_resolution_independence(self.__editor.window,
															1.6, 1.929648241)
		self.__dialog.set_default_size(width, height)
		self.__dialog.set_icon_name("stock_print")
		self.__dialog.set_transient_for(self.__editor.window)
		return

	def __show_dialog(self):
		"""
		Show the print dialog.

		@param self: Reference to the ScribesPrintDialog instance.
		@type self: A ScribesPrintDialog object.
		"""
		from i18n import msg0002
		self.__status_id = self.__editor.feedback.set_modal_message(msg0002, "print")
		self.__editor.emit("show-dialog", self.__dialog)
		self.__dialog.run()
		return

	def __printdialog_response_cb(self, dialog, response):
		"""
		Handles callback when the "response" signal is emitted.

		@param self: Reference to the ScribesPrintDialog instance.
		@type self: A ScribesPrintDialog object.
		"""
		from gnomeprint.ui import DIALOG_RESPONSE_PRINT, DIALOG_RESPONSE_PREVIEW
		if response == DIALOG_RESPONSE_PREVIEW:
			from Preview import PrintPreview
			self.__preview = PrintPreview(self.__dialog, self.__job)
		elif response == DIALOG_RESPONSE_PRINT:
			self.__editor.feedback.unset_modal_message(self.__status_id)
			self.__job.print_()
			self.__editor.emit("hide-dialog", self.__dialog)
			self.__dialog.hide()
			self.__destroy()
		else:
			self.__editor.feedback.unset_modal_message(self.__status_id)
			self.__editor.emit("hide-dialog", self.__dialog)
			self.__dialog.hide()
			self.__destroy()
		return

	def __destroy(self):
		"""
		Destroy instance of this class.

		@param self: Reference to the PrintDialog instance.
		@type self: A PrintDialog object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self.__dialog)
		self.__dialog.destroy()
		self.__printjob.destroy()
		if self.__preview: self.__preview.destroy()
		del self
		self = None
		return
