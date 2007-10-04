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
This module documents a class that performs bracket completion operations
for the text editor.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class BracketManager(object):
	"""
	This class implements bracket completion operations for the text
	editor. Closing characters for most pair characters are
	automatically inserted into the editing area.
	"""

	def __init__(self, editor):
		"""
		Initialize object.

		@param self: Reference to the BracketManager instance.
		@type self: A BracketManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(editor)
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__compile_methods, priority=PRIORITY_LOW)
		self.__check_mimetype()
		self.__signal_id_1 = editor.textview.connect("key-press-event", self.__key_press_event_cb)
		self.__signal_id_2 = editor.connect("cursor-moved", self.__cursor_moved_cb)
		self.__signal_id_3 = editor.connect("loaded-document", self.__loaded_document_cb)

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the BracketManager instance.
		@type self: A BracketManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		from gtksourceview import source_iter_find_matching_bracket
		self.__match = source_iter_find_matching_bracket
		self.__monitor_list = []
		self.__escape_character = "\\"
		from gtk import keysyms
		self.__open_pair_characters = [keysyms.quotedbl,
			keysyms.braceleft, keysyms.bracketleft,
			keysyms.parenleft, keysyms.leftdoublequotemark,
			keysyms.guillemotleft, keysyms.guillemotright,
			keysyms.leftsinglequotemark, keysyms.leftmiddlecurlybrace,
			keysyms.lowleftcorner, keysyms.topleftparens,
			keysyms.topleftsqbracket, keysyms.upleftcorner,
			keysyms.botleftparens, keysyms.botleftsqbracket,
			keysyms.apostrophe]
		self.__open_pair_characters_for_enclosement = self.__open_pair_characters + [keysyms.less,			keysyms.apostrophe]
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		self.__signal_id_4 = None
		return

########################################################################
#
#							Public Methods
#
########################################################################

	def destroy(self):
		"""
		Destroy instance of this class.

		@param self: Reference to the BracketManager instance.
		@type self: A BracketManager object.
		"""
		self.__destroy()
		return

########################################################################
#
#							Helper Methods
#
########################################################################

	def __insert_closing_pair_character(self, keyval):
		"""
		Insert closing pair characters into the text editor's buffer.

		@param self: Reference to the BracketManager instance.
		@type self: A BracketManager object.

		@param keyval: A value representing a keyboard symbol
		@type keyval: An Integer object.
		"""
		from operator import eq, truth
		from gtk import keysyms
		if eq(keyval, keysyms.quotedbl):
			self.__insert_pair_characters(keyval, keysyms.quotedbl)
		elif eq(keyval, keysyms.braceleft):
			self.__insert_pair_characters(keyval, keysyms.braceright)
		elif eq(keyval, keysyms.bracketleft):
			self.__insert_pair_characters(keyval, keysyms.bracketright)
		elif eq(keyval, keysyms.parenleft):
			self.__insert_pair_characters(keyval, keysyms.parenright)
		elif eq(keyval, keysyms.leftdoublequotemark):
			self.__insert_pair_characters(keyval, keysyms.righdoublequotemark)
		elif eq(keyval, keysyms.guillemotleft):
			self.__insert_pair_characters(keyval, keysyms.guillemotright)
		elif eq(keyval, keysyms.guillemotright):
			self.__insert_pair_characters(keyval, keysyms.guillemotleft)
		elif eq(keyval , keysyms.leftsinglequotemark):
			self.__insert_pair_characters(keyval, keysyms.rightsinglequotemark)
		elif eq(keyval , keysyms.leftmiddlecurlybrace):
			self.__insert_pair_characters(keyval, keysyms.rightmiddlecurlybrace)
		elif eq(keyval , keysyms.lowleftcorner):
			self.__insert_pair_characters(keyval, keysyms.lowrightcorner)
		elif eq(keyval , keysyms.topleftparens):
			self.__insert_pair_characters(keyval, keysyms.toprightparens)
		elif eq(keyval , keysyms.topleftsqbracket):
			self.__insert_pair_characters(keyval, keysyms.toprightsqbracket)
		elif eq(keyval , keysyms.upleftcorner):
			self.__insert_pair_characters(keyval, keysyms.uprightcorner)
		elif eq(keyval , keysyms.botleftparens):
			self.__insert_pair_characters(keyval, keysyms.botrightparens)
		elif eq(keyval , keysyms.botleftsqbracket):
			self.__insert_pair_characters(keyval, keysyms.botrightsqbracket)
		elif eq(keyval , keysyms.less):
			self.__insert_pair_characters(keyval, keysyms.greater)
		elif eq(keyval , keysyms.dollar):
			self.__insert_pair_characters(keyval, keysyms.dollar)
		elif eq(keyval , keysyms.apostrophe):
			if truth(self.__can_insert_apostrophe()):
				self.__insert_pair_characters(keyval, keysyms.apostrophe)
			else:
				self.__insert_apostrophe()
		return

	def __insert_pair_characters(self, open_keyval, close_keyval):
		"""
		Insert pair characters into the text editor's buffer.

		@param self: Reference to the BracketManager instance.
		@type self: A BracketManager object.

		@param open_keyval: A value representing the openning character.
		@type open_keyval: An Integer object.

		@param close_keyval: A value representing the closing character.
		@type close_keyval: An Integer object.
		"""
		textbuffer = self.__editor.textbuffer
		from gtk.gdk import keyval_to_unicode
		utf8_open_character = unichr(keyval_to_unicode(open_keyval)).encode("utf-8")
		utf8_closing_character = unichr(keyval_to_unicode(close_keyval)).encode("utf-8")
		from SCRIBES.cursor import get_cursor_iterator
		cursor_position = get_cursor_iterator(textbuffer)
		begin_mark = textbuffer.create_mark(None, cursor_position, True)
		textbuffer.begin_user_action()
		textbuffer.insert_at_cursor(utf8_open_character+utf8_closing_character)
		textbuffer.end_user_action()
		from SCRIBES.cursor import get_cursor_iterator
		cursor_position = get_cursor_iterator(textbuffer)
		end_mark = textbuffer.create_mark(None, cursor_position, False)
		cursor_position.backward_char()
		textbuffer.place_cursor(cursor_position)
		self.__monitor_list.append((close_keyval, (begin_mark, end_mark)))
		from i18n import msg0001
		self.__editor.feedback.update_status_message(msg0001, "succeed")
		return

	def __enclose_selection(self, keyval):
		"""
		Enclose selection in pair characters.

		@param self: Reference to the BracketManager instance.
		@type self: A BracketManager object.

		@param keyval: The value of a pair character.
		@type keyval: An Integer object.
		"""
		from gtk import keysyms
		from operator import eq
		if eq(keyval, keysyms.quotedbl):
			self.__insert_enclosed_selection(keysyms.quotedbl, keysyms.quotedbl)
		elif eq(keyval, keysyms.braceleft):
			self.__insert_enclosed_selection(keysyms.braceleft, keysyms.braceright)
		elif eq(keyval, keysyms.bracketleft):
			self.__insert_enclosed_selection(keysyms.bracketleft, keysyms.bracketright)
		elif eq(keyval, keysyms.parenleft):
			self.__insert_enclosed_selection(keysyms.parenleft, keysyms.parenright)
		elif eq(keyval, keysyms.leftdoublequotemark):
			self.__insert_enclosed_selection(keysyms.leftdoublequotemark, keysyms.rightdoublequotemark)
		elif eq(keyval, keysyms.guillemotleft):
			self.__insert_enclosed_selection(keysyms.guillemotleft, keysyms.guillemotright)
		elif eq(keyval, keysyms.guillemotright):
			self.__insert_enclosed_selection(keysyms.guillemotright, keysyms.guillemotleft)
		elif eq(keyval, keysyms.leftsinglequotemark):
			self.__insert_enclosed_selection(keysyms.leftsinglequotemark, keysyms.rightsinglequotemark)
		elif eq(keyval, keysyms.leftmiddlecurlybrace):
			self.__insert_enclosed_selection(keysyms.leftmiddlecurlybrace, keysyms.rightmiddlecurlybrace)
		elif eq(keyval, keysyms.lowleftcorner):
			self.__insert_enclosed_selection(keysyms.lowleftcorner, keysyms.lowrightcorner)
		elif eq(keyval, keysyms.topleftparens):
			self.__insert_enclosed_selection(keysyms.topleftparens, keysyms.toprightparens)
		elif eq(keyval, keysyms.topleftsqbracket):
			self.__insert_enclosed_selection(keysyms.topleftsqbracket, keysyms.toprightsqbracket)
		elif eq(keyval, keysyms.upleftcorner):
			self.__insert_enclosed_selection(keysyms.upleftcorner, keysyms.uprightcorner)
		elif eq(keyval, keysyms.botleftparens):
			self.__insert_enclosed_selection(keysyms.botleftparens, keysyms.botrightparens)
		elif eq(keyval, keysyms.botleftsqbracket):
			self.__insert_enclosed_selection(keysyms.botleftsqbracket, keysyms.botrightsqbracket)
		elif eq(keyval, keysyms.less):
			self.__insert_enclosed_selection(keysyms.less, keysyms.greater)
		elif eq(keyval, keysyms.dollar):
			self.__insert_enclosed_selection(keysyms.dollar, keysyms.dollar)
		elif eq(keyval, keysyms.apostrophe):
			self.__insert_enclosed_selection(keysyms.apostrophe, keysyms.apostrophe)
		return

	def __insert_enclosed_selection(self, open_keyval, close_keyval):
		"""
		Enclose selected text in pair characters.

		@param self: Reference to the BracketManager instance.
		@type self: A BracketManager object.

		@param open_keyval: An integer representing an open pair character.
		@type open_keyval: An Integer object.

		@param close_keyval: An integer representing a close pair character.
		@type close_keyval: An Integer object.
		"""
		textbuffer = self.__editor.textbuffer
		from gtk.gdk import keyval_to_unicode
		utf8_open_character = unichr(keyval_to_unicode(open_keyval)).encode("utf-8")
		utf8_closing_character = unichr(keyval_to_unicode(close_keyval)).encode("utf-8")
		selection = textbuffer.get_selection_bounds()
		string = textbuffer.get_text(selection[0], selection[1])
		text = utf8_open_character + string + utf8_closing_character
		textbuffer.begin_user_action()
		textbuffer.delete(selection[0], selection[1])
		textbuffer.insert_at_cursor(text)
		textbuffer.end_user_action()
		from i18n import msg0002
		self.__editor.feedback.update_status_message(msg0002, "succeed")
		return

	def __move_cursor_out_of_bracket_region(self):
		"""
		Move cursor after closing pair character.

		@param self: Reference to the BracketManager instance.
		@type self: A BracketManager object.
		"""
		textbuffer = self.__editor.textbuffer
		end_mark = self.__monitor_list[-1][1][1]
		iterator = textbuffer.get_iter_at_mark(end_mark)
		textbuffer.place_cursor(iterator)
		from SCRIBES.cursor import move_view_to_cursor
		move_view_to_cursor(self.__editor.textview)
		return

	def __stop_monitoring(self):
		"""
		Stop monitoring the most recently inserted bracket region.

		@param self: Reference to the BracketManager instance.
		@type self: A BracketManager object.
		"""
		begin_mark = self.__monitor_list[-1][1][0]
		end_mark = self.__monitor_list[-1][1][1]
		from operator import not_
		if not_(begin_mark.get_deleted()):
			self.__editor.textbuffer.delete_mark(begin_mark)
		if not_(end_mark.get_deleted()):
			self.__editor.textbuffer.delete_mark(end_mark)
		del self.__monitor_list[-1]
		return

	def __remove_closing_pair_character(self):
		"""
		Remove closing pair character if it was automatically entered.

		@param self: Reference to the BracketManager instance.
		@type self: A BracketManager object.

		@return: True to handle keyboard events.
		@rtype: A Boolean object.
		"""
		from operator import ne
		textbuffer = self.__editor.textbuffer
		begin_mark = self.__monitor_list[-1][1][0]
		end_mark = self.__monitor_list[-1][1][1]
		begin = textbuffer.get_iter_at_mark(begin_mark)
		end = textbuffer.get_iter_at_mark(end_mark)
		if ne(len(textbuffer.get_text(begin, end)), 2): return False
		begin.forward_char()
		from gtk.gdk import keyval_to_unicode
		close_keyval = self.__monitor_list[-1][0]
		character = unichr(keyval_to_unicode(close_keyval)).encode("utf-8")
		if ne(begin.get_char(), character): return False
		begin.backward_char()
		textbuffer.begin_user_action()
		textbuffer.delete(begin, end)
		textbuffer.end_user_action()
		from i18n import msg0003
		self.__editor.feedback.update_status_message(msg0003, "succeed")
		return True

	def __has_escape_character(self):
		"""
		Check for escape character before single or double quote character.

		@param self: Reference to the BracketManager instance.
		@type self: A BracketManager object.

		@return: True if there's an escape character before single or double quote character.
		@rtype: A Boolean object.
		"""
		end_iterator = self.__editor.get_cursor_position()
		start_iterator = end_iterator.copy()
		start_iterator.backward_char()
		from operator import eq
		if eq(start_iterator.get_char(), self.__escape_character): return True
		return False

	def __remove_escape_character(self):
		"""
		Remove escape character.

		@param self: Reference to the BracketManager instance.
		@type self: A BracketManager object.
		"""
		end_iterator = self.__editor.get_cursor_position()
		start_iterator = end_iterator.copy()
		start_iterator.backward_char()
		self.__editor.textbuffer.delete(start_iterator, end_iterator)
		return

	def __can_insert_apostrophe(self):
		"""
		Check whether or not a closing apostrophe can be automatically
		inserted into the text editor's buffer.

		Automatic completion will not be performed for apostrophes
		following an alphabet.

		@param self: Reference to the BracketManager instance.
		@type self: A BracketManager object.

		@return: True to insert automatically insert apostrophe.
		@rtype: A Boolean object.
		"""
		from SCRIBES.cursor import get_cursor_iterator
		iterator = get_cursor_iterator(self.__editor.textbuffer)
		from operator import truth
		if truth(iterator.starts_line()): return True
		iterator.backward_char()
		character = iterator.get_char()
		if truth(character.isalpha()): return False
		return True

	def __insert_apostrophe(self):
		"""
		Insert a single apostrophe into the buffer.

		@param self: Reference to the BracketManager instance.
		@type self: A BracketManager object.
		"""
		from gtk import keysyms
		from gtk.gdk import keyval_to_unicode
		utf8_apostrophe_character = unichr(keyval_to_unicode(keysyms.apostrophe)).encode("utf-8")
		self.__editor.textbuffer.insert_at_cursor(utf8_apostrophe_character)
		return

	def __check_mimetype(self):
		"""
		Check the mimetype of the file and modify completion behavior
		for LaTeX and markup source code if possible.

		@param self: Reference to the BracketManager instance.
		@type self: A BracketManager object.
		"""
		from operator import eq, contains, not_
		from gnomevfs import get_mime_type
		from gtk import keysyms
		markup_mimetype = ["text/html", "application/xml", "text/xml", "application/docbook+xml"]
		if not_(self.__editor.uri): return
		try:
			mimetype = get_mime_type(self.__editor.uri)
		except RuntimeError:
			return
		if eq(mimetype, "text/x-tex"):
			self.__open_pair_characters.append(keysyms.dollar)
		elif contains(markup_mimetype, mimetype):
			self.__open_pair_characters.append(keysyms.less)
		return

	def __compile_methods(self):
		"""
		Use psyco, the Python performance optimizing compiler to
		precompile certain methods.

		@param self: Reference to the BracketManager instance.
		@type self: A BracketManager object.
		"""
		try:
			from psyco import bind
			bind(self.__insert_pair_characters)
			bind(self.__insert_closing_pair_character)
			bind(self.__insert_enclosed_selection)
			bind(self.__insert_apostrophe)
			bind(self.__enclose_selection)
			bind(self.__check_mimetype)
			bind(self.__remove_closing_pair_character)
			bind(self.__stop_monitoring)
			bind(self.__move_cursor_out_of_bracket_region)
			bind(self.__can_insert_apostrophe)
			bind(self.__monitor_pair_characters)
		except ImportError:
			pass
		return False

	def __destroy(self):
		"""
		Destroy instance of this class.

		@param self: Reference to the BracketManager instance.
		@type self: A BracketManager object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self.__editor.textview)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__editor)
		self = None
		del self
		return

########################################################################
#
#						Signal and Event Handlers
#
########################################################################

	def __key_press_event_cb(self, textview, event):
		"""
		Handles callback when "key-press-event" signal is emitted.

		This function monitors the editing area for pair character
		insertions.

		@param self: Reference to the BracketManager instance.
		@type self: A BracketManager object.

		@param textview: The text editor's buffer container.
		@type textview: A ScribesTextView object.

		@param event: An event that occurs when keys on the keyboard are pressed.
		@type event: A gtk.Event object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		#from gtk.gdk import keyval_name
		#print keyval_name(event.keyval)
		from operator import truth, eq, contains
		selection = self.__editor.textbuffer.get_selection_bounds()
		if truth(selection) and contains(self.__open_pair_characters_for_enclosement, event.keyval):
			self.__enclose_selection(event.keyval)
			return True
		if truth(self.__monitor_list):
			from gtk import keysyms
			if eq(event.keyval, keysyms.BackSpace):
				result = self.__remove_closing_pair_character()
				return result
			if eq(keysyms.Escape, event.keyval):
				self.__move_cursor_out_of_bracket_region()
				return True
			if eq(self.__monitor_list[-1][0], event.keyval):
				if contains((keysyms.quotedbl, keysyms.apostrophe), event.keyval):
					if truth(self.__has_escape_character()):
						self.__remove_escape_character()
						self.__insert_closing_pair_character(event.keyval)
						return True
				self.__move_cursor_out_of_bracket_region()
				return True
		if contains(self.__open_pair_characters, event.keyval):
			self.__insert_closing_pair_character(event.keyval)
			return True
		return False

	def __cursor_moved_cb(self, editor):
		"""
		Handles callback when the "cursor-moved" signal is emitted.

		@param self: Reference to the BracketManager instance.
		@type self: A BracketManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		from gobject import idle_add
		idle_add(self.__monitor_pair_characters)
		return

	def __monitor_pair_characters(self):
		from operator import not_, truth
		if not_(self.__monitor_list): return False
		textbuffer = self.__editor.textbuffer
		begin_mark = self.__monitor_list[-1][1][0]
		end_mark = self.__monitor_list[-1][1][1]
		begin = textbuffer.get_iter_at_mark(begin_mark)
		end = textbuffer.get_iter_at_mark(end_mark)
		from SCRIBES.cursor import get_cursor_iterator
		cursor_position = get_cursor_iterator(textbuffer)
		if truth(cursor_position.equal(begin)) or truth(cursor_position.equal(end)):
			self.__stop_monitoring()
		elif not_(cursor_position.in_range(begin, end)):
			self.__stop_monitoring()
		return False

	def __loaded_document_cb(self, editor, uri):
		"""
		Handles callback when the "loaded-document" signal is emitted.

		@param self: Reference to the BracketManager instance.
		@type self: A BracketManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__check_mimetype()
		return
