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

"""
Bookmark actions for the text editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE

class BookmarkTrigger(GObject):
	"""
	This class implements an object that allows users of the text editor
	to perform bookmark operations via the text editor's standard
	shortcut keys.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize the bookmark trigger object.

		@param self: Reference to the BookmarkTrigger instance.
		@type self: A BookmarkTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		self.__create_bookmark_triggers()
		self.__bookmark_document()
		self.__signal_id_1 = self.__trigger_1.connect("activate", self.__toggle_bookmark_cb)
		self.__signal_id_2 = self.__trigger_2.connect("activate", self.__toggle_bookmark_cb)
		self.__signal_id_3 = self.__trigger_3.connect("activate", self.__remove_all_bookmarks_cb)
		self.__signal_id_4 = self.__trigger_4.connect("activate", self.__next_bookmark_cb)
		self.__signal_id_5 = self.__trigger_5.connect("activate", self.__previous_bookmark_cb)
		self.__signal_id_6 = self.__trigger_6.connect("activate", self.__first_bookmark_cb)
		self.__signal_id_7 = self.__trigger_7.connect("activate", self.__last_bookmark_cb)
		self.__signal_id_8 = self.editor.connect_after("loaded-document", self.__trigger_loaded_document_cb)
		self.__signal_id_9 = self.connect("destroy", self.__trigger_destroy_cb)
		self.__signal_id_10 = self.editor.textview.connect_after("populate-popup", self.__popup_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the bookmark triggers data attributes.

		@param self: Reference to the BookmarkTrigger instance.
		@type self: A BookmarkTrigger object.
		"""
		self.editor = self.__editor = editor
		self.__manager = None
		self.__trigger_1 = self.__trigger_2 = self.__trigger_3 = None
		self.__trigger_4 = self.__trigger_5 = self.__trigger_6 = None
		self.__trigger_7 = None
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		self.__signal_id_4 = self.__signal_id_5 = self.__signal_id_6 = None
		self.__signal_id_7 = self.__signal_id_8 = self.__signal_id_9 = None
		self.__signal_id_10 = None
#		self.__browser = None
		return

	def __create_bookmark_triggers(self):
		"""
		Create the bookmark triggers.

		@param self: Reference to the BookmarkTrigger instance.
		@type self: A BookmarkTrigger object.
		"""
		# Trigger to bookmark a line.
		self.__trigger_1 = self.__editor.create_trigger("bookmark_line", "ctrl - d")
		self.editor.add_trigger(self.__trigger_1)

		self.__trigger_2 = self.__editor.create_trigger("remove_bookmark")
		self.editor.add_trigger(self.__trigger_2)

		# Trigger to remove all bookmarks from the document.
		self.__trigger_3 = self.__editor.create_trigger("remove_all_bookmarks", "alt - ctrl - Delete")
		self.editor.add_trigger(self.__trigger_3)

		# Trigger to move to the next bookmark in the document.
		self.__trigger_4 = self.__editor.create_trigger("next_bookmark", "alt - Right")
		self.editor.add_trigger(self.__trigger_4)

		# Trigger to move to the next bookmark in the document.
		self.__trigger_5 = self.__editor.create_trigger("previous_bookmark", "alt - Left")
		self.editor.add_trigger(self.__trigger_5)

		# Trigger to move to the first bookmark in the document
		self.__trigger_6 = self.__editor.create_trigger("first_bookmark", "alt - ctrl - Home")
		self.editor.add_trigger(self.__trigger_6)

		# Trigger to move to the first bookmark in the document
		self.__trigger_7 = self.__editor.create_trigger("last_bookmark", "alt - ctrl - End")
		self.editor.add_trigger(self.__trigger_7)
		return

	def __toggle_bookmark_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		This function toggles bookmarks on a line in the text editor's
		buffer.

		@param self: Reference to the BookmarkTrigger instance.
		@type self: A BookmarkTrigger object.

		@param trigger: An action to bookmark a line in the text editor's
			buffer.
		@type trigger: A Trigger object.
		"""
		try:
			self.__manager.is_initialized
		except AttributeError:
			from Manager import BookmarkManager
			self.__manager = BookmarkManager(self.editor)
		line = self.__editor.get_cursor_line()
		if self.__manager.line_is_bookmarked(line):
			self.__manager.remove_bookmark_on_line(line)
			from i18n import msg0001
			message = msg0001 % (line+1)
			self.editor.feedback.update_status_message(message, "succeed")
			return
		self.__manager.bookmark_line(line)
		self.__editor.move_view_to_cursor()
		from i18n import msg0002
		message = msg0002 % (line+1)
		self.editor.feedback.update_status_message(message, "succeed")
		return

	def __remove_all_bookmarks_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the BookmarkTrigger instance.
		@type self: A BookmarkTrigger object.

		@param trigger: Remove all bookmarks from the buffer.
		@type trigger: A Trigger object.
		"""
		try:
			self.__manager.is_initialized
		except AttributeError:
			from Manager import BookmarkManager
			self.__manager = BookmarkManager(self.editor)
		if not self.__manager.get_bookmarked_lines():
			from i18n import msg0003
			self.editor.feedback.update_status_message(msg0003, "fail")
			return
		self.__manager.remove_all_bookmarks()
		from i18n import msg0004
		self.editor.feedback.update_status_message(msg0004, "succeed")
		return

	def __next_bookmark_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the BookmarkTrigger instance.
		@type self: A BookmarkTrigger object.

		@param trigger: Move to next bookmark.
		@type trigger: A Trigger object.
		"""
		try:
			self.__manager.is_initialized
		except AttributeError:
			from Manager import BookmarkManager
			self.__manager = BookmarkManager(self.editor)
		if not self.__manager.get_bookmarked_lines():
			from i18n import msg0003
			self.editor.feedback.update_status_message(msg0003, "fail")
			return
		result = self.__manager.move_to_next_bookmark()
		if result:
			from i18n import msg0005
			line = self.__editor.get_cursor_line()
			message = msg0005 % (line+1)
			self.editor.feedback.update_status_message(message, "succeed")
		else:
			from i18n import msg0006
			self.editor.feedback.update_status_message(msg0006, "fail")
		return

	def __previous_bookmark_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the BookmarkTrigger instance.
		@type self: A BookmarkTrigger object.

		@param trigger: Move to previous bookmark in the buffer.
		@type trigger: A Trigger object.
		"""
		try:
			self.__manager.is_initialized
		except AttributeError:
			from Manager import BookmarkManager
			self.__manager = BookmarkManager(self.editor)
		if not self.__manager.get_bookmarked_lines():
			from i18n import msg0003
			self.editor.feedback.update_status_message(msg0003, "fail")
			return
		result = self.__manager.move_to_previous_bookmark()
		if result:
			from i18n import msg0005
			line = self.__editor.get_cursor_line()
			message = msg0005 % (line+1)
			self.editor.feedback.update_status_message(message, "succeed")
		else:
			from i18n import msg0007
			self.editor.feedback.update_status_message(msg0007, "fail")
		return

	def __first_bookmark_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the BookmarkTrigger instance.
		@type self: A BookmarkTrigger object.

		@param trigger: Move to first document in the buffer.
		@type trigger: A Trigger object.
		"""
		try:
			self.__manager.is_initialized
		except AttributeError:
			from Manager import BookmarkManager
			self.__manager = BookmarkManager(self.editor)
		if not self.__manager.get_bookmarked_lines():
			from i18n import msg0003
			self.editor.feedback.update_status_message(msg0003, "fail")
			return
		if len(self.__manager.get_bookmarked_lines()) == 1:
			from i18n import msg0008
			self.editor.feedback.update_status_message(msg0008, "fail")
			return
		self.__manager.move_to_first_bookmark()
		from i18n import msg0009
		self.editor.feedback.update_status_message(msg0009, "succeed")
		return

	def __last_bookmark_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the BookmarkTrigger instance.
		@type self: A BookmarkTrigger object.

		@param trigger: Move to the last bookmark in the buffer.
		@type trigger: A Trigger object.
		"""
		try:
			self.__manager.is_initialized
		except AttributeError:
			from Manager import BookmarkManager
			self.__manager = BookmarkManager(self.editor)
		if not self.__manager.get_bookmarked_lines():
			from i18n import msg0003
			self.editor.feedback.update_status_message(msg0003, "fail")
			return
		if len(self.__manager.get_bookmarked_lines()) == 1:
			from i18n import msg0010
			self.editor.feedback.update_status_message(msg0010, "fail")
			return
		self.__manager.move_to_last_bookmark()
		from i18n import msg0011
		self.editor.feedback.update_status_message(msg0011, "succeed")
		return

	def __show_bookmark_browser_cb(self, trigger):
		"""
		Handles callback when the "activate" signal is emitted.

		@param self: Reference to the BookmarkTrigger instance.
		@type self: A BookmarkTrigger object.

		@param trigger: An action to show the bookmark browser.
		@type trigger: A Trigger object.
		"""
		try:
			self.__manager.is_initialized
		except AttributeError:
			from Manager import BookmarkManager
			self.__manager = BookmarkManager(self.editor)

		if not self.__manager.get_bookmarked_lines():
			from i18n import msg0428
			self.editor.feedback.update_status_message(msg0428, "fail")
			return
		try:
			self.__browser.show_dialog()
		except AttributeError:
			from bookmarkbrowser import BookmarkBrowser
			self.__browser = BookmarkBrowser(self.__manager)
			self.__browser.show_dialog()
		return

	def __trigger_loaded_document_cb(self, editor, uri):
		"""
		Handles callback when the "loaded-document" signal is emitted.

		@param self: Reference to the BookmarkTrigger instance.
		@type self: A BookmarkTrigger object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		from gobject import idle_add
		idle_add(self.__bookmark_document)
		return

	def __bookmark_document(self):
		"""
		Bookmark a document if it has an entry in the bookmark database.

		@param self: Reference to the BookmarkTrigger instance.
		@type self: A BookmarkTrigger object.
		"""
		if self.editor.contains_document is False or self.editor.uri is None: return False
		from BookmarkMetadata import get_bookmarks_from_database
		bookmarked_lines = get_bookmarks_from_database(str(self.editor.uri))
		if bookmarked_lines is None: return False
		try:
			self.__manager.is_initialized
		except AttributeError:
			from Manager import BookmarkManager
			self.__manager = BookmarkManager(self.editor)
		map(self.__manager.bookmark_line, bookmarked_lines)
		return False

	def __trigger_destroy_cb(self, trigger):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the BookmarkTrigger instance.
		@type self: A BookmarkTrigger object.

		@param trigger: Reference to the BookmarkTrigger instance.
		@type trigger: A BookmarkTrigger object.
		"""
		# Remove all triggers.
		triggers = (self.__trigger_1, self.__trigger_2, self.__trigger_3, self.__trigger_4,
			self.__trigger_5, self.__trigger_6, self.__trigger_7)
		self.editor.remove_triggers(triggers)
		# Disconnect all signals.
		self.__editor.disconnect_signal(self.__signal_id_1, self.__trigger_1)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__trigger_2)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__trigger_3)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__trigger_4)
		self.__editor.disconnect_signal(self.__signal_id_5, self.__trigger_5)
		self.__editor.disconnect_signal(self.__signal_id_6, self.__trigger_6)
		self.__editor.disconnect_signal(self.__signal_id_7, self.__trigger_7)
		self.__editor.disconnect_signal(self.__signal_id_8, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_9, self)
		self.__editor.disconnect_signal(self.__signal_id_10, self.__editor.textview)
		# Destroy bookmark manager.
		if self.__manager: self.__manager.emit("destroy")
		del self
		self = None
		return

	def __popup_cb(self, textview, menu):
		"""
		Handles callback when the "populate-popup" signal is emitted.

		@param self: Reference to the SelectionTrigger instance.
		@type self: An SelectionTrigger object.

		@param textview: Reference to the editor's textview.
		@type textview: A ScribesTextView object.

		@param menu: Reference to the editor's popup menu.
		@type menu: A gtk.Menu object.
		"""
		from PopupMenuItem import BookmarkPopupMenuItem
		menu.prepend(BookmarkPopupMenuItem(self.editor, self.__manager))
		menu.show_all()
		return False
