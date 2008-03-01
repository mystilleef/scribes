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
This module documents a class that monitors the editor's buffer for
template triggers. It emits a signal when template triggers are found or
activated.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class TemplateMonitor(object):
	"""
	This class creates an object that monitors the editor's buffer for
	template triggers. It emits a signal when template triggers are
	found or activated.
	"""

	def __init__(self, manager, editor):
		"""
		Initialize object.

		@param self: Reference to the TemplateMonitor instance.
		@type self: A TemplateMonitor object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(manager, editor)
		self.__signal_id_1 = manager.connect("destroy", self.__destroy_cb)
		self.__signal_id_2 = manager.connect("loaded-general-templates", self.__loaded_general_templates_cb)
		self.__signal_id_3 = manager.connect("loaded-language-templates", self.__loaded_language_templates_cb)
		self.__signal_id_4 = editor.connect("cursor-moved", self.__cursor_moved_cb)
		self.__signal_id_5 = editor.textview.connect("key-press-event", self.__key_press_event_cb)
		self.__signal_id_6 = manager.connect("trigger-activated", self.__trigger_activated_cb)
		self.__signal_id_7 = manager.connect("template-destroyed", self.__template_destroyed_cb)
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__precompile_methods, priority=PRIORITY_LOW)

	def __init_attributes(self, manager, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the TemplateManager instance.
		@type self: A TemplateManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__editor = editor
		self.__manager = manager
		self.__language = None
		self.__language_dictionary = {}
		self.__general_dictionary = {}
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		self.__signal_id_4 = None
		self.__active_templates = 0
		iterator = self.__editor.get_cursor_position()
		self.__bmark = self.__editor.textbuffer.create_mark(None, iterator, True)
		self.__emark = self.__editor.textbuffer.create_mark(None, iterator, True)
		return

	def __precompile_methods(self):
		try:
			from psyco import bind
			bind(self.__key_press_event_cb)
			bind(self.__cursor_moved_cb)
			bind(self.__get_template)
			bind(self.__check_trigger)
		except ImportError:
			pass
		return False

	def __get_template(self, word):
		"""
		Get template associated with word, if possible.

		@param self: Reference to the TemplateMonitor instance.
		@type self: A TemplateMonitor object.

		@param word: A possible template trigger.
		@type word: A String object.
		"""
		general = "General" + word.lstrip("`")
		language = ""
		if self.__language: language = self.__language + word.lstrip("`")
		if language in self.__language_dictionary.keys():
			return self.__language_dictionary[language]
		elif general in self.__general_dictionary.keys():
			return self.__general_dictionary[general]
		return None

	def __check_trigger(self, word):
		"""
		Check if word is a template trigger.

		@param self: Reference to the TemplateMonitor instance.
		@type self: A TemplateMonitor object.

		@param word: A string.
		@type word: A String object.
		"""
		if self.__get_template(word) is None:
			self.__manager.emit("no-trigger-found", (self.__bmark, self.__emark))
			return False
		# Call this to remove previous highlight.
		self.__manager.emit("no-trigger-found", (self.__bmark, self.__emark))
		self.__mark_position(word)
		self.__manager.emit("trigger-found", (self.__bmark, self.__emark))
		return False

	def __remove_trigger(self, word):
		iterator = self.__editor.get_cursor_position()
		from utils import remove_trailing_spaces_on_line
		remove_trailing_spaces_on_line(self.__editor.textview, iterator.get_line())
		iterator = self.__editor.get_cursor_position()
		temp_iter = iterator.copy()
		for character in xrange(len(word)): temp_iter.backward_char()
		self.__editor.textbuffer.delete(iterator, temp_iter)
		return

	def __mark_position(self, word):
		"""
		Mark position of word in the buffer.

		@param self: Reference to the TemplateMonitor instance.
		@type self: A TemplateMonitor object.

		@param word: A string.
		@type word: A String object.
		"""
		iterator = self.__editor.get_cursor_position()
		temporary = iterator.copy()
		self.__editor.textbuffer.move_mark(self.__emark, iterator)
		for character in xrange(len(word)):
			temporary.backward_char()
		self.__editor.textbuffer.move_mark(self.__bmark, temporary)
		return

	def __destroy_cb(self, manager):
		"""
		Destroy instance of this object.

		@param self: Reference to the TemplateMonitor instance.
		@type self: A TemplateMonitor object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.
		"""
		self.__language_dictionary.clear()
		self.__general_dictionary.clear()
		self.__editor.disconnect_signal(self.__signal_id_1, manager)
		self.__editor.disconnect_signal(self.__signal_id_2, manager)
		self.__editor.disconnect_signal(self.__signal_id_3, manager)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_5, self.__editor.textview)
		self.__editor.disconnect_signal(self.__signal_id_6, manager)
		self.__editor.disconnect_signal(self.__signal_id_7, manager)
		self = None
		del self
		return

	def __loaded_general_templates_cb(self, manager, dictionary):
		"""
		Handles callback when the "loaded-general-templates" signal is
		emitted.

		@param self: Reference to the TemplateMonitor instance.
		@type self: A TemplateMonitor object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param dictionary: A dictionary containing general templates.
		@type dictionary: A Dict object.
		"""
		self.__general_dictionary.clear()
		self.__general_dictionary.update(dictionary)
		return

	def __loaded_language_templates_cb(self, manager, dictionary):
		"""
		Handles callback when the "loaded-language-templates" signal is
		emitted.

		@param self: Reference to the TemplateManager instance.
		@type self: A TemplateManager object.

		@param dictionary: A dictionary containing language templates.
		@type dictionary: A Dictionary object.
		"""
		self.__language_dictionary.clear()
		self.__language_dictionary.update(dictionary)
		self.__language = None
		source_lang = self.__editor.language
		if source_lang: self.__language = source_lang.get_id()
		return

	def __cursor_moved_cb(self, *args):
		"""
		Handles callback when the "cursor-moved" signal is emitted.

		@param self: Reference to the TemplateMonitor instance.
		@type self: A TemplateMonitor object.
		"""
		from utils import word_to_cursor
		word = word_to_cursor(self.__editor.textbuffer, self.__editor.get_cursor_position())
		if not (word):
			self.__manager.emit("no-trigger-found", (self.__bmark, self.__emark))
			return False
		from gobject import idle_add, source_remove, timeout_add
		try:
			source_remove(self.__cursor_moved_id)
		except:
			pass
		self.__cursor_moved_id = timeout_add(50, self.__check_trigger, word)
		return False

	def __key_press_event_cb(self, textview, event):
		result = False
		from gtk import keysyms
		if event.keyval == keysyms.Tab:
			try:
				from utils import word_to_cursor
				word = word_to_cursor(self.__editor.textbuffer, self.__editor.get_cursor_position())
				if not (word): raise Exception
				template = self.__get_template(word)
				if template is None: raise Exception
				result = True
				self.__remove_trigger(word)
				self.__manager.emit("trigger-activated", template)
			except:
				if self.__active_templates:
					self.__manager.emit("next-placeholder")
					return True
				return False
		if (event.keyval == keysyms.ISO_Left_Tab):
			if self.__active_templates:
				self.__manager.emit("previous-placeholder")
				return True
		return result

	def __trigger_activated_cb(self, *args):
		self.__active_templates += 1
		return

	def __template_destroyed_cb(self, *args):
		try:
			self.__active_templates -= 1
		except:
			pass
		return
