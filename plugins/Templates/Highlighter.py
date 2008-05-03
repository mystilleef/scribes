# -*- coding: utf-8 -*-
# Copyright © 2008 Lateef Alabi-Oki
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
This module documents a class that highlights template triggers when
they are found.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

class Highlighter(object):
	"""
	This class creates an object that highlights found template
	triggers.
	"""

	def __init__(self, manager, editor):
		"""
		Initialize object.

		@param self: Reference to the Highlighter instance.
		@type self: A Highlighter object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("trigger-found", self.__trigger_found_cb)
		self.__sigid3 = manager.connect("no-trigger-found", self.__no_trigger_found_cb)
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__precompile_methods, priority=9000)

	def __init_attributes(self, manager, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the Highlighter instance.
		@type self: A Highlighter object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__manager = manager
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__is_highlighted = False
		self.__highlight_tag = self.__create_highlight_tag()
		self.__sigid1 = self.__sigid2 = None
		self.__status_id = None
		return

	def __tag_text(self, position):
		"""
		Tag text at marked position.

		@param self: Reference to the Highlighter instance.
		@type self: A Highlighter object.

		@param position: A list containing marked positions.
		@type position: A List object.
		"""
		start = self.__buffer.get_iter_at_mark(position[0])
		end = self.__buffer.get_iter_at_mark(position[1])
		self.__buffer.apply_tag(self.__highlight_tag, start, end)
		self.__is_highlighted = True
		self.__status_id = self.__editor.feedback.set_modal_message("Template trigger highlighted", "info")
		return False

	def __untag_text(self, position):
		"""
		Untag text at marked position.

		@param self: Reference to the Highlighter instance.
		@type self: A Highlighter object.

		@param position: A list containing marked positions
		@type position: A List object.
		"""
		start = self.__buffer.get_iter_at_mark(position[0])
		end = self.__buffer.get_iter_at_mark(position[1])
		self.__buffer.remove_tag(self.__highlight_tag, start, end)
		self.__is_highlighted = False
		self.__editor.feedback.unset_modal_message(self.__status_id)
		return False

	def __destroy_cb(self, manager):
		"""
		Destroy object.

		@param manager: The template manager.
		@type manager: A Manager object.
		"""
		self.__buffer.get_tag_table().remove(self.__highlight_tag)
		self.__editor.disconnect_signal(self.__sigid1, manager)
		self.__editor.disconnect_signal(self.__sigid2, manager)
		del self
		self = None
		return

	def __trigger_found_cb(self, manager, position):
		"""
		Handles callback when a trigger is found.

		@param self: Reference to the Highlighter instance.
		@type self: A Highlighter object.

		@param manager: Reference to the handle manager.
		@type manager: A Manager object.

		@param position: Position of marks in the buffer.
		@type position: A List object.
		"""
		if self.__is_highlighted: return
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__tag_text_id)
		except AttributeError:
			pass
		self.__tag_text_id = idle_add(self.__tag_text, position)
		return

	def __no_trigger_found_cb(self, manager, position):
		"""
		Handles callback when no trigger is found.

		@param self: Reference to the Highlighter instance.
		@type self: A Highlighter object.

		@param manager: Reference to the template manager.
		@type manager: A Manager object.

		@param position: Position of marks in the buffer.
		@type position: A List object.
		"""
		if self.__is_highlighted is False: return
		try:
			from gobject import idle_add, PRIORITY_LOW, source_remove
			source_remove(self.__untag_text_id)
		except AttributeError:
			pass
		self.__untag_text_id = idle_add(self.__untag_text, position)
		return

	def __precompile_methods(self):
		"""
		Precompile the methods.

		@param self: Reference to the Highlighter instance.
		@type self: A Highlighter object.
		"""
		try:
			from psyco import bind
			bind(self.__trigger_found_cb)
			bind(self.__no_trigger_found_cb)
			bind(self.__tag_text)
			bind(self.__untag_text)
		except ImportError:
			pass
		return False

	def __create_highlight_tag(self):
		"""
		Create the a highlight tag.

		@param self: Reference to the Highlighter instance.
		@type self: A Highlighter object.

		@return: A region highlight tag.
		@rtype: A gtk.TextTag object.
		"""
		from gtk import TextTag
		tag = TextTag("template-trigger")
		self.__editor.textbuffer.get_tag_table().add(tag)
		tag.set_property("background", "black")
		tag.set_property("foreground", "orange")
	#	tag.set_property("background", "gray")
	#	tag.set_property("foreground", "black")
		from pango import WEIGHT_HEAVY
		tag.set_property("weight", WEIGHT_HEAVY)
#		tag.set_property("style", STYLE_ITALIC)
		return tag
