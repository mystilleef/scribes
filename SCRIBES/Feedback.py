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
This module documents a class that sends messages to the text editor's
statusbar.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class FeedbackManager(object):
	"""
	This class creates an instance that manages messages sent to the
	text editor's statusbar.
	"""

	def __init__(self, editor):
		"""
		Initialize object.

		@param self: Reference to the FeedbackManager instance.
		@type self: A FeedbackManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(editor)
		self.__signal_id_1 = editor.connect("close-document", self.__close_document_cb)
		self.__signal_id_2 = editor.connect("close-document-no-save", self.__close_document_cb)
		self.__signal_id_3 = editor.connect("checking-document", self.__checking_document_cb)
		self.__signal_id_4 = editor.connect("loaded-document", self.__loaded_document_cb)
		self.__signal_id_5 = editor.connect("load-error", self.__load_error_cb)
		self.__signal_id_6 = editor.connect("renamed-document", self.__renamed_document_cb)
		self.__signal_id_7 = editor.connect("saved-document", self.__saved_document_cb)
		self.__signal_id_8 = editor.connect("enable-readonly", self.__enable_readonly_cb)
		self.__signal_id_9 = editor.connect("disable-readonly", self.__disable_readonly_cb)
		self.__signal_id_10 = editor.connect("not-yet-implemented", self.__not_yet_implemented_cb)
		self.__signal_id_11 = editor.connect("modified-document", self.__changed_cb)
		self.__signal_id_12 = editor.connect("gui-created", self.__gui_created_cb)
		self.__signal_id_13 = editor.connect("reload-document", self.__reload_document_cb)

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the FeedbackManager instance.
		@type self: A FeedbackManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__registration_id = editor.register_object()
		self.__icon_dictionary = self.__create_feedback_icons()
		self.__spinner = editor.store.get_object("Spinner")
		self.__message_stack = []
		self.__message_id = None
		self.__filename = None
		self.__reset_timer = None
		self.__is_busy = False
		self.__default_message_is_set = False
		return

########################################################################
#
#						Public APIs
#
########################################################################

	def update_status_message(self, message=None, icon=None, time=3):
		"""
		Update the statusbar with feedback message and image.

		@param self: Reference to the FeedbackManager instance.
		@type self: A FeedbackManager object.

		@param message: Message to send to the statusbar.
		@type message: A String object.

		@param icon: Image to place in the statusbar.
		@type icon: A gtk.STOCK object.

		@param time: How long to display feedback message in seconds.
		@type time: An Integer object.

		@return: False to call this function once.
		@rtype: A Boolean object.
		"""
		self.__is_busy = True
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__set_message, message, priority=PRIORITY_LOW)
		idle_add(self.__set_icon, icon, priority=PRIORITY_LOW)
		idle_add(self.__reset, time, priority=PRIORITY_LOW)
		idle_add(self.__beep, icon, priority=PRIORITY_LOW)
		self.__default_message_is_set = False
		return False

	def set_modal_message(self, message=None, icon=None):
		"""
		Add feedback data to message stack.

		@param message: Feedback data representing a message.
		@type message: A String object.

		@param icon: Feedback data representing an image.
		@type icon: A String object.

		@return: A unique number associated with a set of feedback data.
		@rtype: An Integer object.
		"""
		message_id = self.__editor.generate_random_number(self.__message_stack)
		self.__message_stack.append((message, icon, message_id))
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__set_message, message, priority=PRIORITY_LOW)
		idle_add(self.__set_icon, icon, priority=PRIORITY_LOW)
		self.__default_message_is_set = False
		return message_id

	def unset_modal_message(self, message_id, reset=True):
		"""
		Remove feedback data from message stack.

		@param self: Reference to the FeedbackManager instance.
		@type self: A FeedbackManager object.

		@param message_id: A unique number associated with feedback data.
		@type message_id: A Integer object.

		@param reset: If True reset the statusbar.
		@type reset: A Boolean object.

		@return: False to call this function once.
		@rtype: A Boolean object.
		"""
		try:
			from operator import truth
			for feedback in self.__message_stack:
				found = self.__remove_message_from_stack(message_id, feedback)
				if truth(found): break
			if truth(reset):
				from gobject import idle_add, PRIORITY_LOW
				idle_add(self.__reset_message, priority=PRIORITY_LOW)
		except RuntimeError:
			pass
		return False

	def start_spinner(self):
		"""
		Start spinning the feedback throbber.

		@param self: Reference to the FeedbackManager instance.
		@type self: A FeedbackManager object.
		"""
		self.__spinner.start()
		return False

	def stop_spinner(self):
		"""
		Stop spinning the feedback throbber.

		@param self: Reference to the FeedbackManager instance.
		@type self: A FeedbackManager object.
		"""
		self.__spinner.stop()
		return False

	def start_busy_cursor(self):
		"""
		Show the busy cursor.

		@param self: Reference to the FeedbackManager instance.
		@type self: A FeedbackManager object.
		"""
		from cursor import show_busy_textview_cursor
		show_busy_textview_cursor(self.__editor.textview)
		return False

	def stop_busy_cursor(self):
		"""
		Stop showing busy cursor.

		@param self: Reference to the FeedbackManager instance.
		@type self: A FeedbackManager object.
		"""
		from cursor import show_textview_cursor
		show_textview_cursor(self.__editor.textview)
		return False

########################################################################
#
#						Helper Methods
#
########################################################################

	def __set_message(self, message):
		"""
		Update the statusbar with message.

		@param self: Reference to the FeedbackManager instance.
		@type self: A FeedbackManager object.

		@param message: A message to push to the statusbar.
		@type message: A String object.
		"""
		try:
			from operator import not_
			if not_(message): return False
			statusbar = self.__editor.statusone
			statusbar.pop(statusbar.context_id)
			context_id = statusbar.get_context_id(message)
			statusbar.push(context_id, message)
		except AttributeError:
			self.__destroy()
		except RuntimeError:
			pass
		return False

	def __set_icon(self, icon):
		"""
		Update the statusbar with icon.

		@param self: Reference to the FeedbackManager instance.
		@type self: A FeedbackManager object.

		@param message: An icon to place in the statusbar.
		@type message: A gtk.STOCK object.
		"""
		try:
			from operator import not_
			if not_(icon): return False
			image = self.__editor.status_image
			frame = self.__editor.status_image_frame
			image.clear()
			from gtk import ICON_SIZE_MENU
			image.set_from_stock(self.__icon_dictionary[icon], ICON_SIZE_MENU)
			image.show_all()
			frame.show()
		except KeyError:
			pass
		except AttributeError:
			self.__destroy()
		except RuntimeError:
			pass
		return False

	def __remove_message(self):
		"""
		Remove message from statusbar.

		@param self: Reference to the FeedbackManager instance.
		@type self: A FeedbackManager object.
		"""
		try:
			statusbar = self.__editor.statusone
			statusbar.pop(statusbar.context_id)
			statusbar.push(0, "")
		except AttributeError:
			self.__destroy()
		return False

	def __remove_icon(self):
		"""
		Remove image from statusbar.

		@param self: Reference to the FeedbackManager instance.
		@type self: A FeedbackManager object.
		"""
		try:
			self.__editor.status_image.clear()
			self.__editor.status_image_frame.hide_all()
		except AttributeError:
			self.__destroy()
		return False

	def __reset_message(self):
		"""
		Reset the message in the statusbar.

		@param self: Reference to the FeedbackManager instance.
		@type self: A FeedbackManager object.
		"""
		from operator import truth, not_, is_
		if truth(self.__message_stack) and not_(self.__editor.is_readonly):
			self.__set_message_from_stack()
		elif is_(self.__filename, None):
			self.__remove_message()
			self.__remove_icon()
		else:
			self.__set_default_message()
			self.__set_default_icon()
		self.__is_busy = False
		self.__default_message_is_set = True
		return False

	def __set_default_message(self):
		"""
		Determine default message to display in the statusbar.

		@param self: Reference to the FeedbackManager instance.
		@type self: A FeedbackManager object.
		"""
		from operator import truth
		from internationalization import msg0044, msg0045
		if truth(self.__editor.is_readonly):
			message = msg0044 % self.__filename
			self.__set_message(message)
		else:
			message = msg0045 % self.__filename
			self.__set_message(message)
		return False

	def __set_default_icon(self):
		"""
		Determine default image to show in the statusbar.

		@param self: Reference to the FeedbackManager instance.
		@type self: A FeedbackManager object.
		"""
		from operator import truth
		if truth(self.__editor.is_readonly):
			self.__set_icon("readonly")
		elif truth(self.__editor.file_is_saved):
			self.__set_icon("new")
		else:
			self.__set_icon("edit")
		return False

	def __set_message_from_stack(self):
		"""
		Determine feedback to show in the statusbar from the message stack.

		@param self: Reference to the FeedbackManager instance.
		@type self: A FeedbackManager object.
		"""
		message = self.__message_stack[-1][0]
		icon = self.__message_stack[-1][1]
		self.__set_message(message)
		self.__set_icon(icon)
		return False

	def __remove_message_from_stack(self, message_id, feedback):
		"""
		Remove feedback data from message stack.

		@param message_id: A unique number associated with feedback data.
		@type message_id: An Integer object.

		@param feedback: Data representing feedback information.
		@type feedback: A Tuple object.

		@return: True if feedback data is found in message stack.
		@rtype: A Boolean object.
		"""
		from operator import contains
		if contains(feedback, message_id):
			self.__message_stack.remove(feedback)
			return True
		return False

	def __reset(self, time):
		"""
		Reset the statusbar with default message.

		@param self: Reference to the FeedbackManager instance.
		@type self: A FeedbackManager object.

		@param time: How long to reset the statusbar.
		@type time: An Integer object.
		"""
		from operator import is_
		if is_(time, None): time = 3
		time *= 1000
		from gobject import timeout_add
		self.__remove_timer()
		self.__reset_timer = timeout_add(time, self.__reset_message)
		return False

	def __remove_timer(self):
		"""
		Remove timer of timeout_add functions to prevent multiple calls.

		@param self: Reference to the FeedbackManager instance.
		@type self: A FeedbackManager object.
		"""
		from gobject import source_remove
		try:
			source_remove(self.__reset_timer)
		except:
			pass
		return False

	def __beep(self, icon):
		"""
		Beep on failed, error or warning messages.

		@param self: Reference to the FeedbackManager instance.
		@type self: A FeedbackManager object.

		@param icon: A string representing an image.
		@type icon: A String object.
		"""
		from operator import contains
		if contains(("fail", "no", "error", "warning"), icon):
			from gtk.gdk import beep
			beep()
		return False

	def __set_filename_from_uri(self, uri):
		"""
		Set filename to show in the statusbar.

		@param self: Reference to the FeedbackManager instance.
		@type self: A FeedbackManager object.

		@param uri: A string representing a file.
		@type uri: A String object.
		"""
		if uri.startswith("file:///"):
			from gnomevfs import get_local_path_from_uri
			local_path = get_local_path_from_uri(uri)
			if local_path.startswith(self.__editor.home_folder):
				self.__filename = local_path.replace(self.__editor.home_folder, "~")
			else:
				self.__filename = local_path
		else:
			self.__filename = uri
		return False

	def __create_feedback_icons(self):
		"""
		Generate feedback images for the statusbar.

		@param self: Reference to the FeedbackManager instance.
		@type self: A FeedbackManager object.

		@return: A dictionary of stock icons.
		@rtype: A Dictionary object.
		"""
		from gtk import STOCK_YES, STOCK_NO, STOCK_OPEN, STOCK_EDIT, STOCK_SAVE
		from gtk import STOCK_SAVE_AS, STOCK_NEW, STOCK_PRINT, STOCK_UNDO
		from gtk import STOCK_REDO, STOCK_JUMP_TO, STOCK_FIND
		from gtk import STOCK_FIND_AND_REPLACE, STOCK_PREFERENCES
		from gtk import STOCK_DIALOG_WARNING, STOCK_DIALOG_AUTHENTICATION
		from gtk import STOCK_DIALOG_ERROR, STOCK_COPY, STOCK_CUT, STOCK_PASTE
		from gtk import STOCK_SPELL_CHECK, STOCK_HELP, STOCK_EXECUTE
		from gtk import STOCK_DIALOG_INFO, STOCK_ABOUT, STOCK_SELECT_COLOR
		from gtk import STOCK_STOP
		icon_dictionary = {
			"succeed": STOCK_YES,
			"suceed": STOCK_YES,
			"fail": STOCK_NO,
			"no": STOCK_NO,
			"yes": STOCK_YES,
			"open": STOCK_OPEN,
			"edit": STOCK_EDIT,
			"save": STOCK_SAVE,
			"saveas": STOCK_SAVE_AS,
			"new": STOCK_NEW,
			"print": STOCK_PRINT,
			"undo": STOCK_UNDO,
			"redo": STOCK_REDO,
			"goto": STOCK_JUMP_TO,
			"find": STOCK_FIND,
			"replace": STOCK_FIND_AND_REPLACE,
			"preferences": STOCK_PREFERENCES,
			"warning": STOCK_DIALOG_WARNING,
			"readonly": STOCK_DIALOG_AUTHENTICATION,
			"error": STOCK_DIALOG_ERROR,
			"copy" : STOCK_COPY,
			"cut": STOCK_CUT,
			"paste": STOCK_PASTE,
			"spell": STOCK_SPELL_CHECK,
			"help": STOCK_HELP,
			"run": STOCK_EXECUTE,
			"info": STOCK_DIALOG_INFO,
			"about": STOCK_ABOUT,
			"color": STOCK_SELECT_COLOR,
			"stop": STOCK_STOP,
		}
		return icon_dictionary

	def __destroy(self):
		"""
		Destroy instance of this class.

		@param self: Reference to the Store instance.
		@type self: A Store object.
		"""
		self.__remove_timer()
		# Disconnect signals.
		self.__editor.disconnect_signal(self.__signal_id_1, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_5, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_6, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_7, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_8, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_9, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_10, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_11, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_12, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_13, self.__editor)
		self.__icon_dictionary.clear()
		# Unregister object so that editor can quit.
		self.__spinner.destroy_object()
		self.__editor.unregister_object(self.__registration_id)
		# Delete data attributes.
		del self
		self = None
		return

########################################################################
#
#					Event and Signal Handlers
#
########################################################################

	def __close_document_cb(self, editor):
		"""
		Handles callback when the "close-document" signal is emitted.

		This function destroys instance of this class.

		@param self: Reference to the FeedbackManager instance.
		@type self: A FeedbackManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__destroy()
		return

	def __checking_document_cb(self, editor, uri):
		"""
		Handles callback when the "checking-document" signal is emitted.

		@param self: Reference to the FeedbackManager instance.
		@type self: A FeedbackManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param uri: A string representing a file.
		@type uri: A String object.
		"""
		self.__set_filename_from_uri(uri)
		self.start_spinner()
		self.start_busy_cursor()
		from internationalization import msg0032
		self.__message_id = self.set_modal_message(msg0032, "run")
		return

	def __loaded_document_cb(self, editor, uri):
		"""
		Handles callback when the "loaded-document" signal is emitted.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param self: Reference to the FeedbackManager instance.
		@type self: A FeedbackManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param uri: A string representing a file.
		@type uri: A String object.
		"""
		from internationalization import msg0030
		message = msg0030 % self.__filename
		self.unset_modal_message(self.__message_id, False)
		self.update_status_message(message, "open")
		self.stop_spinner()
		self.stop_busy_cursor()
		return

	def __load_error_cb(self, editor, uri):
		"""
		Handles callback when the "load-error" signal is emitted.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param self: Reference to the FeedbackManager instance.
		@type self: A FeedbackManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param uri: A string representing a file.
		@type uri: A String object.
		"""
		self.__filename = None
		self.stop_spinner()
		self.stop_busy_cursor()
		self.unset_modal_message(self.__message_id)
		return

	def __renamed_document_cb(self, editor, uri):
		"""
		Handles callback when the "renamed-document" signal is emitted.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param self: Reference to the FeedbackManager instance.
		@type self: A FeedbackManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param uri: A string representing a file.
		@type uri: A String object.
		"""
		self.__set_filename_from_uri(uri)
		from internationalization import msg0085
		message = msg0085 % self.__filename
		self.update_status_message(message, "save", 5)
		return

	def __reload_document_cb(self, *args):
		from internationalization import msg0489
		message = msg0489 % self.__filename
		self.update_status_message(message, "run", 15)
		return

	def __saved_document_cb(self, editor, uri):
		"""
		Handles callback when the "saved-document" signal is emitted.

		@param self: Reference to the FeedbackManager instance.
		@type self: A FeedbackManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param uri: A string representing a file.
		@type uri: A String object.
		"""
		from operator import truth, not_
		if self.__is_busy: return
		if not_(self.__default_message_is_set): return
		from internationalization import msg0085
		message = msg0085 % self.__filename
		self.update_status_message(message, "save", 5)
		return

	def __enable_readonly_cb(self, editor):
		"""
		Handles callback when the "enable-readonly" signal is emitted.

		@param self: Reference to the FeedbackManager instance.
		@type self: A FeedbackManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		from internationalization import msg0322
		self.update_status_message(msg0322, "suceed")
		return

	def __disable_readonly_cb(self, editor):
		"""
		Handles callback when the "disable-readonly" signal is emitted.

		@param self: Reference to the FeedbackManager instance.
		@type self: A FeedbackManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		from internationalization import msg0324
		self.update_status_message(msg0324, "suceed")
		return

	def __not_yet_implemented_cb(self, editor):
		"""
		Handles callback when the "not-yet-implemented" signal is emitted.

		@param self: Reference to the FeedbackManager instance.
		@type self: A FeedbackManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		message = "Not yet implemented"
		self.update_status_message(message, "warning")
		return

	def __changed_cb(self, *args):
		"""
		Handles callback when the "changed" signal is emitted.

		@param self: Reference to the FeedbackManager instance.
		@type self: A FeedbackManager object.

		@param args: Unimportant arguments.
		@type args: A Tuple object.
		"""
		from operator import not_, ne, is_
		if is_(self.__filename, None): return False
		if not_(self.__default_message_is_set): return False
		from gtk import STOCK_EDIT
		if ne(self.__editor.status_image.get_stock()[0], STOCK_EDIT): self.__set_icon("edit")
		return False

	def __gui_created_cb(self, *args):
		self.__remove_message()
		self.__remove_icon()
		return
