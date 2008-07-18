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
This module documents a class that creates an object that colors template
triggers.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2008 Lateef Alabi-Oki
@license: GNU GPLv3 or Later
@contact: mystilleef@gmail.com
"""

class Colorer(object):
	"""
	This class creates an object that colors template triggers.
	"""

	def __init__(self, editor, manager):
		"""
		Initialize object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param manager: The template manager.
		@type manager: A Manager object.
		"""
		self.__init_attributes(editor, manager)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("trigger-found", self.__trigger_found_cb)
		self.__sigid3 = manager.connect("no-trigger-found", self.__no_trigger_found_cb)
#		from gobject import idle_add, PRIORITY_LOW
#		idle_add(self.__precompile_methods, priority=9000)

	def __init_attributes(self, editor, manager):
		"""
		Initialize attributes.

		@param self: Reference to the Colorer instance.
		@type self: A Colorer object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.

		@param manager: The template manager
		@type manager: A Manager object.
		"""
		self.__manager = manager
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__is_highlighted = False
		self.__highlight_tag = self.__create_highlight_tag()
		self.__sigid1 = self.__sigid2 = None
		self.__status_id = None
		self.__lmark = self.__editor.create_left_mark()
		self.__rmark = self.__editor.create_right_mark()
		return

	def __destroy(self):
		"""
		Destroy colorer.

		@param self: Reference to the Colorer instance.
		@type self: A Colorer object.
		"""
		self.__editor.delete_mark(self.__lmark)
		self.__editor.delete_mark(self.__rmark)
		self.__buffer.get_tag_table().remove(self.__highlight_tag)
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return

	def __precompile_methods(self):
		"""
		Precompile methods.

		@param self: Reference to the Colorer instance.
		@type self: A Colorer object.
		"""
		methods = [self.__trigger_found_cb, self.__no_trigger_found_cb,
				self.__color_trigger, self.__uncolor_trigger, self.__process,
				self.__get_trigger_position, self.__mark_trigger_position,
		]
		self.__editor.optimize(methods)
		return False

	def __create_highlight_tag(self):
		"""
		Create trigger highlight tag.

		@param self: Reference to the Colorer instance.
		@type self: A Colorer object.

		@return: A color tag
		@rtype: A gtk.TextTag object.
		"""
		from gtk import TextTag
		tag = TextTag("template-trigger")
		self.__editor.textbuffer.get_tag_table().add(tag)
		tag.set_property("background", "black")
		tag.set_property("foreground", "orange")
		from pango import WEIGHT_HEAVY
		tag.set_property("weight", WEIGHT_HEAVY)
		return tag

################################################################################
#
#						Processing Methods
#
################################################################################

	def __process(self, trigger):
		"""
		Color trigger in editing area.

		@param self: Reference to the Colorer instance.
		@type self: A Colorer object.

		@param trigger: A template trigger.
		@type trigger: A String object.
		"""
		position = self.__get_trigger_position(len(trigger))
		self.__color_trigger(position)
		self.__mark_trigger_position(position)
		return False

	def __get_trigger_position(self, trigger_length):
		"""
		Get position of trigger in editing area.

		@param self: Reference to the Colorer instance.
		@type self: A Colorer object.

		@param trigger_length: Length of trigger
		@type trigger_length: An Integer object.

		@return: Return position of trigger in editing area.
		@rtype: A Tuple object.
		"""
		cursor = self.__editor.cursor
		begin = cursor.copy()
		for count in xrange(trigger_length): begin.backward_char()
		return begin, cursor

	def __mark_trigger_position(self, position):
		"""
		Mark trigger position in buffer.

		@param self: Reference to the Colorer instance.
		@type self: A Colorer object.

		@param position: Position of trigger in buffer.
		@type position: A Tuple object.
		"""
		self.__buffer.move_mark(self.__lmark, position[0])
		self.__buffer.move_mark(self.__rmark, position[1])
		return

	def __color_trigger(self, position):
		"""
		Color trigger in editing area (buffer)

		@param self: Reference to the Colorer instance.
		@type self: A Colorer object.

		@param position: Position of trigger in editing area.
		@type position: A Tuple object.
		"""
		self.__uncolor_trigger()
		self.__buffer.apply_tag(self.__highlight_tag, position[0], position[1])
		self.__is_highlighted = True
		self.__status_id = self.__editor.feedback.set_modal_message("Template trigger highlighted", "info")
		return False

	def __uncolor_trigger(self):
		"""
		Remove trigger color from editing area.

		@param self: Reference to the Colorer instance.
		@type self: A Colorer object.
		"""
		start = self.__buffer.get_iter_at_mark(self.__lmark)
		end = self.__buffer.get_iter_at_mark(self.__rmark)
		self.__buffer.remove_tag(self.__highlight_tag, start, end)
		self.__is_highlighted = False
		self.__editor.feedback.unset_modal_message(self.__status_id)
		return False

################################################################################
#
# 						Event and Signal Callbacks
#
################################################################################

	def __destroy_cb(self, *args):
		"""
		Handles callback when the destroy signal is emitted.

		@param self: Reference to the Colorer instance.
		@type self: A Colorer object.
		"""
		self.__destroy()
		return

	def __trigger_found_cb(self, manager, trigger):
		"""
		Handles callback when a template trigger is found.

		@param self: Reference to the Colorer instance.
		@type self: A Colorer object.

		@param manager: Template system manager.
		@type manager: A Manager object.

		@param trigger: A template trigger
		@type trigger: A String object.
		"""
#		if self.__is_highlighted: return
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__tid)
		except AttributeError:
			pass
		self.__tid = idle_add(self.__process, trigger, priority=9999)
		return

	def __no_trigger_found_cb(self, *args):
		"""
		Handles callback when the no trigger is found.

		@param self: Reference to the Colorer instance.
		@type self: A Colorer object.
		"""
		if self.__is_highlighted is False: return
		try:
			from gobject import idle_add, PRIORITY_LOW, source_remove
			source_remove(self.__textid)
		except AttributeError:
			pass
		self.__textid = idle_add(self.__uncolor_trigger)
		return
