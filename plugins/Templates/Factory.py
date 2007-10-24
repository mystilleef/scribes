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
This module documents a class that produces objects that process
templates.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class TemplateFactory(object):
	"""
	This class creates an object to that produces objects that process
	templates.
	"""

	def __init__(self, manager, editor):
		"""
		Initialize object.

		@param self: Reference to the TemplateFactory instance.
		@type self: A TemplateFactory object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__init_attributes(manager, editor)
		from gobject import idle_add
		idle_add(self.__precompile_methods)
		self.__signal_id_1 = manager.connect("trigger-activated", self.__trigger_activated_cb)
		self.__signal_id_2 = manager.connect("next-placeholder", self.__next_placeholder_cb)
		self.__signal_id_3 = manager.connect("previous-placeholder", self.__previous_placeholder_cb)
		self.__signal_id_4 = manager.connect("template-destroyed", self.__template_destroyed_cb)
		self.__signal_id_5 = manager.connect("destroy", self.__destroyed_cb)

	def __init_attributes(self, manager, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the TemplateFactory instance.
		@type self: A TemplateFactory object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param editor: Reference to the text editor.
		@type editor: An Editor object.
		"""
		self.__manager = manager
		self.__editor = editor
		self.__templates = []
		self.__signal_id_1 = self.__signal_id_2 = self.__signal_id_3 = None
		self.__signal_id_4 = None
		return

	def __trigger_activated_cb(self, manager, template):
		"""
		Handles callback when the "trigger-activated" signal is emitted.

		@param self: Reference to the TemplateFactory instance.
		@type self: A TemplateFactory object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param template: A template to insert into the buffer.
		@type template: A TemplateManager object.
		"""
		from Processor import TemplateProcessor
		self.__templates.append(TemplateProcessor(manager, self.__editor, template))
		return

	def __previous_placeholder_cb(self, *args):
		"""
		Handles callback when the "previous-placeholder" signal is emitted.

		@param self: Reference to the TemplateFactory instance.
		@type self: A TemplateFactory object.
		"""
		self.__templates[-1].previous()
		return

	def __next_placeholder_cb(self, *args):
		"""
		Handles callback when the "next-placeholder" signal is emitted.

		@param self: Reference to the TemplateFactory instance.
		@type self: A TemplateFactory object.
		"""
		self.__templates[-1].next()
		return

	def __template_destroyed_cb(self, manager, processor):
		"""
		Handles callback when the "template-destroyed" signal is emitted.

		@param self: Reference to the TemplateFactory instance.
		@type self: A TemplateFactory object.

		@param manager: Reference to the TemplateManager instance.
		@type manager: A TemplateManager object.

		@param processor: An object that processes templates.
		@type processor: A TemplateProcessor object.
		"""
		try:
			self.__templates.remove(processor)
		except:
			pass
		return

	def __precompile_methods(self):
		try:
			from pysco import bind
			bind(self.__template_destroyed_cb)
			bind(self.__trigger_activated_cb)
			bind(self.__next_placeholder_cb)
			bind(self.__previous_placeholder_cb)
		except ImportError:
			pass
		return False

	def __destroyed_cb(self, manager):
		"""
		Handles callback when the "destroyed" signal is emitted.

		@param self: Reference to the TemplateFactory instance.
		@type self: A TemplateFactory object.

		@param manager: Reference to the TemplateManager
		@type manager: A TemplateManager object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, manager)
		self.__editor.disconnect_signal(self.__signal_id_2, manager)
		self.__editor.disconnect_signal(self.__signal_id_3, manager)
		self.__editor.disconnect_signal(self.__signal_id_4, manager)
		self.__editor.disconnect_signal(self.__signal_id_5, manager)
		del self
		self = None
		return
