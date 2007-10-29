# -*- coding: utf-8 -*-
# Copyright © 2006 Lateef Alabi-Oki
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
abbreviations for automatic replacement.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2006 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_PYOBJECT

class AutoReplaceMonitor(GObject):
	"""
	This class creates an object that monitors string in the buffer for
	automatic replacement. When a string eligible for replacement is
	found, an signal is emitted.
	"""

	__gsignals__ = {
		"abbreviation-found": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_PYOBJECT,)),
	}

	def __init__(self, manager, editor):
		"""
		Initialize the monitor object.

		@param self: Reference to the AutoReplaceMonitor instance.
		@type self: An AutoReplaceMonitor object.

		@param manager: Reference to the AutoReplaceManager.
		@type manager: An AutoReplaceManager object.
		"""
		GObject.__init__(self)
		self.__init_attributes(manager, editor)
		self.__signal_id_1 = self.__manager.connect("abbreviations-updated", self.__manager_abbreviations_updated_cb)
		self.__signal_id_2 = self.__manager.connect("destroy", self.__monitor_destroy_cb)
		self.__signal_id_3 = self.__editor.textview.connect("key-press-event", self.__monitor_key_press_event_cb)
		if self.__can_monitor is False:
			self.__editor.textview.handle_block(self.__signal_id_3)

	def __init_attributes(self, manager, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the AutoReplaceMonitor instance.
		@type self: An AutoReplaceMonitor object.

		@param manager: Reference to the AutoReplaceManager
		@type manager: An AutoReplaceManager object.
		"""
		# Reference to the AutoReplaceManager.
		self.__manager = manager
		# Reference to the editor.
		self.__editor = editor
		# A list of strings (abbreviations) to monitor.
		self.__abbreviation_list = []
		# Identifier for the "abbreviations-updated" signal.
		self.__signal_id_1 = None
		# Identifier for the "destroy" signal.
		self.__signal_id_2 = None
		# Identifier for the "key-press-event" signal.
		self.__signal_id_3 = None
		self.__can_monitor = True
		return

########################################################################
#
#					Event and Signal Handlers
#
########################################################################

	def __manager_abbreviations_updated_cb(self, manager, abbreviation_dictionary):
		"""
		Handles callback when the "abbreviations-updated" signal is
		emitted.

		@param self: Reference to the AutoReplaceMonitor instance.
		@type self: An AutoReplaceMonitor object.

		@param manager: Reference to the AutoReplaceManager.
		@type manager: An AutoReplaceManager object.

		@param abbreviation_dictionary: A dictionary of abbreviations.
		@type abbreviation_dictionary: A Dictionary object.
		"""
		self.__abbreviation_list = abbreviation_dictionary.keys()
		return

	def __monitor_destroy_cb(self, manager):
		"""
		Handles callback when the "destroy" signal is emitted.

		@param self: Reference to the AutoReplaceManager instance.
		@type self: An AutoReplaceManager object.

		@param manager: Reference to the AutoReplaceManager.
		@type manager: An AutoReplaceManager object.
		"""
		self.__editor.disconnect_signal(self.__signal_id_1, self.__manager)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__manager)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__editor.textview)
		del self
		self = None
		return

	def __monitor_key_press_event_cb(self, textview, event):
		"""
		Handles callback when the "key-press-event" signal is emitted.

		@param self: Reference to the AutoReplaceMonitor instance.
		@type self: An AutoReplaceMonitor object.

		@param textview: Reference to the editor's textview.
		@type textview: A ScribesTextView object.

		@return: True to propagate signals to parent widgets.
		@type: A Boolean Object.
		"""
		from gtk import keysyms
		if event.keyval in [keysyms.Return, keysyms.space]:
			if self.__found_abreviation(event.keyval): return True
		return False

	def __found_abreviation(self, keyval):
		"""
		Emit a signal if an abbreviation is found.

		@param self: Reference to the AutoReplaceMonitor instance.
		@type self: An AutoReplaceMonitor object.

		@param keyval: A value representing either Enter or Space character.
		@type keyval: An Integer object.

		@return: True if an abbreviation is found.
		@rtype: A Boolean object.
		"""
		word = self.__editor.word_to_cursor()
		if word is None: return False
		if word in self.__abbreviation_list:
			from gtk import keysyms
			if keyval == keysyms.space:
				self.emit("abbreviation-found", word + " ")
			else:
				self.emit("abbreviation-found", word + "\n")
			return True
		return False
