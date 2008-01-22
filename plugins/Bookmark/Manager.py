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
This module documents a class that performs bookmark operations for the
text editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE

class BookmarkManager(GObject):
	"""
	This class creates an object that implements bookmark operations for
	the text editor. The object is created during the initialization
	process of the text editor. In particular, it is created by the
	text editor's view object to run on a separate thread for the entire
	duration of the text editor's life-cycle. Thus, third party modules
	should never create an instance of this class. In the future, an
	interface will be provided for third party modules to have access to
	the manager.
	"""

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize the manager object.

		@param self: Reference to the BookmarkManager instance.
		@type self: A BookmarkManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		self.__store_id = self.editor.add_object("BookmarkManager", self)
		self.__signal_id_1 = self.connect("destroy", self.__manager_destroy_cb)
		self.__signal_id_2 = self.editor.connect_after("saved-document", self.__manager_saved_document_cb)
		self.__signal_id_3 = self.textbuffer.connect("mark-deleted", self.__manager_mark_deleted_cb)

	def __init_attributes(self, editor):
		"""
		Initialize the manager's data attributes.

		@param self: Reference to the BookmarkManager instance.
		@type self: A BookmarkManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.editor = self.__editor = editor
		self.textbuffer = editor.textbuffer
		self.bookmark_list = []
		self.bookmark_image = self.__create_bookmark_image()
		self.textview = editor.textview
		self.is_initialized = True
		self.__signal_id_1 = None
		self.__signal_id_2 = None
		self.__signal_id_3 = None
		self.__store_id = None
		return

	def line_is_bookmarked(self, line):
		"""
		Return true if a particular line is bookmarked.

		@param self: Reference to the BookmarkManager instance.
		@type self: A BookmarkManager object.

		@param line: A line in a the text editor's buffer.
		@type line: An Integer object.

		@return: True if the line is bookmarked.
		@rtype: A Boolean object.
		"""
		markers = self.__get_bookmark_on_line(line)
		if markers: return True
		return False

	def bookmark_line(self, line):
		"""
		Bookmark a line in the text editor's buffer.

		@param self: Reference to the BookmarkManager instance.
		@type self: A BookmarkManager object.

		@param line: A line to be bookmarked.
		@type line: An Integer object.
		"""
		iterator = self.textbuffer.get_iter_at_line(line)
		marker = self.textbuffer.create_marker(None, "scribes_bookmark", iterator)
		self.bookmark_list.append(marker)
		self.textview.set_show_line_markers(True)
		self.textview.set_marker_pixbuf("scribes_bookmark", self.bookmark_image)
		from gobject import idle_add
		idle_add(self.__update_bookmark_database)
		return

	def remove_bookmark_on_line(self, line):
		"""
		Remove the bookmark on a particular line in the text editor's
		buffer.

		@param self: Reference to the BookmarkManager instance.
		@type self: A BookmarkManager object.

		@param line: The line to remove a bookmark from.
		@type line: An Integer object.
		"""
		markers = self.__get_bookmark_on_line(line)
		for marker in markers:
			if marker.get_marker_type() == "scribes_bookmark":
				if marker.get_deleted() is False:
					self.textbuffer.delete_marker(marker)
		return

	def remove_all_bookmarks(self):
		"""
		Remove all bookmarks in a buffer.

		@param self: Reference to the BookmarkManager instance.
		@type self: A BookmarkManager object.
		"""
		lines = self.get_bookmarked_lines()
		for line in lines:
			self.remove_bookmark_on_line(line)
		self.textview.set_show_line_markers(False)
		return

	def get_bookmarked_lines(self):
		"""
		Return a list of bookmarked lines in a buffer.

		@param self: Reference to the BookmarkManager instance.
		@type self: A BookmarkManager object.

		@return: A list of bookmarked lines.
		@rtype: A List object.
		"""
		begin_position, end_position = self.textbuffer.get_bounds()
		markers = self.textbuffer.get_markers_in_region(begin_position, end_position)
		bookmarked_lines = []
		for marker in markers:
			if marker.get_marker_type() == "scribes_bookmark":
				bookmarked_lines.append(marker.get_line())
		return bookmarked_lines

	def move_to_next_bookmark(self):
		"""
		Move the cursor to the next bookmarked line in the buffer.

		@param self: Reference to the BookmarkManager instance.
		@type self: A BookmarkManager object.
		"""
		cursor_line = self.__editor.get_cursor_line()
		bookmarked_lines = self.get_bookmarked_lines()
		if not len(bookmarked_lines): return False
		bookmarked_lines.sort()
		for line in bookmarked_lines:
			if line > cursor_line:
				iterator = self.textbuffer.get_iter_at_line(line)
				self.textbuffer.place_cursor(iterator)
				self.__editor.move_view_to_cursor()
				return True
		return False

	def move_to_previous_bookmark(self):
		"""
		Move the cursor to the previous bookmarked line in the buffer.

		@param self: Reference to the BookmarkManager instance.
		@type self: A BookmarkManager object.
		"""
		cursor_line = self.__editor.get_cursor_line()
		bookmarked_lines = self.get_bookmarked_lines()
		if not len(bookmarked_lines): return False
		bookmarked_lines.sort()
		bookmarked_lines.reverse()
		for line in bookmarked_lines:
			if line < cursor_line:
				iterator = self.textbuffer.get_iter_at_line(line)
				self.textbuffer.place_cursor(iterator)
				self.__editor.move_view_to_cursor()
				return True
		return False

	def move_to_first_bookmark(self):
		"""
		Move the cursor to the first bookmarked line in the buffer.

		@param self: Reference to the BookmarkManager instance.
		@type self: A BookmarkManager object.
		"""
		line = min(self.get_bookmarked_lines())
		iterator = self.textbuffer.get_iter_at_line(line)
		self.textbuffer.place_cursor(iterator)
		self.__editor.move_view_to_cursor()
		return

	def move_to_last_bookmark(self):
		"""
		Move the cursor to the last bookmarked line in the buffer.

		@param self: Reference to the BookmarkManager instance.
		@type self: A BookmarkManager object.
		"""
		line = max(self.get_bookmarked_lines())
		iterator = self.textbuffer.get_iter_at_line(line)
		self.textbuffer.place_cursor(iterator)
		self.__editor.move_view_to_cursor()
		return

	def __manager_mark_deleted_cb(self, textbuffer, textmark):
		"""
		Handles callback when the "mark-deleted" signal is emitted.

		@param self: Reference to the BookmarkManager instance.
		@type self: A BookmarkManager object.

		@param textbuffer: The text editor's buffer.
		@type textbuffer: A ScribesTextBuffer object.

		@param textmark: The mark that is being deleted.
		@type textmark: A gtksourceview.SourceMarker object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		if textmark.get_marker_type() == "scribes_bookmark":
			self.bookmark_list.remove(textmark)
			if not self.get_bookmarked_lines():
				self.textview.set_show_line_markers(False)
			from gobject import idle_add
			idle_add(self.__update_bookmark_database)
		return False

	def __manager_saved_document_cb(self, *args):
		"""
		Handles callback when the "saved-document" signal is emitted.

		@param self: Reference to the BookmarkManager instance.
		@type self: A BookmarkManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__update_bookmark_database, priority=PRIORITY_LOW)
		return

	def __manager_destroy_cb(self, manager):
		"""
		Handles callback when the "quit" signal is emitted.

		@param self: Reference to the BookmarkManager instance.
		@type self: A BookmarkManager object.

		@param manager: Reference to the BookmarkManager instance.
		@type manager: A BookmarkManager object.
		"""
		self.__update_bookmark_database()
		# Remove bookmark manager from global repository.
		if self.__store_id and self.editor.store: self.editor.remove_object("BookmarkManager", self.__store_id)
		# Disconnect signals.
		self.__editor.disconnect_signal(self.__signal_id_1, self)
#		self.__editor.disconnect_signal(self.__signal_id_3, self.textbuffer)
		self.__editor.disconnect_signal(self.__signal_id_2, self.editor)
		self.remove_all_bookmarks()
		del self
		self = None
		return

	def __get_bookmark_on_line(self, line):
		"""
		Get the bookmark on a particular line.

		@param self: Reference to the BookmarkManager instance.
		@type self: A BookmarkManager object.

		@param line: The line to get the bookmark from.
		@type line: An Integer object.

		@return: A bookmark on the line.
		@rtype: A gtksourceview.SourceMarker object.
		"""
		begin_position = self.textbuffer.get_iter_at_line(line)
		end_position = begin_position.copy()
		end_position.forward_to_line_end()
		bookmarks = []
		markers = self.textbuffer.get_markers_in_region(begin_position, end_position)
		for marker in markers:
			if marker.get_marker_type() == "scribes_bookmark":
				if marker.get_line() == line:
					bookmarks.append(marker)
		return bookmarks

	def __update_bookmark_database(self):
		"""
		Store the position of bookmarks in the buffer in a database.

		@param self: Reference to the BookmarkManager instance.
		@type self: A BookmarkManager object.
		"""
		if self.editor.uri is None: return False
		lines = self.get_bookmarked_lines()
#		from operator import not_
#		if not_(lines): return False
		from BookmarkMetadata import update_bookmarks_in_database
		update_bookmarks_in_database(str(self.editor.uri), lines)
		return False

	def __create_bookmark_image(self):
		"""
		Create the bookmark image for the text editor.

		@param self: Reference to the BookmarkManager instance.
		@type self: A BookmarkManager object.

		@return: An image representing a bookmark.
		@rtype: A gtk.gdk.Pixbuf object.
		"""
		image_file = self.__find_bookmark_image()
		from gtk import Image
		image = Image()
		image.set_from_file(image_file)
		pixbuf = image.get_pixbuf()
		return pixbuf

	def __find_bookmark_image(self):
		"""
		Return the path to the bookmark image on the host's file system.

		@param self: Reference to the BookmarkManager instance.
		@type self: A BookmarkManager object.

		@return: Path to the bookmark image.
		@rtype: A String object.
		"""
		try:
			from os import path
			image_path = path.join(self.__editor.scribes_data_folder, "bookmarks.png")
		except:
			print "Error: Could not find scribes data files."
		return image_path
