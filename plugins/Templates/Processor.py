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
This module documents a class that creates an object that processes
templates.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class TemplateProcessor(object):
	"""
	This class creates an object that inserts templates with
	placeholders into the text editor's buffer and provides mechanisms
	for navigating between the placeholders.
	"""

	def __init__(self, manager, editor, template):
		"""
		Initialize object.

		@param self: Reference to the TemplateProcessor instance.
		@type self: A TemplateProcessor object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param template: A string representing a template.
		@type template: A String object.
		"""
		self.__init_attributes(manager, editor, template)
		from utils import insert_string
		editor.textbuffer.begin_user_action()
		insert_string(editor.textbuffer, template)
		self.__signal_id_1 = manager.connect("destroy", self.__destroy_cb)
		if self.__special_placeholders: self.__expand_special_placeholders()
		from gobject import timeout_add, idle_add
		if self.__placeholders:
			self.__mark_and_tag_placeholders()
			editor.textbuffer.end_user_action()
			self.__determine_last_placeholder()
			self.__select_first_placeholder()
			self.__signal_id_2 = editor.connect("cursor-moved", self.__cursor_moved_cb)
			self.__signal_id_3 = editor.textbuffer.connect("insert-text", self.__insert_text_cb)
			self.__signal_id_4 = editor.textbuffer.connect_after("insert-text",
											self.__insert_text_after_cb)
			from i18n import msg0001
			self.__status_id = self.__editor.feedback.set_modal_message(msg0001, "info")

		else:
			editor.textbuffer.end_user_action()
			idle_add(self.__destroy_cb, manager)

	def __init_attributes(self, manager, editor, template):
		"""
		Initialize object.

		@param self: Reference to the TemplateProcessor instance.
		@type self: A TemplateProcessor object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param template: A string representing a template.
		@type template: A String object.
		"""
		self.__manager = manager
		self.__editor = editor
		self.__template = template
		iterator = editor.get_cursor_position()
		self.__start_template_mark = editor.mark(iterator, "left")
		self.__end_template_mark = editor.mark(iterator, "right")
		from utils import get_placeholders, get_special_placeholders
		self.__placeholders = get_placeholders(template)
		self.__special_placeholders = get_special_placeholders(template)
		# A tag used for unmodified placeholders.
		self.__pre_modification_highlight_tag = self.__create_pre_modification_tag()
		# A tag used for modified placeholders.
		self.__post_modification_highlight_tag = self.__create_post_modification_tag()
		# A tag used for placeholders under modification.
		self.__modification_highlight_tag = self.__create_modification_tag()
		# A tag used for special placeholders.
		self.__special_highlight_tag = self.__create_special_tag()
		# Duplicate placeholders
		self.__mirror_list = self.__get_duplicate_placeholders()
		# Stores the position of duplicate placeholders in the editing area.
		self.__mirror_dictionary = {}
		# Stores the position of placeholders in the editing area.
		self.__placeholder_dictionary = {}
		# A value that keeps track of the cursor position relative to
		# placeholders in the buffer.
		self.__index = 0
		# An index representing the last placeholder.
		self.__last_index = None
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		self.__signal_id_4 = None
		self.__status_id = None
		return

########################################################################
#
#					Navigation Methods
#
########################################################################

	def next(self):
		"""
		Jump to the next placeholder in the template.

		@param self: Reference to the TemplateProcessor instance.
		@type self: A TemplateProcessor object.
		"""
		begin_mark, end_mark, value = self.__placeholder_dictionary[self.__index]
		if begin_mark and not end_mark and value:
			# In this branch the index is most likely on the last
			# special placeholder, "cursor." Thus exit template mode.
			self.__destroy_cb(self.__manager)
			return
		# Tag the current placeholder before moving to the next one.
		begin = self.__editor.textbuffer.get_iter_at_mark(begin_mark)
		end = self.__editor.textbuffer.get_iter_at_mark(end_mark)
		self.__editor.textbuffer.remove_tag(self.__pre_modification_highlight_tag, begin, end)
		self.__editor.textbuffer.remove_tag(self.__modification_highlight_tag, begin, end)
		self.__editor.textbuffer.apply_tag(self.__post_modification_highlight_tag, begin, end)
		# Update mirrors if any.
		from operator import contains
		if contains(self.__mirror_dictionary.keys(), (begin_mark, end_mark)):
			self.__update_mirrors()
		from SCRIBES.cursor import move_view_to_cursor
		self.__index = self.__calculate_next_index()
		# Jump to, or select, the placeholder associated with the new
		# index.
		if self.__index:
			begin_mark, end_mark, value = self.__placeholder_dictionary[self.__index]
			if begin_mark and end_mark and value:
				# In this branch the placeholder is not "cursor"
				begin = self.__editor.textbuffer.get_iter_at_mark(begin_mark)
				end = self.__editor.textbuffer.get_iter_at_mark(end_mark)
				self.__editor.textbuffer.select_range(begin, end)
			else:
				# In this branch the placeholder is likely "cursor"
				iterator = self.__editor.textbuffer.get_iter_at_mark(begin_mark)
				self.__editor.textbuffer.place_cursor(iterator)
			move_view_to_cursor(self.__editor.textview)
			from i18n import msg0003
			self.__editor.feedback.update_status_message(msg0003, "yes")
		else:
			iterator = self.__editor.textbuffer.get_iter_at_mark(self.__end_template_mark)
			self.__editor.textbuffer.place_cursor(iterator)
			move_view_to_cursor(self.__editor.textview)
			self.__destroy_cb(self.__manager)
		return

	def previous(self):
		"""
		Move to the previous placeholder if possible.

		@param self: Reference to the TemplateProcessor instance.
		@type self: A TemplateProcessor object.
		"""
		# Tag the current placeholder before moving to the next one.
		begin_mark, end_mark, value = self.__placeholder_dictionary[self.__index]
		if begin_mark and end_mark:
			from operator import contains
			if contains(self.__mirror_dictionary.keys(), (begin_mark, end_mark)):
				self.__update_mirrors()
			begin = self.__editor.textbuffer.get_iter_at_mark(begin_mark)
			end = self.__editor.textbuffer.get_iter_at_mark(end_mark)
			self.__editor.textbuffer.remove_tag(self.__pre_modification_highlight_tag, begin, end)
			self.__editor.textbuffer.remove_tag(self.__modification_highlight_tag, begin, end)
			self.__editor.textbuffer.apply_tag(self.__post_modification_highlight_tag, begin, end)
		# Determine the previous placeholder index.
		self.__index = self.__calculate_previous_index()
		from operator import is_
		if is_(self.__index, None): return
		# Select the previous placeholder.
		begin_mark, end_mark, value = self.__placeholder_dictionary[self.__index]
		if begin_mark and end_mark and value:
			begin = self.__editor.textbuffer.get_iter_at_mark(begin_mark)
			end = self.__editor.textbuffer.get_iter_at_mark(end_mark)
			self.__editor.textbuffer.select_range(begin, end)
		else:
			iterator = self.__editor.textbuffer.get_iter_at_mark(begin_mark)
			self.__editor.textbuffer.place_cursor(iterator)
		from SCRIBES.cursor import move_view_to_cursor
		move_view_to_cursor(self.__editor.textview)
		from i18n import msg0004
		self.__editor.feedback.update_status_message(msg0004, "yes")
		return

	def __get_duplicate_placeholders(self):
		from operator import gt
		mirrors = [placeholder.strip("${}") for placeholder in self.__placeholders if gt(self.__placeholders.count(placeholder), 1)]
		return mirrors

	def __expand_special_placeholders(self):
		"""
		Replace special placeholders in the text editor's buffer with
		their determined value and tag them.

		@param self: Reference to the TemplateProcessor instance.
		@type self: A TemplateProcessor object.
		"""
		# Search for special placeholders, replace them with their
		# determined value and tag them.
		start_position = self.__editor.textbuffer.get_iter_at_mark(self.__start_template_mark)
		from gtk import TEXT_SEARCH_VISIBLE_ONLY
		from utils import replace_special_placeholder
		for placeholder in self.__special_placeholders:
			end_position = self.__editor.textbuffer.get_iter_at_mark(self.__end_template_mark)
			begin, end = start_position.forward_search(placeholder, TEXT_SEARCH_VISIBLE_ONLY, end_position)
			self.__editor.textbuffer.place_cursor(begin)
			self.__editor.textbuffer.delete(begin, end)
			new_placeholder = replace_special_placeholder(placeholder)
			cursor_position = self.__editor.get_cursor_position()
			mark = self.__editor.mark(cursor_position)
			self.__editor.textbuffer.insert_with_tags(cursor_position, new_placeholder,
												self.__special_highlight_tag)
			start_position = self.__editor.textbuffer.get_iter_at_mark(mark)
		return

	def __mark_and_tag_placeholders(self):
		"""
		Mark the position of placeholders in the text editor's buffer
		and highlight them.

		@param self: Reference to the TemplateProcessor instance.
		@type self: A TemplateProcessor object.
		"""
		from operator import eq, contains, not_
		editor = self.__editor
		textbuffer = editor.textbuffer
		if self.__special_placeholders:
			is_not_special = lambda placeholder: not_(contains(self.__special_placeholders, placeholder))
			placeholders = filter(is_not_special, self.__placeholders)
		else:
			placeholders = self.__placeholders
		start_position = textbuffer.get_iter_at_mark(self.__start_template_mark)
		from gtk import TEXT_SEARCH_VISIBLE_ONLY
		# Search for special placeholders, replace them with their
		# determined value and tag them.
		count = 0
		mirror_list = []
		for placeholder in placeholders:
			end_position = textbuffer.get_iter_at_mark(self.__end_template_mark)
			begin, end = start_position.forward_search(placeholder, TEXT_SEARCH_VISIBLE_ONLY, end_position)
			textbuffer.place_cursor(begin)
			textbuffer.delete(begin, end)
			cursor_position = editor.get_cursor_position()
			placeholder = placeholder.strip("${}")
			if eq(placeholder, "cursor"):
				emark = textbuffer.create_mark(None, cursor_position, False)
				emark.set_visible(True)
				self.__placeholder_dictionary["cursor"] = (emark,)
			else:
				bmark = textbuffer.create_mark(None, cursor_position, True)
				emark = textbuffer.create_mark(None, cursor_position, False)
				self.__placeholder_dictionary[count] = (bmark, emark, True)
				if placeholder:
					if self.__mirror_list:
						if contains(self.__mirror_list, placeholder):
							self.__mirror_dictionary[(bmark, emark)] = placeholder
							if contains(mirror_list, placeholder):
								self.__placeholder_dictionary[count] = (bmark, emark, False)
							else:
								mirror_list.append(placeholder)
				else:
					placeholder = " "
				textbuffer.insert_with_tags(cursor_position,
					placeholder, self.__pre_modification_highlight_tag)
				count += 1
			start_position = textbuffer.get_iter_at_mark(emark)
		return

	def __determine_last_placeholder(self):
		"""
		Set the index of the last placeholder.

		@param self: Reference to the TemplateProcessor instance.
		@type self: A TemplateProcessor object.
		"""
		if self.__placeholder_dictionary.has_key("cursor"):
			cursor_marker = self.__placeholder_dictionary["cursor"]
			from operator import eq, gt
			if eq(len(self.__placeholder_dictionary), 1):
				# In this branch cursor is the only placeholder.
				del self.__placeholder_dictionary["cursor"]
				self.__last_index = 0
				self.__placeholder_dictionary[self.__last_index] = cursor_marker[0], None, True
			elif gt(len(self.__placeholder_dictionary), 1):
				del self.__placeholder_dictionary["cursor"]
				self.__last_index = max(self.__placeholder_dictionary.keys()) + 1
				self.__placeholder_dictionary[self.__last_index] = cursor_marker[0], None, True
		else:
			self.__last_index = max(self.__placeholder_dictionary.keys())
			if self.__mirror_list:
				navigating_index_list = []
				for key, value in self.__placeholder_dictionary.items():
					if value[2]: navigating_index_list.append(key)
				if navigating_index_list: self.__last_index = max(navigating_index_list)
		return

	def __calculate_next_index(self):
		"""
		Determine the next placeholder index to jump to.

		@param self: Reference to the TemplateProcessor instance.
		@type self: A TemplateProcessor object.

		@return: The next placeholder index to jump to.
		@rtype: An Integer object.
		"""
		indexes = self.__placeholder_dictionary.keys()
		indexes.sort()
		from operator import gt
		for index in indexes:
			if gt(index, self.__index):
				if self.__placeholder_dictionary[index][2]:
					return index
		return None

	def __calculate_previous_index(self):
		"""
		Determine the previous placeholder index to jump to.

		@param self: Reference to the TemplateProcessor instance.
		@type self: A TemplateProcessor object.

		@return: The next placeholder index to jump to.
		@rtype: An Integer object.
		"""
		indexes = self.__placeholder_dictionary.keys()
		indexes.sort()
		indexes.reverse()
		from operator import not_, lt
		for index in indexes:
			if not_(self.__index):
				self.__index = max(indexes)
				if self.__placeholder_dictionary[self.__index][2]:
					return self.__index
			if lt(index, self.__index):
				if self.__placeholder_dictionary[index][2]:
					return index
		return None

	def __update_index(self, begin_mark, end_mark):
		"""
		Update the current placeholder index.

		@param self: Reference to the TemplateProcessor instance.
		@type self: A TemplateProcessor object.
		"""
		for value in xrange(self.__last_index + 1):
			marks = self.__placeholder_dictionary[value]
			if begin_mark in marks and end_mark in marks:
				self.__index = value
				break
		return

	def __select_first_placeholder(self):
		"""
		Select the first placeholder.

		@param self: Reference to the TemplateProcessor instance.
		@type self: A TemplateProcessor object.
		"""
		begin_mark, end_mark, value = self.__placeholder_dictionary[0]
		if begin_mark and end_mark and value:
			begin = self.__editor.textbuffer.get_iter_at_mark(begin_mark)
			end = self.__editor.textbuffer.get_iter_at_mark(end_mark)
			self.__editor.textbuffer.select_range(begin, end)
		return

	def __update_mirrors(self):
		"""
		Update other mirrors when one mirror is edited.

		@param self: Reference to the TemplateProcessor instance.
		@type self: A TemplateProcessor object.
		"""
		begin_mark, end_mark, value = self.__placeholder_dictionary[self.__index]
		mirror_list = []
		from operator import eq, ne, not_
		for key, value in self.__mirror_dictionary.items():
			if eq(value, self.__mirror_dictionary[(begin_mark, end_mark)]):
				if ne(key, (begin_mark, end_mark)):
					mirror_list.append(key)
		if not_(mirror_list): return
		self.__editor.textbuffer.handler_block(self.__signal_id_4)
		for placeholder in mirror_list:
			begin_position = self.__editor.textbuffer.get_iter_at_mark(begin_mark)
			end_position = self.__editor.textbuffer.get_iter_at_mark(end_mark)
			begin = self.__editor.textbuffer.get_iter_at_mark(placeholder[0])
			end = self.__editor.textbuffer.get_iter_at_mark(placeholder[1])
			self.__editor.textbuffer.delete(begin, end)
			begin_position = self.__editor.textbuffer.get_iter_at_mark(begin_mark)
			end_position = self.__editor.textbuffer.get_iter_at_mark(end_mark)
			begin = self.__editor.textbuffer.get_iter_at_mark(placeholder[0])
			end = self.__editor.textbuffer.get_iter_at_mark(placeholder[1])
			self.__editor.textbuffer.insert_range(begin, begin_position, end_position)
			begin_position = self.__editor.textbuffer.get_iter_at_mark(begin_mark)
			end_position = self.__editor.textbuffer.get_iter_at_mark(end_mark)
			begin = self.__editor.textbuffer.get_iter_at_mark(placeholder[0])
			end = self.__editor.textbuffer.get_iter_at_mark(placeholder[1])
			self.__editor.textbuffer.remove_tag(self.__pre_modification_highlight_tag, begin, end)
			self.__editor.textbuffer.remove_tag(self.__modification_highlight_tag, begin, end)
			self.__editor.textbuffer.apply_tag(self.__post_modification_highlight_tag, begin, end)
		self.__editor.textbuffer.handler_unblock(self.__signal_id_4)
		return

########################################################################
#
#						Tags for Placeholders
#
########################################################################

	def __create_pre_modification_tag(self):
		"""
		Create a tag for unmodified placeholders.

		@param self: Reference to the TemplateProcessor.
		@type self: A TemplateProcessor object.

		@return: A highlight tag.
		@rtype: A gtk.TextTag object.
		"""
		highlight_tag = self.__editor.textbuffer.create_tag()
		highlight_tag.set_property("background", "yellow")
		highlight_tag.set_property("foreground", "blue")
		from pango import WEIGHT_HEAVY
		highlight_tag.set_property("weight", WEIGHT_HEAVY)
		return highlight_tag

	def __create_post_modification_tag(self):
		"""
		Create a tag for modified placeholders.

		@param self: Reference to the TemplateProcessor.
		@type self: A TemplateProcessor object.

		@return: A highlight tag.
		@rtype: A gtk.TextTag object.
		"""
		highlight_tag = self.__editor.textbuffer.create_tag()
		highlight_tag.set_property("foreground", "blue")
		from pango import WEIGHT_HEAVY, STYLE_ITALIC
		highlight_tag.set_property("weight", WEIGHT_HEAVY)
		highlight_tag.set_property("style", STYLE_ITALIC)
		return highlight_tag

	def __create_modification_tag(self):
		"""
		Create a tag for placeholders being modified.

		@param self: Reference to the TemplateProcessor.
		@type self: A TemplateProcessor object.

		@return: A highlight tag.
		@rtype: A gtk.TextTag object.
		"""
		highlight_tag = self.__editor.textbuffer.create_tag()
		highlight_tag.set_property("background", "#ADD8E6")
		highlight_tag.set_property("foreground", "#CB5A30")
		from pango import WEIGHT_HEAVY
		highlight_tag.set_property("weight", WEIGHT_HEAVY)
		return highlight_tag

	def __create_special_tag(self):
		"""
		Create a tag for special placeholders.

		@param self: Reference to the TemplateProcessor.
		@type self: A TemplateProcessor object.

		@return: A highlight tag.
		@rtype: A gtk.TextTag object.
		"""
		highlight_tag = self.__editor.textbuffer.create_tag()
		highlight_tag.set_property("foreground", "pink")
		from pango import WEIGHT_HEAVY
		highlight_tag.set_property("weight", WEIGHT_HEAVY)
		return highlight_tag

########################################################################
#
#					Event and Signal Handlers
#
########################################################################

	def __cursor_moved_cb(self, editor):
		"""
		Handles callback when the "cursor-moved" signal is emitted.

		@param self: Reference to the class instance.
		@type self: A class object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		# Destroy this template object if the cursor moves outside the
		# template region.
		cursor_position = editor.get_cursor_position()
		begin_position = self.__editor.textbuffer.get_iter_at_mark(self.__start_template_mark)
		end_position = self.__editor.textbuffer.get_iter_at_mark(self.__end_template_mark)
		from operator import not_
		if not_(cursor_position.in_range(begin_position, end_position)):
			if cursor_position.equal(begin_position) and cursor_position.equal(end_position):
				self.__destroy_cb(self.__manager)
			elif cursor_position.equal(end_position):
				pass
			else:
				self.__destroy_cb(self.__manager)
		return

	def __insert_text_cb(self, textbuffer, iterator, text, length):
		"""
		Handles callback when the "insert-text" signal is emitted.

		@param self: Reference to the TemplateProcessor instance.
		@type self: A TemplateProcessor object.

		@param textbuffer: The text editor's buffer.
		@type textbuffer: A ScribesTextBuffer object.

		@param iterator: The position to insert text.
		@type iterator: A gtk.TextIter object.

		@param text: Text to be entered in the text editor's buffer.
		@type text: A String object.

		@param length: The length of text to be entered in the buffer.
		@type length: An Integer object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		from operator import ne, contains
		if ne(self.__index, self.__last_index):
			# Ignore every other index other than the last one.
			return False
		begin_mark, end_mark, value = self.__placeholder_dictionary[self.__index]
		if contains(self.__mirror_dictionary.keys(), (begin_mark, end_mark)):
			# Ignore mirrors.
			return False
		# Exit template mode when the user types over the last placeholder.
		if begin_mark and end_mark and value:
			begin = self.__editor.textbuffer.get_iter_at_mark(begin_mark)
			end = self.__editor.textbuffer.get_iter_at_mark(end_mark)
			if iterator.in_range(begin, end) or iterator.equal(begin) or iterator.equal(end):
				self.__destroy_cb(self.__manager)
		else:
			iterator = self.__editor.textbuffer.get_iter_at_mark(begin_mark)
			if iterator.equal(iterator):
				self.__destroy_cb(self.__manager)
		return False

	def __get_modified_placeholder(self):
		"""
		Return the position of a placeholder under modification.

		@param self: Reference to the TemplateProcessor instance.
		@type self: A TemplateProcessor object.

		@return: The position of the placeholder being modified.
		@rtype: A List object.
		"""
		placeholders = self.__placeholder_dictionary.values()
		for placeholder in placeholders:
			if placeholder[0] and not placeholder[1] and placeholder[2]:
				# Ignore the "cursor" special placeholder.
				continue
			begin = self.__editor.textbuffer.get_iter_at_mark(placeholder[0])
			end = self.__editor.textbuffer.get_iter_at_mark(placeholder[1])
			iterator = self.__editor.get_cursor_position()
			if iterator.in_range(begin, end) or iterator.equal(begin) or iterator.equal(end):
				return placeholder
		return None

	def __update_index(self, begin_mark, end_mark):
		"""
		Update the current placeholder index.

		@param self: Reference to the TemplateProcessor instance.
		@type self: A TemplateProcessor object.
		"""
		for value in xrange(self.__last_index + 1):
			marks = self.__placeholder_dictionary[value]
			if begin_mark in marks and end_mark in marks:
				self.__index = value
				break
		return

	def __insert_text_after_cb(self, textbuffer, iterator, text, length):
		"""
		Handles callback when the "insert-text" signal is emitted.

		@param self: Reference to the TemplateProcessor instance.
		@type self: A TemplateProcessor object.

		@param textbuffer: The text editor's buffer.
		@type textbuffer: A ScribesTextBuffer object.

		@param iterator: The position to insert text.
		@type iterator: A gtk.TextIter object.

		@param text: Text to be entered in the text editor's buffer.
		@type text: A String object.

		@param length: The length of text to be entered in the buffer.
		@type length: An Integer object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		# Check if a placeholder is being modified.
		placeholder = self.__get_modified_placeholder()
		from operator import not_
		if not_(placeholder): return False
		# Tag placeholder that is being modified.
		begin_position = self.__editor.textbuffer.get_iter_at_mark(placeholder[0])
		end_position = self.__editor.textbuffer.get_iter_at_mark(placeholder[1])
		self.__editor.textbuffer.apply_tag(self.__modification_highlight_tag,
											begin_position, end_position)
		self.__update_index(placeholder[0], placeholder[1])
		return False

	def __destroy_cb(self, manager):
		from SCRIBES.utils import delete_attributes, disconnect_signal
		self.__manager.emit("template-destroyed", self)
		disconnect_signal(self.__signal_id_1, manager)
		disconnect_signal(self.__signal_id_2, self.__editor)
		disconnect_signal(self.__signal_id_3, self.__editor.textbuffer)
		disconnect_signal(self.__signal_id_4, self.__editor.textbuffer)
		# Remove all tags associated with this template object.
		begin_position = self.__editor.textbuffer.get_iter_at_mark(self.__start_template_mark)
		end_position = self.__editor.textbuffer.get_iter_at_mark(self.__end_template_mark)
		self.__editor.textbuffer.remove_tag(self.__pre_modification_highlight_tag,
											begin_position, end_position)
		self.__editor.textbuffer.remove_tag(self.__post_modification_highlight_tag,
											begin_position, end_position)
		self.__editor.textbuffer.remove_tag(self.__modification_highlight_tag,
											begin_position, end_position)
		self.__editor.textbuffer.remove_tag(self.__special_highlight_tag,
											begin_position, end_position)
		self.__editor.delete_mark(self.__start_template_mark)
		self.__editor.delete_mark(self.__end_template_mark)
		for positions in self.__placeholder_dictionary.values():
			try:
				self.__editor.delete_mark(positions[0])
				self.__editor.delete_mark(positions[1])
			except:
				pass
		self.__mirror_dictionary.clear()
		self.__placeholder_dictionary.clear()
		self.__editor.feedback.unset_modal_message(self.__status_id)
		from i18n import msg0002
		self.__editor.feedback.update_status_message(msg0002, "yes")
		delete_attributes(self)
		self = None
		del self
		return False
