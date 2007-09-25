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
This module documents a class that creates an object that searches for,
or replaces, text found in the text editor's buffer.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2005 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE

class SearchReplaceManager(GObject):
	"""
	This class implements and object that searches for, or replaces,
	text found in the text editor's buffer.
	"""

	__gsignals__ = {
		"matches-found": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"no-matches-found": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"searching": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"next": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"previous": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"cancel": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"updated-queries": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"replacing": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"replaced": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"replaced-all": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		"""
		Initialize the object.

		@param self: Reference to the SearchReplaceManager instance.
		@type self: A SearchReplaceManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		GObject.__init__(self)
		self.__init_attributes(editor)
		self.__store_id = self.__editor.store.add_object("SearchReplaceManager", self)
		self.__signal_id_1 = self.connect("searching", self.__search_searching_cb)
		self.__signal_id_2 = self.connect("matches-found", self.__search_matches_found_cb)
		self.__signal_id_3 = self.connect("no-matches-found", self.__search_no_matches_found_cb)
		self.__signal_id_4 = self.connect("next", self.__search_next_cb)
		self.__signal_id_5 = self.connect("previous", self.__search_previous_cb)
		self.__signal_id_6 = self.connect("cancel", self.__search_cancel_cb)
		self.__signal_id_7 = self.connect("replacing", self.__search_replacing_cb)
		self.__signal_id_8 = self.connect("replaced", self.__search_replaced_cb)
		self.__signal_id_9 = self.connect("replaced-all", self.__search_replace_all_cb)
		self.__signal_id_10 = editor.connect("hide-bar", self.__search_hide_bar_cb)
		self.__signal_id_11 = editor.connect("show-bar", self.__search_show_bar_cb)
		self.__signal_id_12 = self.connect("destroy", self.__destroy_cb)
		self.__gconf_client.notify_add("/apps/scribes/match_case", self.__search_client_cb)
		self.__gconf_client.notify_add("/apps/scribes/match_word", self.__search_client_cb)

	def __init_attributes(self, editor):
		"""
		Initialize data attributes for the object.

		@param self: Reference to the SearchReplaceManager instance.
		@type self: A SearchReplaceManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__queries = []
		self.__start_point_mark = None
		self.__end_point_mark = None
		self.__index = None
		self.__number_of_matches = None
		self.__position_of_matches = []
		self.__match_tag = self.__create_match_tag()
		self.__selection_tag = self.__create_selection_tag()
		self.__replace_tag = self.__create_replace_tag()
		self.__cancel_search_operation = False
		self.__cancel_replace_operation = False
		self.__enable_regular_expression = False
		self.__enable_incremental_search = False
		self.__reset_flag = True
		from gconf import client_get_default
		self.__gconf_client = client_get_default()
		self.__match_case = self.__gconf_client.get_bool("/apps/scribes/match_case")
		self.__match_word = self.__gconf_client.get_bool("/apps/scribes/match_word")
		self.__is_initialized = True
		self.__bar_is_visible = False
		self.__status_id = None
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		self.__signal_id_4 = self.__signal_id_5 = self.__signal_id_6 = None
		self.__signal_id_7 = self.__signal_id_8 = self.__signal_id_9 = None
		self.__signal_id_10 = self.__signal_id_11 = self.__signal_id_12 = None
		self.__store_id = None
		return

	def __get_index(self):
		return self.__index

	def __get_number_of_matches(self):
		return self.__number_of_matches

	def __get_queries(self):
		return self.__queries

	def __get_is_initialized(self):
		return self.__is_initialized

########################################################################
#
#						Public Search Methods
#
########################################################################

	# Public API property.
	index = property(__get_index, doc="")
	number_of_matches = property(__get_number_of_matches, doc="Number of match found")
	queries = property(__get_queries, doc="")
	is_initialized = property(__get_is_initialized, doc="")

	def find(self, string, start, end):
		"""
		Search the text editor's buffer for a string.

		@param self: Reference to the SearchReplaceManager instance.
		@type self: A SearchReplaceManager object.

		@param string: A string in the buffer to search for.
		@type string: A String object.
		"""
		self.__start_point_mark = start
		self.__end_point_mark = end
		self.__reset_flag = False
		self.__cancel_search_operation = False
		self.emit("searching")
		if not string in self.__queries:
			self.__queries.append(string)
			self.emit("updated-queries")
		else:
			self.__queries.remove(string)
			self.__queries.append(string)
#		begin, end = self.__editor.textbuffer.get_bounds()
		found_matches = self.__search_for_matches(string)
		if self.__cancel_search_operation:
			self.__reset()
			return
		if found_matches:
			self.__position_of_matches = found_matches
			self.emit("matches-found")
		else:
			if self.__cancel_search_operation:
				self.__reset()
				return
			self.emit("no-matches-found")
		return

	def search(self, string, start, end):
		self.find(string, start, end)
		return

	def next(self):
		"""
		Move the selection tag to the next match.

		@param self: Reference to the SearchReplaceManager instance.
		@type self: A SearchReplaceManager object.
		"""
		self.emit("next")
		return

	def previous(self):
		"""
		Move the selection tag to the previous match.

		@param self: Reference to the SearchReplaceManager instance.
		@type self: A SearchReplaceManager object.
		"""
		self.emit("previous")
		return

########################################################################
#
#						Public Replace Methods
#
########################################################################

	def replace(self, text):
		"""
		Replace selected text in the text editor's buffer.

		@param self: Reference to the Replace instance.
		@type self: A Replace object.
		"""
		self.__reset_flag = False
		self.__cancel_replace_operation = False
		self.emit("replacing")
		begin, end = self.__position_of_matches[self.__index]
		textbuffer = self.__editor.textbuffer
		begin_mark = textbuffer.create_mark(None, begin, True)
		self.__reset()
		textbuffer.begin_user_action()
		textbuffer.delete(begin, end)
		begin = textbuffer.get_iter_at_mark(begin_mark)
		textbuffer.insert_with_tags(begin, text, self.__replace_tag)
		textbuffer.end_user_action()
		if begin_mark.get_deleted() is False:
			textbuffer.delete_mark(begin_mark)
		self.emit("replaced")
		return

	def replace_all(self, text):
		"""
		Replace all selected text in the text editor's buffer.

		@param self: Reference to the Replace instance.
		@type self: A Replace object.
		"""
		self.__reset_flag = False
		self.__cancel_replace_operation = False
		self.emit("replacing")
		position_marks = []
		textbuffer = self.__editor.textbuffer
		def delete_marks():
			for item in position_marks:
				if item[0].get_deleted() is False:
					textbuffer.delete_mark(item[0])
				if item[1].get_deleted() is False:
					textbuffer.delete_mark(item[1])
		from SCRIBES.utils import response
		for position in self.__position_of_matches:
			response()
			mark_begin = textbuffer.create_mark(None, position[0], True)
			mark_end = textbuffer.create_mark(None, position[1], False)
			position_marks.append((mark_begin, mark_end))
			if self.__cancel_replace_operation:
				delete_marks()
				self.__reset()
				return
		self.__reset()
		from SCRIBES.cursor import move_view_to_cursor
		textbuffer.begin_user_action()
		for position in position_marks:
			response()
			if self.__cancel_replace_operation:
				delete_marks()
				return
			begin = textbuffer.get_iter_at_mark(position[0])
			end = textbuffer.get_iter_at_mark(position[1])
			textbuffer.delete(begin, end)
			begin = textbuffer.get_iter_at_mark(position[0])
			textbuffer.place_cursor(begin)
			textbuffer.insert_with_tags(begin, text, self.__replace_tag)
			move_view_to_cursor(self.__editor.textview)
		textbuffer.end_user_action()
		delete_marks()
		if self.__cancel_replace_operation:
			self.__reset()
			return
		self.emit("replaced-all")
		return

########################################################################
#
#							Public Methods
#
########################################################################

	def cancel(self):
		"""
		Cancel a search operation.

		@param self: Reference to the SearchReplaceManager instance.
		@type self: A SearchReplaceManager object.
		"""
		self.emit("cancel")
		return

	def reset(self):
		"""
		Reset the search processor's state.

		@param self: Reference to the SearchReplaceManager instance.
		@type self: A SearchReplaceManager object.
		"""
		self.__reset()
		return

	def enable_incremental_searching(self, value=True):
		"""
		Enable or disable incremental searching.

		@param self: Reference to the SearchReplaceManager instance.
		@type self: A SearchReplaceManager object.

		@param value: True to enable incremental searching.
		@type value: A Boolean object.
		"""
		if value is True or value is False:
			self.__enable_incremental_search = value
		return

	def get_queries(self):
		"""
		Return a list of search queries.

		@param self: Reference to the SearchReplaceManager instance.
		@type self: A SearchReplaceManager object.

		@return: A list of search queries.
		@rtype: A List object.
		"""
		return self.__queries

	def is_initialized(self):
		return self.__is_initialized

########################################################################
#
#						Tags for Matches
#
########################################################################

	def __create_match_tag(self):
		"""
		Create the search processor's match tag.

		@param self: Reference to the SearchReplaceManager instance.
		@type self: A SearchReplaceManager object.
		"""
		tag = self.__editor.textbuffer.create_tag()
		tag.set_property("background", "yellow")
		tag.set_property("foreground", "blue")
		from pango import WEIGHT_BOLD
		tag.set_property("weight", WEIGHT_BOLD)
		return tag

	def __create_selection_tag(self):
		"""
		Create the search processor's selection tag

		@param self: Reference to the SearchReplaceManager instance.
		@type self: A SearchReplaceManager object.
		"""
		tag = self.__editor.textbuffer.create_tag()
		tag.set_property("background", "blue")
		tag.set_property("foreground", "yellow")
		from pango import WEIGHT_HEAVY
		tag.set_property("weight", WEIGHT_HEAVY)
		return tag

	def __create_replace_tag(self):
		"""
		Create the replace tag for the Replace object.

		@param self: Reference to the Replace instance.
		@type self: A Replace object.
		"""
		tag = self.__editor.textbuffer.create_tag()
		tag.set_property("background", "green")
		tag.set_property("foreground", "blue")
		from pango import WEIGHT_HEAVY
		tag.set_property("weight", WEIGHT_HEAVY)
		return tag

########################################################################
#
#							Search Algorithm
#
########################################################################

	def __search_for_matches(self, string):
		"""
		Search the text editor's buffer for a string.

		@param self: Reference to the SearchReplaceManager instance.
		@type self: A SearchReplaceManager object.

		@param string: The string to search for.
		@type string: A String object.
		"""
		begin = self.__editor.textbuffer.get_iter_at_mark(self.__start_point_mark)
		end = self.__editor.textbuffer.get_iter_at_mark(self.__end_point_mark)
		if self.__enable_incremental_search:
			from SCRIBES.cursor import get_cursor_iterator
			begin = get_cursor_iterator(self.__editor.textbuffer)
			self.__editor.textbuffer.move_mark(self.__start_point_mark, begin)
		text = self.__editor.textbuffer.get_text(begin, end)
		found_matches = []
		from re import UNICODE, findall, escape, MULTILINE, IGNORECASE
		if self.__enable_regular_expression:
			if self.__match_case:
				matches = findall(string, text, UNICODE|MULTILINE)
			else:
				matches = findall(string, text, UNICODE|MULTILINE|IGNORECASE)
		else:
			if self.__match_case:
				matches = findall(escape(string), text, UNICODE|MULTILINE)
			else:
				matches = findall(escape(string), text, UNICODE|MULTILINE|IGNORECASE)
		if not matches:
			return None
		found_matches = self.__get_positions(matches)
		return found_matches

	def __get_positions(self, matches):
		"""
		Get position of found matches in the buffer.

		@param self: Reference to the SearchReplaceManager instance.
		@type self: A SearchReplaceManager object.

		@param matches: Found matches.
		@type matches: A List object.

		@return: Position of found matches in the text editor's buffer.
		@rtype: A List object.
		"""
		positions = []
		begin = self.__editor.textbuffer.get_iter_at_mark(self.__start_point_mark)
		end = self.__editor.textbuffer.get_iter_at_mark(self.__end_point_mark)
		from gtk import TEXT_SEARCH_VISIBLE_ONLY
		from SCRIBES.utils import response
		for match in matches:
			if self.__cancel_search_operation:
				return None
			response()
			start, stop = begin.forward_search(match, TEXT_SEARCH_VISIBLE_ONLY, end)
			positions.append((start, stop))
			begin = stop
		if self.__match_word and self.__enable_regular_expression is False:
			temp = []
			for start, stop in positions:
				if start.starts_word() and stop.ends_word():
					temp.append((start, stop))
			positions = temp
		return positions

########################################################################
#
#						Event and Signal Handlers
#
########################################################################

	def __search_searching_cb(self, SearchReplaceManager):
		"""
		Handles callback when the "searching" signal is emitted.

		@param self: Reference to the SearchReplaceManager instance.
		@type self: A SearchReplaceManager object.

		@param SearchReplaceManager: The text editor's search processor.
		@type SearchReplaceManager: A SearchReplaceManager object.
		"""
		from i18n import msg0001
		if self.__status_id:
			self.__editor.feedback.unset_modal_message(self.__status_id)
		self.__status_id = self.__editor.feedback.set_modal_message(msg0001, "run")
		return

	def __search_matches_found_cb(self, SearchReplaceManager):
		"""
		Handles callback when the "matches-found" signal is emitted.

		@param self: Reference to the SearchReplaceManager instance.
		@type self: A SearchReplaceManager object.

		@param SearchReplaceManager: The text editor's search processor.
		@type SearchReplaceManager: A SearchReplaceManager object.
		"""
		self.__reset_flag = False
		if self.__cancel_search_operation:
			return
		self.__index = 0
		self.__number_of_matches = len(self.__position_of_matches)
		for position in self.__position_of_matches:
			if self.__cancel_search_operation:
				return
			self.__editor.textbuffer.apply_tag(self.__match_tag, position[0], position[1])
		begin, end = self.__position_of_matches[self.__index]
		self.__editor.textbuffer.place_cursor(begin)
		self.__editor.textbuffer.apply_tag(self.__selection_tag, begin, end)
		from SCRIBES.cursor import move_view_to_cursor
		move_view_to_cursor(self.__editor.textview)
		# Send feedback to the status bar.
		if self.__status_id:
			self.__editor.feedback.unset_modal_message(self.__status_id)
		from i18n import msg0002, msg0003
		message = msg0003 % (self.__index+1, self.__number_of_matches)
		self.__status_id = self.__editor.feedback.set_modal_message(message, "find")
		message = msg0002 % self.__number_of_matches
		self.__editor.feedback.update_status_message(message, "succeed", 10)
		return

	def __search_no_matches_found_cb(self, SearchReplaceManager):
		"""
		Handles callback when the "no-matches-found" signal is emitted.

		@param self: Reference to the SearchReplaceManager instance.
		@type self: A SearchReplaceManager object.

		@param SearchReplaceManager: The text editor's SearchReplaceManager.
		@type SearchReplaceManager: A SearchReplaceManager object.
		"""
		self.__reset()
		from i18n import msg0004
		self.__editor.feedback.update_status_message(msg0004, "warning", 10)
		return

	def __search_next_cb(self, SearchReplaceManager):
		"""
		Handles callback when the "next" signal is emitted.

		@param self: Reference to the SearchReplaceManager instance.
		@type self: A SearchReplaceManager object.

		@param SearchReplaceManager: The text editor's SearchReplaceManager.
		@type SearchReplaceManager: A SearchReplaceManager object.
		"""
		self.__reset_flag = False
		if self.__index >= self.__number_of_matches - 1:
			from i18n import msg0005
			self.__editor.feedback.update_status_message(msg0005, "warning")
			return
		begin, end = self.__editor.textbuffer.get_bounds()
		self.__editor.textbuffer.remove_tag(self.__selection_tag, begin, end)
		self.__index += 1
		begin, end = self.__position_of_matches[self.__index]
		self.__editor.textbuffer.place_cursor(begin)
		self.__editor.textbuffer.apply_tag(self.__selection_tag, begin, end)
		from SCRIBES.cursor import move_view_to_cursor
		move_view_to_cursor(self.__editor.textview)
		if self.__status_id:
			self.__editor.feedback.unset_modal_message(self.__status_id)
		from i18n import msg0003
		message = msg0003 % (self.__index+1, self.__number_of_matches)
		self.__status_id = self.__editor.feedback.set_modal_message(message, "find")
		return

	def __search_previous_cb(self, SearchReplaceManager):
		"""
		Handles callback when the "previous" signal is emitted.

		@param self: Reference to the SearchReplaceManager instance.
		@type self: A SearchReplaceManager object.

		@param SearchReplaceManager: The text editor's SearchReplaceManager.
		@type SearchReplaceManager: A SearchReplaceManager object.
		"""
		self.__reset_flag = False
		if self.__index <= 0:
			from i18n import msg0010
			self.__editor.feedback.update_status_message(msg0010, "warning")
			return
		begin, end = self.__editor.textbuffer.get_bounds()
		self.__editor.textbuffer.remove_tag(self.__selection_tag, begin, end)
		self.__index -= 1
		begin, end = self.__position_of_matches[self.__index]
		self.__editor.textbuffer.place_cursor(begin)
		self.__editor.textbuffer.apply_tag(self.__selection_tag, begin, end)
		from SCRIBES.cursor import move_view_to_cursor
		move_view_to_cursor(self.__editor.textview)
		if self.__status_id:
			self.__editor.feedback.unset_modal_message(self.__status_id)
		from i18n import msg0003
		message = msg0003 % (self.__index+1, self.__number_of_matches)
		self.__status_id = self.__editor.feedback.set_modal_message(message, "find")
		return

	def __search_cancel_cb(self, SearchReplaceManager):
		"""
		Handles callback when the "cancel" signal is emitted.

		@param self: Reference to the SearchReplaceManager instance.
		@type self: A SearchReplaceManager object.

		@param SearchReplaceManager: The text editor's SearchReplaceManager.
		@type SearchReplaceManager: A SearchReplaceManager object.
		"""
		self.__cancel_search_operation = True
		self.__cancel_replace_operation = True
		self.__reset()
		from i18n import msg0006
		self.__editor.feedback.set_modal_message(msg0006, "stop")
		return

	def __search_hide_bar_cb(self, editor, bar):
		"""
		Handles callback when the "hide-bar" signal is emitted.

		@param self: Reference to the SearchReplaceManager instance.
		@type self: A SearchReplaceManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param bar: One of the text editor's bar objects.
		@type bar: A ScribesBar object.
		"""
		from operator import is_, truth
		if truth(self.__start_point_mark) and is_(self.__start_point_mark.get_deleted(), False):
			self.__editor.textbuffer.delete_mark(self.__start_point_mark)
			self.__start_point_mark = None
		if truth(self.__end_point_mark) and is_(self.__end_point_mark.get_deleted(), False):
			self.__editor.textbuffer.delete_mark(self.__end_point_mark)
			self.__end_point_mark = None
		self.__bar_is_visible = False
		if not self.__index is None:
			begin, end = self.__position_of_matches[self.__index]
			self.__editor.textbuffer.select_range(begin, end)
		self.__reset()
		self.__enable_regular_expression = False
		self.__enable_incremental_search = False
		return

	def __search_show_bar_cb(self, editor, bar):
		"""
		Handles callback when the "show-bar" signal is emitted.

		@param self: Reference to the SearchReplaceManager instance.
		@type self: A SearchReplaceManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param bar: One of the text editor's bar objects.
		@type bar: A ScribesBar object.
		"""
		self.__bar_is_visible = True
		return

	def __search_replacing_cb(self, processor):
		self.__reset_flag = False
		from i18n import msg0007
		if self.__status_id:
			self.__editor.feedback.unset_modal_message(self.__status_id)
		self.__status_id = self.__editor.feedback.set_modal_message(msg0007, "run")
		return

	def __search_replaced_cb(self, processor):
		self.__reset_flag = False
		from i18n import msg0008
		if self.__status_id:
			self.__editor.feedback.unset_modal_message(self.__status_id)
		self.__editor.feedback.update_status_message(msg0008, "succeed", 10)
		return

	def __search_replace_all_cb(self, processor):
		self.__reset_flag = False
		from i18n import msg0009
		if self.__status_id:
			self.__editor.feedback.unset_modal_message(self.__status_id)
		self.__editor.feedback.update_status_message(msg0009, "succeed", 10)
		return

	def __search_client_cb(self, client, cnxn_id, entry, data):
		"""
		Handles callback when the GConf database is modified.

		@param self: Reference to the SearchReplaceManager instance.
		@type self: A SearchReplaceManager object.
		"""
		self.__match_case = client.get_bool("/apps/scribes/match_case")
		self.__match_word = client.get_bool("/apps/scribes/match_word")
		return

########################################################################
#
#						Auxiliary Method
#
########################################################################

	def __reset(self):
		"""
		Reset the search processor's state.

		@param self: Reference to the SearchReplaceManager instance.
		@type self: A SearchReplaceManager object.
		"""
		if self.__reset_flag:
			return
		if self.__status_id:
			self.__editor.feedback.unset_modal_message(self.__status_id)
		self.__status_id = None
		self.__index = None
		self.__number_of_matches = None
		self.__position_of_matches = []
		begin, end = self.__editor.textbuffer.get_bounds()
		self.__editor.textbuffer.remove_tag(self.__match_tag, begin, end)
		self.__editor.textbuffer.remove_tag(self.__selection_tag, begin, end)
		self.__editor.textbuffer.remove_tag(self.__replace_tag, begin, end)
		self.__cancel_search_operation = False
		self.__cancel_replace_operation = False
		self.__reset_flag = True
		return

	def __destroy_cb(self, manager):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the SearchReplaceManager instance.
		@type self: A SearchReplaceManager object.

		@param manager: Reference to the SearchReplaceManager instance.
		@type manager: A SearchReplaceManager object.
		"""
		self.__editor.store.remove_object("SearchReplaceManager", self.__store_id)
		from SCRIBES.utils import disconnect_signal, delete_attributes
		from SCRIBES.utils import delete_list
		disconnect_signal(self.__signal_id_1, self)
		disconnect_signal(self.__signal_id_2, self)
		disconnect_signal(self.__signal_id_3, self)
		disconnect_signal(self.__signal_id_4, self)
		disconnect_signal(self.__signal_id_5, self)
		disconnect_signal(self.__signal_id_6, self)
		disconnect_signal(self.__signal_id_7, self)
		disconnect_signal(self.__signal_id_8, self)
		disconnect_signal(self.__signal_id_9, self)
		disconnect_signal(self.__signal_id_12, self)
		disconnect_signal(self.__signal_id_11, self.__editor)
		disconnect_signal(self.__signal_id_10, self.__editor)
		delete_list(self.__queries)
		delete_list(self.__position_of_matches)
		delete_attributes(self)
		del self
		self = None
		return
