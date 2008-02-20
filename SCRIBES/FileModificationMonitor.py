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

save_dbus_service = "org.sourceforge.ScribesSaveProcessor"

class FileModificationMonitor(object):
	"""
	This class creates an object that checks if a file opened by Scribes
	has been modified by a third party application.
	"""

	def __init__(self, editor):
		"""
		Initialize object.

		@param self: Reference to the FileModificationMonitor instance.
		@type self: A FileModificationMonitor object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(editor)
		self.__signal_id_1 = editor.connect("rename-document", self.__rename_document_cb)
		self.__signal_id_2 = editor.connect("renamed-document", self.__renamed_document_cb)
		self.__signal_id_3 = editor.connect("loaded-document", self.__renamed_document_cb)
		self.__signal_id_4 = editor.connect("close-document", self.__close_document_cb)
		self.__signal_id_5 = editor.connect("close-document-no-save", self.__close_document_cb)
		editor.session_bus.add_signal_receiver(self.__saved_document_cb,
						signal_name="saved_file",
						dbus_interface=save_dbus_service)
		editor.session_bus.add_signal_receiver(self.__saved_document_cb,
						signal_name="error",
						dbus_interface=save_dbus_service)
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__precompile_methods, priority=PRIORITY_LOW)

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the FileModificationMonitor instance.
		@type self: A FileModificationMonitor object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__modification_dialog = None
		self.__last_modification_time = None
		self.__monitor_id = None
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		self.__signal_id_4 = self.__signal_id_5 = None
		return

	def __start_monitoring_file(self):
		"""
		Start monitoring a file.

		@param self: Reference to the FileModificationMonitor instance.
		@type self: A FileModificationMonitor object.
		"""
		if not self.__editor.uri.startswith("file:///"): return
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monitor_id = monitor_add(self.__editor.uri, MONITOR_FILE,
					self.__file_changed_cb)
		return

	def __stop_monitoring_file(self):
		"""
		Stop monitoring a file.

		@param self: Reference to the FileModificationMonitor instance.
		@type self: A FileModificationMonitor object.
		"""
		self.__last_modification_time = None
		from gnomevfs import monitor_cancel
		if not self.__monitor_id: return
		monitor_cancel(self.__monitor_id)
		return

	def __show_modification_dialog(self):
		"""
		Show a dialog when another application modifies this file.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.
		"""
		try:
			self.__modification_dialog.show()
		except AttributeError:
			from ModificationDialog import ModificationDialog
			self.__modification_dialog = ModificationDialog(self, self.__editor)
			self.__modification_dialog.show()
		return

	def __get_file_info(self):
		"""
		Get file information about the file.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.

		@return: An object containing file information.
		@rtype: A gnomevfs.FILE_INFO object.
		"""
		try:
			if self.__editor.uri is None: return None
			if self.__editor.uri.startswith("file:///") is False: return None
			from gnomevfs import get_file_info
			fileinfo = get_file_info(self.__editor.uri)
		except:			return None		return fileinfo

	def __destroy(self):
		"""
		Destroy this object.

		@param self: Reference to the FileModificationMonitor instance.
		@type self: A FileModificationMonitor object.
		"""
		self.__stop_monitoring_file()
		if self.__modification_dialog: self.__modification_dialog.destroy()
		self.__editor.session_bus.remove_signal_receiver(
						self.__saved_document_cb,
						signal_name="saved_file",
						dbus_interface=save_dbus_service)
		self.__editor.session_bus.remove_signal_receiver(
						self.__saved_document_cb,
						signal_name="error",
						dbus_interface=save_dbus_service)
		self.__editor.disconnect_signal(self.__signal_id_1, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_5, self.__editor)
		del self
		self = None
		return

	def __precompile_methods(self):
		"""
		Use psyco to optimize methods.

		@param self: Reference to the FileModificationMonitor instance.
		@type self: A FileModificationMonitor object.
		"""
		try:
			from psyco import bind
			bind(self.__get_file_info)
			bind(self.__saved_document_cb)
		except ImportError:
			pass
		return False

	def __file_changed_cb(self, monitor_uri, info_uri, event_type):
		"""
		Handles callback when the current file is modified.

		@param self: Reference to the FileModificationMonitor instance.
		@type self: An FileModificationMonitor object.

		@param monitor_uri: The uri that is monitored.
		@type monitor_uri: A String object.

		@param info_uri: The uri that is monitored.
		@type info_uri: A String object.

		@param event_type: The type of modification that occured.
		@type event_type: A gnomevfs.MONITOR_EVENT* object.
		"""
		from gnomevfs import MONITOR_EVENT_DELETED
		from gnomevfs import MONITOR_EVENT_CREATED
		from gnomevfs import MONITOR_EVENT_CHANGED
		if event_type in [MONITOR_EVENT_DELETED, MONITOR_EVENT_CREATED, MONITOR_EVENT_CHANGED]:
			try:
				if self.__last_modification_time == self.__get_file_info().mtime: return
				print "Another program is modifying document"
				self.__show_modification_dialog()
			except AttributeError:
				pass
		return

	def __rename_document_cb(self, *args):
		"""
		Handles callback when the "rename-document" signal is emitted.

		@param self: Reference to the FileModificationMonitor instance.
		@type self: A FileModificationMonitor object.
		"""
		self.__stop_monitoring_file()
		return

	def __renamed_document_cb(self, *args):
		"""
		Handles callback when the "rename-document" signal is emitted.

		@param self: Reference to the FileModificationMonitor instance.
		@type self: A FileModificationMonitor object.
		"""
		self.__start_monitoring_file()
		return

	def __saved_document_cb(self, *args):
		try:
			self.__last_modification_time = self.__get_file_info().mtime
		except AttributeError:
			pass
		return

	def __close_document_cb(self, *args):
		self.__destroy()
		return
