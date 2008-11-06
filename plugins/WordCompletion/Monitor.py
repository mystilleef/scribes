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
		self.__sigid1 = self.__manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = self.__manager.connect("update", self.__update_cb)
		self.__sigid3 = editor.textbuffer.connect_after("insert-text", self.__insert_text_cb)
		self.__sigid4 = editor.textview.connect("undo", self.__generic_cb)
		self.__sigid5 = editor.textview.connect("redo", self.__generic_cb)
		self.__sigid6 = editor.textview.connect("paste-clipboard", self.__generic_cb)
		self.__sigid7 = editor.textview.connect_after("undo", self.__generic_cb)
		self.__sigid8 = editor.textview.connect_after("redo", self.__generic_cb)
		self.__sigid9 = editor.textview.connect_after("paste-clipboard", self.__generic_cb)
		self.__sigid10 = editor.textview.connect("key-press-event", self.__key_press_event_cb)
		self.__sigid11 = manager.connect("is-visible", self.__is_visible_cb)
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=9999)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		self.__match_found = False
		self.__completion_window_is_visible = False
		from CompletionDictionary import CompletionDictionary
		self.__dictionary = CompletionDictionary()
		return

	def __precompile_methods(self):
		methods = (self.__key_press_event_cb, self.__insert_text_cb,
			self.__generic_cb, self.__is_visible_cb, 
			self.__update_cb, self.__get_word_to_cursor,
			self.__get_word_before_cursor, self.__emit_no_match_found,
			self.__emit_match_found, self.__find_matches,
			self.__sort_matches_occurrence_only, self.__sort_matches,
			self.__check_buffer)
		self.__editor.optimize(methods)
		return False

########################################################################
#
#						Helper Methods
#
########################################################################

	def __get_word_to_cursor(self):
		from SCRIBES.Word import ends_word, get_word
		if not ends_word(self.__editor.cursor): return None
		word = get_word(self.__editor.textbuffer, self.__editor.cursor)
		return word

	def __get_word_before_cursor(self):
		if self.__editor.inside_word(self.__editor.cursor) is False: return None
		word = self.__editor.textbuffer.get_text(*(self.__editor.get_word_boundary(self.__editor.cursor)))
		if len(word) > 2: return word
		return None

	def __check_buffer(self):
		try:
			word = self.__get_word_before_cursor()
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

	def __update_dictionary(self, dictionary):
		if (self.__dictionary.get_dictionary() == dictionary): return False
		self.__dictionary.update(dictionary)
		return False
	
	def __check_buffer_cb(self):
		try:
			from gobject import source_remove, idle_add
			source_remove(self.__check_buffer_timer)
		except AttributeError:
			pass
		finally:
			self.__check_buffer_timer = idle_add(self.__check_buffer, priority=9999)
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
			else:
				self.__insert_text_id = timeout_add(100, self.__check_buffer_cb, priority=9999)
		except ValueError:
			self.__emit_no_match_found()
		return False

	def __generic_cb(self, *args):
		self.__manager.emit("no-match-found")
		from gobject import source_remove
		try:
			source_remove(self.__insert_text_id)
		except:
			pass
		return False

	def __update_cb(self, manager, dictionary):
		try:
			from gobject import timeout_add, PRIORITY_LOW, source_remove
			source_remove(self.__dictionary_timer)
		except:
			pass
		self.__dictionary_timer = timeout_add(1000, self.__update_dictionary, dictionary, priority=9999)
		return

	def __key_press_event_cb(self, textview, event):
		from gtk import keysyms
		hide_keys = (keysyms.BackSpace, keysyms.space, keysyms.Tab, keysyms.Escape)
		if  event.keyval in hide_keys: self.__emit_no_match_found()
		return False

	def __is_visible_cb(self, manager, visibility):
		self.__completion_window_is_visible = visibility
		return False

	def __destroy_cb(self, manager):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor.textbuffer)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor.textview)
		self.__editor.disconnect_signal(self.__sigid5, self.__editor.textview)
		self.__editor.disconnect_signal(self.__sigid6, self.__editor.textview)
		self.__editor.disconnect_signal(self.__sigid7, self.__editor.textview)
		self.__editor.disconnect_signal(self.__sigid8, self.__editor.textview)
		self.__editor.disconnect_signal(self.__sigid9, self.__editor.textview)
		self.__editor.disconnect_signal(self.__sigid10, self.__editor.textview)
		del self
		self = None
		return
