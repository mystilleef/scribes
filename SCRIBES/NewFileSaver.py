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

# Save file 7 seconds after modification.
SAVE_TIMER = 7000  # units in milliseconds (1000th of a second)
save_dbus_service = "org.sourceforge.ScribesSaveProcessor"

class FileSaver(object):
	"""
	This class creates an object that saves the content of the text
	editor's buffer to a file.
	"""

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__signal_id_1 = editor.connect("close-document", self.__close_document_cb)
		self.__signal_id_2 = editor.connect("close-document-no-save", self.__close_document_no_save_cb)
		self.__signal_id_3 = editor.connect("save-document", self.__save_document_cb)
		self.__signal_id_4 = editor.connect("checking-document", self.__checking_document_cb)
		self.__signal_id_5 = editor.connect_after("loaded-document", self.__loaded_document_cb)
		self.__signal_id_6 = editor.connect_after("load-error", self.__load_error_cb)
		self.__signal_id_7 = editor.textbuffer.connect("modified-changed", self.__modified_changed_cb)
		self.__signal_id_8 = editor.connect_after("rename-document", self.__rename_document_cb)
		self.__signal_id_9 = editor.connect("saved-document", self.__saved_document_cb)
		self.__signal_id_10 = editor.connect_after("reload-document", self.__reload_document_cb)
		self.__signal_id_11 = editor.connect("saving-document", self.__saving_document_cb)
		self.__signal_id_12 = editor.connect("save-error", self.__save_error_cb)
		editor.session_bus.add_signal_receiver(self.__saved_file_cb,
						signal_name="saved_file",
						dbus_interface=save_dbus_service)
		editor.session_bus.add_signal_receiver(self.__error_cb,
						signal_name="error",
						dbus_interface=save_dbus_service)
		editor.session_bus.add_signal_receiver(self.__is_ready_cb,
						signal_name="is_ready",
						dbus_interface=save_dbus_service)
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__precompile_methods, priority=500)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__termination_id = editor.register_object()
		self.__encoding_manager = self.__editor.get_encoding_manager()
		self.__processor = None
		self.__error_flag = False
		self.__should_rename = False
		self.__can_quit = False
		self.__is_saving = False
		self.__save_timer = None
		self.__queue_flag = False
		self.__toggle_readonly = False
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		self.__signal_id_4 = self.__signal_id_5 = self.__signal_id_6 = None
		self.__signal_id_7 = self.__signal_id_8 = self.__signal_id_9 = None
		self.__signal_id_10 = None
		from collections import deque
		self.__queue = deque([])
		return

########################################################################
#
#                           Public API
#
########################################################################

	def save_file(self, encoding="utf8", is_closing=False):
		from Exceptions import DoNothingError
		try:
			self.__determine_action(is_closing)
			from gobject import idle_add, PRIORITY_LOW
			idle_add(self.__save_file, encoding, priority=500)
		except DoNothingError:
			pass
		return False

########################################################################
#
#                       Helper Methods
#
########################################################################

	def __save_file(self, encoding):
		try:
			if self.__is_saving: raise ValueError
			self.__encoding = "utf-8" if encoding is None else encoding
			self.__editor.emit("saving-document", self.__editor.uri)
			from gobject import idle_add
			idle_add(self.__begin_saving, priority=9999)
		except ValueError:
			print "Deffering save process"
			self.__queue_flag = True
			self.__queue.append(1)
		except AttributeError:
			error_message = "Can't find save processor"
			self.__error(error_message)
		return False

	def __begin_saving(self):
		processor = self.__get_save_processor()
		processor.process(self.__editor.id, self.__editor.get_text(),
				self.__editor.uri, self.__encoding,
				dbus_interface=save_dbus_service,
				reply_handler=self.__reply_handler_cb,
				error_handler=self.__error_handler_cb)
		return False

	def __get_save_processor(self):
		if self.__processor: return self.__processor
		self.__processor = self.__editor.get_save_processor()
		return self.__processor

	def __determine_action(self, is_closing):
		if self.__editor.uri: return
		if is_closing:
			# Create a new file and save it if the text editor's buffer
			# contains a document but there is no document to save.
			self.__can_quit = True
			self.__editor.create_new_file()
			from gobject import idle_add, PRIORITY_LOW
			idle_add(self.save_file, priority=PRIORITY_LOW)
		else:
			# Show the save dialog if the text editor's buffer is empty and
			# there is no document to save.
			self.__editor.trigger("show_save_dialog")
		from Exceptions import DoNothingError
		raise DoNothingError
		return

	def __error(self, message):
		from internationalization import msg0477, msg0468
		title = msg0477 % (self.__editor.uri)
		message_id = self.__editor.feedback.set_modal_message(msg0468, "error")
		self.__editor.show_error_message(message, title, self.__editor.window)
		self.__editor.emit("save-error", str(self.__editor.uri))
		self.__editor.feedback.unset_modal_message(message_id)
		return False

	def __save_file_timeout_cb(self):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.save_file, self.__editor.encoding, False, priority=1000)
		return False

	def __remove_save_timer(self):
		try:
			from gobject import source_remove
			source_remove(self.__save_timer)
		except:
			pass
		return

	def __destroy(self):
		self.__remove_save_timer()
		try:
			processor = self.__get_save_processor()
			processor.update(self.__editor.id, dbus_interface=save_dbus_service,
				reply_handler=self.__reply_handler_cb,
				error_handler=self.__error_handler_cb)
		except:
			pass
		self.__editor.session_bus.remove_signal_receiver(self.__saved_file_cb,
						signal_name="saved_file",
						dbus_interface=save_dbus_service)
		self.__editor.session_bus.remove_signal_receiver(self.__error_cb,
						signal_name="error",
						dbus_interface=save_dbus_service)
		self.__editor.session_bus.remove_signal_receiver(self.__is_ready_cb,
						signal_name="is_ready",
						dbus_interface=save_dbus_service)
		self.__encoding_manager.destroy()
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
		try:
			from psyco import bind
			bind(self.save_file)
			bind(self.__save_file)
			bind(self.__remove_save_timer)
		except ImportError:
			pass
		except:
			pass
		return False

	def __check_queue(self):
		try:
			self.__queue.pop()
			from gobject import idle_add, PRIORITY_LOW
			idle_add(self.__begin_saving, priority=1000)
		except IndexError:
			self.__is_saving = False
			self.__toggle_readonly_mode()
			self.__emit_save_signal()
			if self.__can_quit: self.__destroy()
		return False

	def __toggle_readonly_mode(self):
		if not (self.__toggle_readonly): return
		self.__editor.trigger("toggle_readonly")
		self.__toggle_readonly = False
		return False

	def __emit_save_signal(self):
		emit = lambda signal: self.__editor.emit(signal, self.__editor.uri, self.__encoding)
		emit("renamed-document") if self.__should_rename else emit("saved-document")
		self.__should_rename = False
		return False

########################################################################
#
#                       Signal and Event Handlers
#
########################################################################

	def __close_document_cb(self, *args):
		self.__can_quit = True
		self.__remove_save_timer()
		if self.__error_flag: return self.__destroy()
		if not (self.__editor.file_is_saved):
			from gobject import idle_add, PRIORITY_LOW
			idle_add(self.save_file, self.__editor.encoding, True)
		else:
			self.__destroy()
		return True

	def __close_document_no_save_cb(self, *args):
		self.__remove_save_timer()
		self.__destroy()
		return True

	def __checking_document_cb(self, *args):
		self.__editor.textbuffer.handler_block(self.__signal_id_7)
		return True

	def __loaded_document_cb(self, *args):
		self.__editor.textbuffer.handler_unblock(self.__signal_id_7)
		return True

	def __load_error_cb(self, editor, uri):
		editor.textbuffer.handler_unblock(self.__signal_id_7)
		return True

	def __save_document_cb(self, editor, encoding):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.save_file, encoding, False, priority=500)
		return True

	def __saving_document_cb(self, *args):
		self.__is_saving = True
		return True

	def __saved_document_cb(self, *args):
		self.__error_flag = False
		self.__remove_save_timer()
		return True

	def __save_error_cb(self, *args):
		self.__is_saving = False
		self.__error_flag = True
		self.__queue_flag = False
		self.__remove_save_timer()
		self.__queue.clear()
		return True

	def __modified_changed_cb(self, textbuffer):
		if textbuffer.get_modified() is False: return False
		self.__editor.emit("modified-document")
		if self.__editor.uri is None: return False
		from gobject import timeout_add, PRIORITY_LOW
		self.__save_timer = timeout_add(SAVE_TIMER, self.__save_file_timeout_cb, priority=1000)
		return False

	def __reload_document_cb(self, *args):
		self.__remove_save_timer()
		return False

	def __rename_document_cb(self, editor, uri, encoding):
		if self.__editor.is_readonly: self.__toggle_readonly = True
		self.__should_rename = True
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.save_file, encoding, False, priority=500)
		return False

	def __is_ready_cb(self, *args):
		self.__processor = self.__editor.get_save_processor()
		return False

	def __saved_file_cb(self, editor_id):
		if (self.__editor.id != editor_id): return False
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__check_queue, priority=500)
		return False

	def __error_cb(self, editor_id, error_message, error_id):
		if (self.__editor.id != editor_id): return False
		error_message = error_message + " " + str(error_id)
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__error, error_message, priority=PRIORITY_LOW)
		return False

	def __reply_handler_cb(self, *args):
		return None

	def __error_handler_cb(self, error):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__error, error, priority=PRIORITY_LOW)
		return None
