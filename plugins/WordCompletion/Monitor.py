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
This module documents a class that monitors the buffer for potential
words for automatic completions.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class CompletionMonitor(object):
	"""
	This class creates an object that monitors the buffer for words for
	automatic completion.
	"""

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__signal_id_1 = self.__manager.connect("destroy", self.__destroy_cb)
		self.__signal_id_2 = self.__manager.connect("update", self.__update_cb)
		self.__signal_id_3 = editor.textbuffer.connect_after("insert-text", self.__insert_text_cb)
		self.__signal_id_4 = editor.textview.connect("undo", self.__generic_cb)
		self.__signal_id_5 = editor.textview.connect("redo", self.__generic_cb)
		self.__signal_id_6 = editor.textview.connect("paste-clipboard", self.__generic_cb)
		self.__signal_id_7 = editor.textview.connect_after("undo", self.__generic_cb)
		self.__signal_id_8 = editor.textview.connect_after("redo", self.__generic_cb)
		self.__signal_id_9 = editor.textview.connect_after("paste-clipboard", self.__generic_cb)
		self.__signal_id_10 = editor.textview.connect("key-press-event", self.__key_press_event_cb)
		self.__signal_id_11 = manager.connect("is-visible", self.__is_visible_cb)
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__precompile_methods, priority=9999)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		self.__match_found = False
		self.__completion_window_is_visible = False
		self.__dictionary = self.__create_completion_dictionary()
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		self.__signal_id_4 = self.__signal_id_5 = self.__signal_id_6 = None
		self.__signal_id_7 = self.__signal_id_8 = self.__signal_id_9 = None
		return

########################################################################
#
#						Helper Methods
#
########################################################################

	def __check_buffer(self):
		try:
			word = self.__editor.get_word_before_cursor()
			if word:
				matches = self.__find_matches(word)
				self.__emit_match_found(matches) if matches else self.__emit_no_match_found()
			else:
				self.__emit_no_match_found()
		except:
			self.__emit_no_match_found()
		return False

	def __emit_match_found(self, matches):
#		if self.__match_found: return
		self.__match_found = True
		self.__manager.emit("match-found", matches)
		return

	def __emit_no_match_found(self):
		if self.__match_found is False: return
		self.__manager.emit("no-match-found")
		self.__match_found = False
		return

	def __find_matches(self, word):
		dictionary = self.__dictionary.get_dictionary()
		if not dictionary: return None
		match_list = [list(items) for items in dictionary.items() \
				if items[0].startswith(word) and (items[0] != word)]
		if not match_list: return None
		match_list.sort(self.__sort_matches_occurrence_only)
		matches = [items[0] for items in match_list]
		return matches

	def __sort_matches(self, x, y):
		if (len(x[0]) < len(y[0])): return -1
		if (len(x[0]) > len(y[0])): return 1
		if (len(x[0]) == len(y[0])):
			if (x[1] < y[1]): return 1
			if (x[1] > y[1]): return -1
		return 0

	def __sort_matches_occurrence_only(self, x, y):
		if (x[1] < y[1]): return 1
		if (x[1] > y[1]): return -1
		return 0

	def __precompile_methods(self):
		methods = (self.__insert_text_cb, self.__key_press_event_cb,
				self.__emit_no_match_found, self.__emit_match_found)
		self.__editor.optimize(methods)
		return False

	def __create_completion_dictionary(self):
		try:
			from SCRIBES.Exceptions import GlobalStoreObjectDoesNotExistError
			dictionary = self.__editor.get_global_object("WordCompletionDictionary")
		except GlobalStoreObjectDoesNotExistError:
			from CompletionDictionary import CompletionDictionary
			self.__editor.add_global_object("WordCompletionDictionary", CompletionDictionary())
			dictionary = self.__editor.get_global_object("WordCompletionDictionary")
		return dictionary

	def __update_dictionary(self, dictionary):
		if (self.__dictionary.get_dictionary() == dictionary): return False
		self.__dictionary.update(dictionary)
		return False

########################################################################
#
#						Signal and Event Handlers
#
########################################################################

	def __insert_text_cb(self, textbuffer, iterator, text, length):
		try:
			if (length > 1): raise ValueError
			from gobject import idle_add, source_remove, PRIORITY_LOW, timeout_add
			try:
				source_remove(self.__insert_text_id)
			except:
				pass
			if self.__completion_window_is_visible:
				self.__check_buffer()
#				self.__insert_text_id = idle_add(self.__check_buffer, priority=9999)
			else:
				self.__insert_text_id = timeout_add(100, self.__check_buffer, priority=9999)
#			self.__check_buffer()
		except ValueError:
			self.__emit_no_match_found()
		return False

	def __generic_cb(self, *args):
		"""
		A generic callback method.

		@param self: Reference to the CompletionMonitor instance.
		@type self: A CompletionMonitor object.

		@param *args: Irrelevant arguments.
		@type *args: A List object.
		"""
		self.__manager.emit("no-match-found")
		from gobject import source_remove
		try:
			source_remove(self.__insert_text_id)
		except:
			pass
		return False

	def __update_cb(self, manager, dictionary):
		"""
		Handles callback when the "update" signal is emitted.

		@param self: Reference to the CompletionMonitor instance.
		@type self: An CompletionMonitor object.

		@param manager: Reference to the CompletionManager.
		@type manager: An CompletionManager object.
		"""
		try:
			from gobject import timeout_add, PRIORITY_LOW, source_remove
			source_remove(self.__dictionary_timer)
		except:
			pass
		self.__dictionary_timer = timeout_add(1000, self.__update_dictionary, dictionary, priority=9999)
		return

	def __key_press_event_cb(self, textview, event):
		"""
		Handles callback when the "key-press-event" is emitted.

		@param self: Reference to the CompletionMonitor instance.
		@type self: A CompletionMonitor object.

		@param textview: The text editor's buffer container.
		@type textview: A textview object.
		"""
		from gtk import keysyms
		hide_keys = (keysyms.BackSpace, keysyms.space, keysyms.Tab, keysyms.Escape)
		if  event.keyval in hide_keys: self.__emit_no_match_found()
		return False

	def __is_visible_cb(self, manager, visibility):
		self.__completion_window_is_visible = visibility
		return False

	def __destroy_cb(self, manager):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the CompletionMonitor instance.
		@type self: An CompletionMonitor object.

		@param manager: Reference to the CompletionManager.
		@type manager: An CompletionManager object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self.__manager)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__manager)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__editor.textbuffer)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__editor.textview)
		self.__editor.disconnect_signal(self.__signal_id_5, self.__editor.textview)
		self.__editor.disconnect_signal(self.__signal_id_6, self.__editor.textview)
		self.__editor.disconnect_signal(self.__signal_id_7, self.__editor.textview)
		self.__editor.disconnect_signal(self.__signal_id_8, self.__editor.textview)
		self.__editor.disconnect_signal(self.__signal_id_9, self.__editor.textview)
		self.__editor.disconnect_signal(self.__signal_id_10, self.__editor.textview)
		del self
		self = None
		return
