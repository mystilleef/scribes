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
This module documents a class that highlights regions within pair
bracket characters. Characters currently affected are "(", ")", "[", "]"
"<", ">", "{" and "}". More pair characters will be added if the need
arises.


@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class Highlighter(object):
	"""
	The class implements and object that highlights regions within pair
	characters. The following characters are supported "(", ")", "[", "]"
	"<", ">", "{" and "}"
	"""

	def __init__(self, editor):
		"""
		Initialize object.

		@param self: Reference to the Highlighter instance.
		@type self: A Highlighter object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(editor)
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__compile_method, priority=PRIORITY_LOW)
		self.__signal_id_1 = editor.connect("cursor-moved", self.__cursor_moved_cb)
		self.__signal_id_2 = editor.textbuffer.connect("apply-tag", self.__apply_tag_cb)
		self.__signal_id_3 = editor.textbuffer.connect("remove-tag", self.__remove_tag_cb)
		self.__signal_id_4 = editor.connect("loading-document", self.__generic_highlight_off_cb)
		self.__signal_id_5 = editor.connect("loaded-document", self.__generic_highlight_on_cb)
		self.__signal_id_6 = editor.connect("enable-readonly", self.__generic_highlight_off_cb)
		self.__signal_id_7 = editor.connect("disable-readonly", self.__generic_highlight_on_cb)
		self.__signal_id_8 = editor.connect("load-error", self.__generic_highlight_on_cb)
		self.__client.notify_add("/apps/scribes/scope_highlight_color", self.__highlight_cb)

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the Highlighter instance.
		@type self: A Highlighter object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__client = editor.gconf_client
		self.__can_highlight = True
		self.__buffer_is_tagged = False
		self.__highlight_tag = self.__create_highlight_tag()
		from gtksourceview import source_iter_find_matching_bracket
		self.__match = source_iter_find_matching_bracket
		self.__start_mark = None
		self.__end_mark = None
		self.__start_characters = ("(", "[", "<", "{")
		self.__end_characters = (")", "]", ">", "}")
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		return

########################################################################
#
#						Public Method
#
########################################################################

	def destroy(self):
		"""
		Destroy instance of this class.

		@param self: Reference to the Highlighter instance.
		@type self: A Highlighter object.
		"""
		self.__destroy()
		return

########################################################################
#
#						Helper Methods
#
########################################################################

	def __highlight_region(self):
		"""
		Highlight region between pair characters.

		@param self: Reference to the Highlighter instance.
		@type self: A Highlighter object.
		"""
		textbuffer = self.__editor.textbuffer
		from operator import not_, truth
		if truth(self.__buffer_is_tagged):
			begin = textbuffer.get_iter_at_mark(self.__start_mark)
			end = textbuffer.get_iter_at_mark(self.__end_mark)
			textbuffer.remove_tag(self.__highlight_tag, begin, end)
		iterator = textbuffer.get_iter_at_mark(textbuffer.get_insert())
		if not_(self.__match(iterator)): return False
		cursor_iter = textbuffer.get_iter_at_mark(textbuffer.get_insert())
		try:
			start, end = self.__get_boundary(cursor_iter, iterator)
			textbuffer.apply_tag(self.__highlight_tag, start, end)
		except:
			pass
		return False

	def __get_boundary(self, citerator, iterator):
		"""
		Return the region of pair characters.

		@param self: Reference to the Highlighter instance.
		@type self: A Highlighter object.

		@param citerator: The position of the cursor.
		@type citerator: A gtk.TextIter object.

		@param iterator: The position of a matching bracket.
		@type iterator: A gtk.TextIter object.

		@return: A pair of iterators representing the position of matching
			brackets or nothing.
		@rtype: A Tuple object.
		"""
		# The madness going on over here is as a result of the strangeness
		# of the GtkSourceView API. If your head hurts, kindly move along.
		from operator import truth
		if truth(self.__is_start_character(citerator.get_char())):
			iterator.forward_char()
			return citerator, iterator
		if truth(self.__is_end_character(citerator.get_char())):
			citerator.backward_char()
			if truth(self.__is_end_character(citerator.get_char())):
				self.__match(citerator)
				textbuffer = self.__editor.textbuffer
				cursor_iter = textbuffer.get_iter_at_mark(textbuffer.get_insert())
				return citerator, cursor_iter
			citerator.forward_char()
			return None
		citerator.backward_char()
		if truth(self.__is_start_character(citerator.get_char())): return None
		citerator.forward_char()
		return citerator, iterator

	def __is_start_character(self, character):
		"""
		Whether or not character is an openning pair character.

		@param self: Reference to the Highlighter instance.
		@type self: A Highlighter object.

		@param character: A character in the buffer.
		@type character: A String object.

		@return: True if character is an openning pair character.
		@rtype: A Boolean object.
		"""
		if character in self.__start_characters: return True
		return False

	def __is_end_character(self, character):
		"""
		Whether or not character is a closing pair character.

		@param self: Reference to the Highlighter instance.
		@type self: A Highlighter object.

		@param character: A character in the buffer.
		@type character: A String object.

		@return: True if character is a closing pair character.
		@rtype: A Boolean object.
		"""
		if character in self.__end_characters: return True
		return False

	def __create_highlight_tag(self):
		"""
		Create the a highlight tag.

		@param self: Reference to the LexicalScopeHighlight instance.
		@type self: A LexicalScopeHighlight object.

		@return: A region highlight tag.
		@rtype: A gtk.TextTag object.
		"""
		from gtk import TextTag
		tag = TextTag("lexical_scope_tag")
		color = "#cfcfcf"
		if self.__client.get("/apps/scribes/scope_highlight_color"):
			color = self.__client.get_string("/apps/scribes/scope_highlight_color")
		self.__editor.textbuffer.get_tag_table().add(tag)
		tag.set_property("background", color)
		return tag

	def __destroy(self):
		"""
		Destroy instance of this object.

		@param self: Reference to the Highlighter instance.
		@type self: A Highlighter object.
		"""
		self.__editor.textbuffer.get_tag_table().remove(self.__highlight_tag)
		from SCRIBES.utils import delete_attributes, disconnect_signal
		disconnect_signal(self.__signal_id_1, self.__editor)
		disconnect_signal(self.__signal_id_2, self.__editor.textbuffer)
		disconnect_signal(self.__signal_id_3, self.__editor.textbuffer)
		disconnect_signal(self.__signal_id_4, self.__editor)
		disconnect_signal(self.__signal_id_5, self.__editor)
		disconnect_signal(self.__signal_id_6, self.__editor)
		disconnect_signal(self.__signal_id_7, self.__editor)
		disconnect_signal(self.__signal_id_8, self.__editor)
		from operator import truth
		if truth(self.__start_mark):
			if truth(self.__start_mark.get_deleted()):
				self.__editor.textbuffer.delete_mark(self.__start_mark)
		if truth(self.__end_mark):
			if truth(self.__end_mark.get_deleted()):
				self.__editor.textbuffer.delete_mark(self.__end_mark)
		delete_attributes(self)
		self = None
		del self
		return

	def __compile_method(self):
		"""
		Use psyco, the Python performance optimization compiler, to
		compile a method for performance.

		@param self: Reference to the Highlighter instance.
		@type self: A Highlighter object.
		"""
		try:
			from psyco import bind
			bind(self.__highlight_region)
			bind(self.__get_boundary)
		except:
			pass
		return False

########################################################################
#
#						Signal and Event Handlers
#
########################################################################

	def __cursor_moved_cb(self, editor):
		"""
		Handles callback when the "cursor-moved" signal is emitted.

		@param self: Reference to the Highlighter instance.
		@type self: A Highlighter object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		from operator import not_
		if not_(self.__can_highlight): return
		from gobject import idle_add, source_remove
		try:
			source_remove(self.__cursor_moved_id)
		except:
			pass
		self.__cursor_moved_id = idle_add(self.__highlight_region)
		return

	def __apply_tag_cb(self, textbuffer, tag, start, end):
		"""
		Handles callback when the "apply-tag" signal is emitted.

		@param self: Reference to the ScribesTextBuffer instance.
		@type self: A ScribesTextBuffer object.

		@param textbuffer: The text editor's buffer.
		@type textbuffer: A ScribesTextBuffer object.

		@param tag: A tag in the text editor's buffer.
		@type tag: A gtk.TextTag object.

		@param start: The position of the begining of the tag.
		@type start: A gtk.TextIter object.

		@param end: The position of the end of the tag.
		@type end: A gtk.TextIter object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		from operator import ne, is_
		if ne(tag, self.__highlight_tag): return False
		textbuffer = self.__editor.textbuffer
		if is_(self.__start_mark, None):
			self.__start_mark = textbuffer.create_mark(None, start, True)
		if is_(self.__end_mark, None):
			self.__end_mark = textbuffer.create_mark(None, end, False)
		textbuffer.move_mark(self.__start_mark, start)
		textbuffer.move_mark(self.__end_mark, end)
		self.__buffer_is_tagged = True
		return True

	def __remove_tag_cb(self, textbuffer, tag, start, end):
		"""
		Handles callback when the "remove-tag" signal is emitted.

		@param self: Reference to the ScribesTextBuffer instance.
		@type self: A ScribesTextBuffer object.

		@param textbuffer: The text editor's buffer.
		@type textbuffer: A ScribesTextBuffer object.

		@param tag: A tag in the text editor's buffer.
		@type tag: A gtk.TextTag object.

		@param start: The position of the begining of the tag.
		@type start: A gtk.TextIter object.

		@param end: The position of the end of the tag.
		@type end: A gtk.TextIter object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		from operator import ne
		if ne(tag, self.__highlight_tag): return False
		self.__buffer_is_tagged = False
		return True

	def __generic_highlight_off_cb(self, *args):
		"""
		A generic callback to disable scope highlights.

		@param self: Reference to the Highlighter instance.
		@type self: A Highlighter object.

		@param *args: Irrelevant arguments.
		@type *args: A List object.
		"""
		self.__can_highlight = False
		begin, end = self.__editor.textbuffer.get_bounds()
		self.__editor.textbuffer.remove_tag(self.__highlight_tag, begin, end)
		return

	def __generic_highlight_on_cb(self, *args):
		"""
		A generic callback to enable scope highlights.

		@param self: Reference to the Highlighter instance.
		@type self: A Highlighter object.

		@param *args: Irrelevant arguments.
		@type *args: A List object.
		"""
		self.__can_highlight = True
		from gobject import idle_add, source_remove
		try:
			source_remove(self.__generic_id)
		except:
			pass
		self.__generic_id = idle_add(self.__highlight_region)
		return

########################################################################
#
#						GConf Signal Handlers
#
########################################################################

	def __highlight_cb(self, client, cnxn_id, entry, data):
		"""
		Handles callback #FIXME: yeap

		@param self: Reference to the LexicalScopeHighlight instance.
		@type self: A LexicalScopeHighlight object.

		@param client: A client used to query the GConf daemon and database
		@type client: A gconf.Client object.

		@param cnxn_id: The identification number for the GConf client.
		@type cnxn_id: An Integer object.

		@param entry: An entry from the GConf database.
		@type entry: A gconf.Entry object.

		@param data: Optional data
		@type data: Any type object.
		"""
		textbuffer = self.__editor.textbuffer
		begin, end = textbuffer.get_bounds()
		textbuffer.remove_tag(self.__highlight_tag, begin, end)
		color = self.__client.get_string("/apps/scribes/scope_highlight_color")
		self.__highlight_tag.set_property("background", color)
		from gobject import idle_add, source_remove
		try:
			source_remove(self.__highlight_id)
		except:
			pass
		self.__highlight_id = idle_add(self.__highlight_region)
		return
