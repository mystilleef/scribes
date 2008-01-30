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
This module documents a class that saves files.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

PRIORITY = 10

class FileSaver(object):
	"""
	This class creates an object that saves the content of the text
	editor's buffer to a file.
	"""

	def __init__(self, editor):
		"""
		Initialize object.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(editor)
		self.__create_swap_folder_and_file()
		self.__signal_id_1 = editor.connect("close-document", self.__close_document_cb)
		self.__signal_id_2 = editor.connect("close-document-no-save", self.__close_document_no_save_cb)
		self.__signal_id_3 = editor.connect("save-document", self.__save_document_cb)
		self.__signal_id_4 = editor.connect("loading-document", self.__checking_document_cb)
		self.__signal_id_5 = editor.connect_after("loaded-document", self.__loaded_document_cb)
		self.__signal_id_6 = editor.connect_after("load-error", self.__load_error_cb)
		self.__signal_id_7 = editor.textbuffer.connect("modified-changed", self.__modified_changed_cb)
		self.__signal_id_8 = editor.connect_after("rename-document", self.__rename_document_cb)
		self.__signal_id_9 = editor.connect("saved-document", self.__saved_document_cb)
		self.__signal_id_10 = editor.store.connect("updated", self.__updated_cb)
		self.__signal_id_11 = editor.connect_after("renamed-document", self.__renamed_document_cb)
		self.__signal_id_12 = editor.connect_after("reload-document", self.__reload_document_cb)
		from gobject import timeout_add
		timeout_add(500, self.__check_encoding_manager)

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__termination_id = editor.register_object()
		self.__encoding_manager = self.__editor.get_object("EncodingManager")
		self.__should_rename = False
		self.__can_quit = False
		self.__file_info = None
		self.__save_timer = None
		self.__swap_folder = None
		self.__swap_uri = None
		self.__swap_file = None
		self.__last_modification_time = None
		self.__modification_dialog = None
		self.__do_not_save = False
		self.__toggle_readonly = False
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		self.__signal_id_4 = self.__signal_id_5 = self.__signal_id_6 = None
		self.__signal_id_7 = self.__signal_id_8 = self.__signal_id_9 = None
		self.__signal_id_10 = self.__monitor_id = self.__signal_id_11 = None
		self.__signal_id_12 = None
		self.__signal_id_4 = None

		return

########################################################################
#
#                           Public API
#
########################################################################

	def save_file(self, is_closing=False):
		"""
		Save content of text editor's buffer to a file.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.

		@param is_closing: True if this is the last call.
		@type is_closing: A Boolean object.
		"""
		from Exceptions import PermissionError, SwapError, FileWriteError
		from Exceptions import FileCloseError, FileCreateError, TransferError
		from Exceptions import DoNothingError, FileModificationError
		try:
			self.__can_save()
			self.__determine_action(is_closing)
			self.__check_permissions()
			self.__check_swap_folder_and_file()
			self.__save_file()
		except PermissionError:
			from internationalization import msg0469			self.__error(msg0469)		except SwapError:
			from internationalization import msg0471
			self.__error(msg0471)
		except FileModificationError:
			print "File has been modified by another program"
		except DoNothingError:			pass
		return False

	def reset_save_flag(self):
		"""
		Reset the "__do_not_save" flag to its default value.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.
		"""
		self.__do_not_save = False
		return

########################################################################
#
#                       Helper Methods
#
########################################################################

	def __save_file(self):
		"""
		Save document to a temporary file.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.
		"""
		self.__can_save()
		self.__editor.emit("saving-document", self.__editor.uri)
		text = self.__encode_text()
		from gnomevfs import OPEN_WRITE, URI
		from gnomevfs.async import create
		from Exceptions import FileCreateError
		try:
			try:
				# Write to a temporary file.
				create(uri=URI(self.__swap_uri),
						callback=self.__write_cb,
						open_mode=OPEN_WRITE,
						exclusive=False,
						perm=0644,
						priority=PRIORITY,
						data=text)
			except:
				raise FileCreateError		except FileCreateError:
			from internationalization import msg0472
			self.__error(msg0472)
		return

	def __write_cb(self, handle, result, text):
		"""
		Callback to the GNOME-VFS asynchronous create method.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.
		"""
		from Exceptions import FileWriteError
		try:
			self.__can_save()
			try:				handle.write(text, self.__close_cb)
			except:
				handle.cancel()
				raise FileWriteError
		except FileWriteError:
			from internationalization import msg0473
			self.__error(msg0473)
		return

	def __close_cb(self, handle, bytes, result, bytes_requested):
		"""
		Callback to the GNOME-VFS asynchronous write method.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.
		"""
		from Exceptions import FileCloseError
		try:
			self.__can_save()
			try:
				handle.close(self.__finalize_cb)
			except:
				handle.cancel()
				raise FileCloseError
		except FileCloseError:
			from internationalization import msg0474
			self.__error(msg0474)
		return

	def __finalize_cb(self, *args):
		"""
		Callback to the GNOME-VFS asynchronous close method.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.
		"""
		self.__can_save()
		self.__update_file_info()
		self.__begin_file_transfer()
		return

	def __begin_file_transfer(self):
		"""
		Transfer temporary file from swap location to permanent location.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.
		"""
		from gnomevfs import XFER_OVERWRITE_MODE_REPLACE
		from gnomevfs import XFER_ERROR_MODE_QUERY, URI
		from gnomevfs.async import xfer
		from Exceptions import TransferError
		XFER_TARGET_DEFAULT_PERMS = 1 << 12
		try:
			self.__can_save()
			try:
				xfer(source_uri_list=[URI(self.__swap_uri)],
					target_uri_list=[URI(self.__editor.uri)],
					xfer_options=XFER_TARGET_DEFAULT_PERMS,
					error_mode=XFER_ERROR_MODE_QUERY,
					priority = PRIORITY,
					overwrite_mode=XFER_OVERWRITE_MODE_REPLACE,
					progress_update_callback=self.__update_cb,
					update_callback_data=self.__swap_file,
					progress_sync_callback=self.__sync_cb)
			except:
				raise TransferError
		except TransferError:
			from internationalization import msg0470
			self.__error(msg0470)
		return

	def __sync_cb(self, info):
		"""
		Callback the GNOME-VFS asynchronous transfer method.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.
		"""
		from Exceptions import DoNothingError
		try:
			self.__can_save()
			if info.vfs_status:
				return False
		except DoNothingError:
			return False
		return  True

	def __update_cb(self, handle, info, data):
		"""
		Callback to the GNOME-VFS asynchronous transfer method.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.
		"""
		from Exceptions import TransferError, DoNothingError
		try:
			self.__can_save()
			if info.vfs_status:
				# A transfer error occured.
				handle.cancel()
				raise TransferError
			from gnomevfs import XFER_PHASE_COMPLETED
			from operator import ne
			if ne(info.phase, XFER_PHASE_COMPLETED): return True
			from gobject import idle_add
			self.__set_file_info()
			self.__finish_up()
		except TransferError:
			from internationalization import msg0470
			self.__error(msg0470)
		except DoNothingError:
			pass
		return True

	def __set_file_info(self):
		"""
		Set correct permissions of a file after it has been saved.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.
		"""
		from operator import not_
		if not_(self.__file_info): return False
		try:
			from gnomevfs import set_file_info, SET_FILE_INFO_PERMISSIONS
			set_file_info(self.__editor.uri, self.__file_info, SET_FILE_INFO_PERMISSIONS)
		except:
			pass
		return False

	def __finish_up(self):
		"""
		Finalize the saving process.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.
		"""
		self.__file_info = None
		if self.__toggle_readonly:
			self.__toggle_readonly = False
			self.__editor.trigger("toggle_readonly")
		if self.__should_rename:
			self.__editor.emit("renamed-document", self.__editor.uri)
		else:
			self.__editor.emit("saved-document", self.__editor.uri)		self.__should_rename = False
		if self.__can_quit:
			self.__destroy()
		else:
			self.__update_modification_time()
		return False

	def __update_modification_time(self):
		fileinfo = self.__get_file_info()
		from operator import not_
		if not_(fileinfo): return
		self.__last_modification_time = fileinfo.mtime
		return

	def __encode_text(self):
		"""
		Convert the encoding of the content of the document from "UTF-8"
		to an encoding specified by the user, or back to "UTF-8"

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.

		@return: An encoded string.
		@rtype: A String object.
		"""
		try:
			self.__can_save()
			start, end = self.__editor.textbuffer.get_bounds()
			text = self.__editor.textbuffer.get_text(start, end)
			unicode_text = text.decode("utf8")
			encoded_text = unicode_text.encode(self.__encoding_manager.get_encoding())
		except UnicodeEncodeError:
			from internationalization import msg0476
			self.__error(msg0476)
		except UnicodeDecodeError:
			from internationalization import msg0475
			self.__error(msg0475)
		return encoded_text

	def __check_permissions(self):
		"""
		Check the permissions of a file.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.
		"""
		self.__can_save()
		from operator import not_, is_
		if not_(self.__editor.uri.startswith("file:///")): return
		from gnomevfs import get_local_path_from_uri
		file_path = get_local_path_from_uri(self.__editor.uri)
		from os import access, W_OK, path
		folder_path = path.dirname(file_path)
		from Exceptions import PermissionError
		if is_(access(folder_path, W_OK), False):
			raise PermissionError		elif is_(access(file_path, W_OK), False):
			if path.exists(file_path): raise PermissionError
		return

	def __create_swap_folder_and_file(self):
		"""
		Create the swap location and temporary file.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.
		"""
		# Create a temporary folder.
		from tempfile import mkdtemp, NamedTemporaryFile
		try:
			self.__can_save()
			self.__swap_folder = mkdtemp(suffix="scribes",
										prefix=".Scribes",
										dir= self.__editor.home_folder)
			# Create a randomly generated temporary file in the
			# temporary folder created above.
			self.__swap_file = NamedTemporaryFile(mode="w+",
												suffix="Scribes",
												prefix="scribes",
												dir=self.__swap_folder)
			from gnomevfs import get_uri_from_local_path
			self.__swap_uri = get_uri_from_local_path(self.__swap_file.name)
		except:
			from Exceptions import SwapError
			raise SwapError
		return

	def __delete_swap_folder_and_file(self):
		"""
		Remove swap location.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.
		"""
		try:
			self.__swap_file.close()
			from os import rmdir
			rmdir(self.__swap_folder)
		except:
			pass
		return

	def __check_swap_folder_and_file(self):
		"""
		Check if swap location and temporary file exists.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.
		"""
		from gnomevfs import exists
		from operator import not_
		if not_(exists(self.__swap_uri)):
			print "Woops swap area not found: creating..."
			self.__create_swap_folder_and_file()
		return

	def __determine_action(self, is_closing):
		"""
		Determine what saving action to take for files that have not
		yet been saved to disk.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.

		@param is_closing: True if this is the last save call.
		@type is_closing: A Boolean object.
		"""
		self.__can_save()
		if self.__editor.uri: return
		if is_closing:			# Create a new file and save it if the text editor's buffer
			# contains a document but there is no document to save.
			self.__can_quit = True
			self.__editor.create_new_file()
			self.save_file()
		else:
			# Show the save dialog if the text editor's buffer is empty and
			# there is no document to save.
			self.__editor.trigger("show_save_dialog")
		from Exceptions import DoNothingError
		raise DoNothingError
		return

	def __update_file_info(self):
		"""
		Update file information.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.
		"""
		try:
			self.__file_info = None
			fileinfo = self.__get_file_info()
			from gnomevfs import FILE_INFO_FIELDS_PERMISSIONS
			if fileinfo.valid_fields & FILE_INFO_FIELDS_PERMISSIONS:
				self.__file_info = fileinfo
		except:
			pass
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
			from operator import is_
			if is_(self.__editor.uri, None): return None
			if is_(self.__editor.uri.startswith("file:///"), False): return None
			from gnomevfs import get_file_info
			fileinfo = get_file_info(self.__editor.uri)
		except:			return None		return fileinfo

	def __error(self, message):
		"""
		Show error message.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.

		@param message: An error message.
		@type message: A String object.
		"""
		self.__file_info = None
		from internationalization import msg0477, msg0468
		title = msg0477 % (self.__editor.uri)
		message_id = self.__editor.feedback.set_modal_message(msg0468, "error")
		self.__editor.show_error_message(message, title, self.__editor.window)
		self.__editor.emit("save-error", str(self.__editor.uri))
		self.__editor.feedback.unset_modal_message(message_id)
		return

	def __save_file_timeout_cb(self):
		"""
		Callback to the save timeout add function.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.
		"""
		from gobject import idle_add
		idle_add(self.save_file)
		return False

	def __remove_save_timer(self):
		"""
		Remove timer.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.
		"""
		try:
			from gobject import source_remove
			source_remove(self.__save_timer)
		except:
			pass
		return

	def __destroy(self):
		"""
		Destroy instance of this class.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.
		"""
		if self.__modification_dialog: self.__modification_dialog.destroy()
		self.__stop_monitoring_file()
		self.__encoding_manager.destroy()
		self.__remove_save_timer()
		self.__delete_swap_folder_and_file()
		self.__editor.disconnect_signal(self.__signal_id_1, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_5, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_6, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_7, self.__editor.textbuffer)
		self.__editor.disconnect_signal(self.__signal_id_8, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_9, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_10, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_11, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_12, self.__editor)
		self.__editor.unregister_object(self.__termination_id)
		del self
		self = None
		return

	def __precompile_methods(self):
		"""
		Use Psyco to optimize some methods.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.
		"""
		try:
			from psyco import bind
			bind(self.__encode_text)
			bind(self.__save_file)
			bind(self.__check_permissions)
			bind(self.__can_save)
			bind(self.__get_file_info)
		except ImportError:
			pass
		return

	def __check_last_modification(self):
		"""
		Check if the document has been modified by another application.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.
		"""
		from operator import not_, is_, eq
		fileinfo = self.__get_file_info()
		if not_(fileinfo): return
		if is_(self.__last_modification_time, None): return
		if eq(self.__last_modification_time, fileinfo.mtime): return
		from Exceptions import FileModificationError
		raise FileModificationError
		return

	def __start_monitoring_file(self):
		from operator import not_
		if not_(self.__editor.uri.startswith("file:///")): return
		# Monitor database for changes.
		self.__update_modification_time()
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monitor_id = monitor_add(self.__editor.uri, MONITOR_FILE,
					self.__file_changed_cb)
		return

	def __stop_monitoring_file(self):
		from gnomevfs import monitor_cancel
		from operator import not_
		if not_(self.__monitor_id): return
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

	def __can_save(self):
		"""
		Check whether or not to save the current file.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.
		"""
		from Exceptions import DoNothingError
		if self.__do_not_save: raise DoNothingError
		return

########################################################################
#
#                       Signal and Event Handlers
#
########################################################################

	def __close_document_cb(self, editor):
		"""
		Handles callback when the "close-document" signal is emitted.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__can_quit = True
		self.__remove_save_timer()
		from operator import not_
		if not_(editor.file_is_saved):
			from gobject import idle_add
			idle_add(self.save_file, True)
		else:
			self.__destroy()
		return

	def __close_document_no_save_cb(self, editor):
		"""
		Handles callback when the "close-document-no-save" signal is emitted.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__remove_save_timer()
		self.__destroy()
		return

	def __checking_document_cb(self, editor, uri):
		"""
		Handles callback when the "checking-document" signal is emitted.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param uri: Reference to a file.
		@type uri: A String object.
		"""
		editor.textbuffer.handler_block(self.__signal_id_7)
		return

	def __loaded_document_cb(self, editor, uri):
		"""
		Handles callback when the "loaded-document" signal is emitted.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param uri: Reference to a file.
		@type uri: A String object.
		"""
		editor.textbuffer.handler_unblock(self.__signal_id_7)
		self.__start_monitoring_file()
		return

	def __load_error_cb(self, editor, uri):
		"""
		Handles callback when the "load-error" signal is emitted.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param uri: Reference to a file.
		@type uri: A String object.
		"""
		editor.textbuffer.handler_unblock(self.__signal_id_7)
		return

	def __save_document_cb(self, editor):
		"""
		Handles callback when the "save-document" signal is emitted.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		from gobject import idle_add, PRIORITY_HIGH
		idle_add(self.save_file, priority = PRIORITY_HIGH)
		return

	def __saved_document_cb(self, editor, uri):
		"""
		Handles callback when the "saved-document" signal is emitted.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param uri: Reference to a file.
		@type uri: A String object.
		"""
		self.__remove_save_timer()
		return

	def __modified_changed_cb(self, textbuffer):
		"""
		Handles callback when the "modified-changed" signal is emitted.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.

		@param textbuffer: Reference to the text editor's buffer.
		@type textbuffer: A ScribesTextBuffer object.
		"""
		if textbuffer.get_modified() is False: return False
		self.__editor.emit("modified-document")
		if self.__editor.uri is None: return True
		from gobject import timeout_add, PRIORITY_LOW
		self.__save_timer = timeout_add(21000, self.__save_file_timeout_cb, priority=PRIORITY_LOW)
		return True

	def __reload_document_cb(self, *args):
		self.__remove_save_timer()
		return

	def __rename_document_cb(self, editor, uri):
		"""
		Handles callback when the "rename-document" signal is emitted.

		@param self: Reference to the FileSaver instance.
		@type self: A FileSaver object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param uri: Reference to a file.
		@type uri: A String object.
		"""
		self.__stop_monitoring_file()
		if self.__editor.is_readonly: self.__toggle_readonly = True
		self.__should_rename = True
		from gobject import idle_add, PRIORITY_HIGH
		idle_add(self.save_file, priority = PRIORITY_HIGH)
		return

	def __updated_cb(self, store, name):
		from operator import ne
		if ne(name, "EncodingManager"): return
		self.__encoding_manager = store.get_object("EncodingManager")
		return

	def __check_encoding_manager(self):
		if self.__encoding_manager: return False
		self.__encoding_manager = self.__editor.get_object("EncodingManager")
		return True

	def __file_changed_cb(self, monitor_uri, info_uri, event_type):
		"""
		Handles callback when the current file is modified.

		@param self: Reference to the AutoReplaceManager instance.
		@type self: An AutoReplaceManager object.

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
			if self.__can_quit: return
			fileinfo = self.__get_file_info()
			from operator import not_, eq
			if not_(fileinfo): return
			if eq(self.__last_modification_time, fileinfo.mtime): return
			self.__do_not_save = True
			self.__show_modification_dialog()
		return

	def __renamed_document_cb(self, *args):
		self.__start_monitoring_file()
		return

