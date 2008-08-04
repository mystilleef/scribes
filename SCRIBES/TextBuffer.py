# -*- coding: utf-8 -*-
# Copyright (C) 2005 Lateef Alabi-Oki
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
This module implements a class that creates the buffer for the text
editor.

@author: Lateef Alabi-Oki
@organiation: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gtksourceview2 import Buffer

class ScribesTextBuffer(Buffer):
	"""
	This class creates the buffer for the text editor.
	"""

	def __init__(self, editor):
		Buffer.__init__(self)
		self.__init_attributes(editor)
		self.__set_properties()
		self.__signal_id_1 = editor.connect("close-document-no-save", self.__close_document_no_save_cb)
		self.__signal_id_2 = editor.connect("checking-document", self.__checking_document_cb)
		self.__signal_id_3 = editor.connect("loaded-document", self.__loaded_document_cb)
		self.__signal_id_4 = editor.connect("load-error", self.__load_error_cb)
		self.__signal_id_5 = editor.connect("saved-document", self.__saved_document_cb)
		self.__signal_id_6 = editor.connect("enable-readonly", self.__enable_readonly_cb)
		self.__signal_id_7 = editor.connect("disable-readonly", self.__disable_readonly_cb)
		self.__signal_id_8 = editor.connect("close-document", self.__close_document_cb)
		self.__signal_id_9 = editor.connect("renamed-document", self.__renamed_document_cb)
		self.__signal_id_10 = self.connect("notify::cursor-position", self.__cursor_position_cb)
		self.__signal_id_11 = editor.connect("reload-document", self.__reload_document_cb)
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monitor_id_1 = monitor_add(self.__theme_database_uri, MONITOR_FILE, self.__theme_changed_cb)
#		from gobject import idle_add, PRIORITY_LOW
#		idle_add(self.__precompile_methods, priority=5000)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__uri = None
		# Register a unique number with the editor's termination queue
		self.__termination_id = editor.register_object()
		self.__undoable_action = False
		from os.path import join
		preference_folder = join(editor.metadata_folder, "Preferences")
		theme_database_path = join(preference_folder, "ColorTheme.gdb")
		from gnomevfs import get_uri_from_local_path
		self.__theme_database_uri = get_uri_from_local_path(theme_database_path)
		return

	def __set_properties(self):
		self.begin_not_undoable_action()
		mgr = self.__editor.style_scheme_manager
		from ColorThemeMetadata import get_value
		style_scheme = mgr.get_scheme(get_value())
		if style_scheme: self.set_style_scheme(style_scheme)
		self.set_highlight_syntax(True)
		self.set_highlight_matching_brackets(False)
		self.set_max_undo_levels(-1)
		self.set_text("")
		start, end = self.get_bounds()
		self.remove_all_tags(start, end)
		self.remove_source_marks(start, end)
		if self.get_modified(): self.set_modified(False)
		self.notify("cursor-position")
		self.end_not_undoable_action()
		return False

################################################################################
#
#							Signal Handlers
#
################################################################################

	def __checking_document_cb(self, editor, uri):
		self.__uri = uri
		self.begin_not_undoable_action()
		self.__undoable_action = True
		start, end = self.get_bounds()
		self.remove_all_tags(start, end)
		self.remove_source_marks(start, end)
#		from gobject import idle_add, PRIORITY_LOW
#		idle_add(self.__activate_sytnax_colors, priority=PRIORITY_LOW)
		from thread import start_new_thread
		start_new_thread(self.__activate_sytnax_colors, ())
#		self.__activate_sytnax_colors()
		return False

	def __loaded_document_cb(self, *args):
		if self.get_modified(): self.set_modified(False)
		self.end_not_undoable_action()
		self.__undoable_action = False
		from thread import start_new_thread
		start_new_thread(self.__set_cursor_positon, ())
		return False

	def __saved_document_cb(self, *args):
		if self.get_modified(): self.set_modified(False)
		return False

	def __enable_readonly_cb(self, editor):
		self.set_highlight_matching_brackets(False)
		return False

	def __disable_readonly_cb(self, editor):
		self.set_highlight_matching_brackets(True)
		return False

	def __load_error_cb(self, editor, uri):
		self.__uri = None
		if self.__undoable_action: self.end_not_undoable_action()
		self.__set_properties()
		return False

	def __close_document_cb(self, editor):
		self.__update_cursor_metadata(self.__uri)
		return False

	def __close_document_no_save_cb(self, editor):
		self.__destroy()
		return False

	def __renamed_document_cb(self, editor, uri, *args):
		self.__uri = uri
		if self.get_modified(): self.set_modified(False)
		self.set_highlight_matching_brackets(True)
		from gobject import idle_add
		idle_add(self.__activate_sytnax_colors)
		return False

	def __reload_document_cb(self, *args):
		if self.get_modified(): self.set_modified(False)
		self.set_text("")
		if self.get_modified(): self.set_modified(False)
		return False

	def __cursor_position_cb(self, *args):
		self.__editor.emit("cursor-moved")
		self.__stop_update_cursor_timer()
		from gobject import timeout_add, PRIORITY_LOW
		self.__cursor_update_timer = timeout_add(1000, self.__update_cursor_position, priority=9999)
		return False

########################################################################
#
#						Helper Methods
#
########################################################################

	def __activate_sytnax_colors(self):
		# Activate syntax highlight for the language.
		from syntax import activate_syntax_highlight
		activate_syntax_highlight(self, self.__editor.language)
		return False

	def __stop_update_cursor_timer(self):
		try:
			from gobject import source_remove
			source_remove(self.__cursor_update_timer)
		except:
			pass
		return

	def __update_cursor_position(self):
		if not (self.__uri): return False
		from cursor_metadata import update_cursor_position_in_database
		from cursor import get_cursor_line, get_cursor_index
		cursor_line = get_cursor_line(self)
		cursor_index = get_cursor_index(self)
		cursor_position = cursor_line, cursor_index
#		update_cursor_position_in_database(str(self.__uri), cursor_position)
		from gobject import idle_add
		idle_add(update_cursor_position_in_database, str(self.__uri), cursor_position, priority=9999)
		return False

	def __update_cursor_metadata(self, uri):
		self.__stop_update_cursor_timer()
		self.__update_cursor_position()
		self.__destroy()
		return False

	def __set_cursor_positon(self):
		try:
			from cursor_metadata import get_cursor_position_from_database
			position = get_cursor_position_from_database(self.__uri)
			cursor_line, cursor_index = position[0] + 1, position[1]
		except TypeError:
			cursor_line, cursor_index = 1, 0
		start_iterator = self.get_start_iter()
		number_of_lines = self.get_line_count()
		if cursor_line > number_of_lines:
			self.place_cursor(start_iterator)
			self.__editor.textview.grab_focus()
			return False
		iterator = self.get_iter_at_line(cursor_line - 1)
		line_index = iterator.get_bytes_in_line()
		if cursor_index > line_index:
			iterator.set_line_index(line_index)
		else:
			iterator.set_line_index(cursor_index)
		self.place_cursor(iterator)
		from cursor import move_view_to_cursor
		move_view_to_cursor(self.__editor.textview)
		self.__editor.textview.grab_focus()
		return False

	def __theme_changed_cb(self, *args):
		from ColorThemeMetadata import get_value
		style_scheme = self.__editor.style_scheme_manager.get_scheme(get_value())
		if style_scheme: self.set_style_scheme(style_scheme)
		return False

	def __precompile_methods(self):
		try:
			from psyco import bind
			bind(self.__cursor_position_cb)
			bind(self.__stop_update_cursor_timer)
			bind(self.__update_cursor_position)
		except ImportError:
			pass
		except:
			pass
		return False

	def __destroy(self):
		from gnomevfs import monitor_cancel
		if self.__monitor_id_1: monitor_cancel(self.__monitor_id_1)
		self.__editor.disconnect_signal(self.__signal_id_1, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_5, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_6, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_7, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_8, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_9, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_10, self)
		self.__editor.unregister_object(self.__termination_id)
		del self
		self = None
		return False
