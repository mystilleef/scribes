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
This module documents a class that manages and activate triggers.
Triggers are operations mapped to keyboard shortcuts, widgets or
strings.

@author: Lateef Alabi-Oki
@organization: The Scribes Project
@copyright: Copyright © 2007 Lateef Alabi-Oki
@license: GNU GPLv2 or Later
@contact: mystilleef@gmail.com
"""

class TriggerManager(object):
	"""
	This class manages and activates triggers. Triggers are operations
	mapped to accelerators, widgets or strings.
	"""

	def __init__(self, editor):
		"""
		Initialize object.

		@param self: Reference to the TriggerManager instance.
		@type self: A TriggerManager object.

		@param window: A window to bind to.
		@type window: A gtk.Window object.
		"""
		self.__init_attributes(editor)
		from gobject import idle_add
		idle_add(self.__precompile_methods)
		self.__signal_id_1 = self.__window.connect("key-press-event", self.__key_press_event_cb)
		self.__signal_id_2 = self.__editor.connect("show-bar", self.__show_bar_cb)
		self.__signal_id_3 = self.__editor.connect("hide-bar", self.__hide_bar_cb)
		self.__signal_id_4 = self.__editor.connect("close-document", self.__close_document_cb)
		self.__signal_id_5 = self.__editor.connect("close-document-no-save", self.__close_document_no_save_cb)
		self.__editor.emit("initialized-trigger-manager")

	def __init_attributes(self, editor):
		"""
		Initialize data attributes.

		@param self: Reference to the TriggerManager instance.
		@type self: A TriggerManager object.

		@param window: A window to bind to.
		@type window: A gtk.Window object.
		"""
		self.__window = editor.window
		self.__editor = editor
		# Precached list of accelerator keys
		self.__accelerator_keyname_list = set([])
		self.__bar_is_visible = False
		# Precached list of accelerator modifiers and keys
		self.__accelerators = set([])
		# A mapping of the format: {trigger_name: (trigger_object, accelerator)}
		self.__trigger_dictionary = {}
		self.__signal_id_1 = self.__signal_id_2 = None
		self.__signal_id_3 = self.__signal_id_4 = None
		self.__signal_id_5 = None
		self.__registration_id = editor.register_object()
		return

########################################################################
#
#							Public API
#
########################################################################

	def add_trigger(self, trigger):
		"""
		Add a new trigger object to the manager.

		@param self: Reference to the TriggerManager instance.
		@type self: A TriggerManager object.

		@param trigger: A trigger.
		@type trigger: A Trigger object.
		"""
		try:
			self.__editor.response()
			from Exceptions import InvalidTriggerNameError
			from Exceptions import DuplicateTriggerNameError
			from Exceptions import DuplicateTriggerRemovalError
			from Exceptions import DuplicateTriggerAcceleratorError
			accelerator = self.__format_accelerator(trigger.accelerator)
			self.__validate_trigger(trigger, accelerator)
			self.__trigger_dictionary[trigger.name] = trigger, accelerator
			self.__update_accelerator_info()
			self.__editor.response()
		except InvalidTriggerNameError:
			print "Error: %s is not a valid trigger name." % trigger.name
		except DuplicateTriggerNameError:
			print "Error: Another trigger named %s exists." % trigger.name
			print self.get_trigger_info(trigger.name)
		except DuplicateTriggerAcceleratorError:
			print "Error: Another trigger uses this accelerator %s." % trigger.accelerator
		except DuplicateTriggerRemovalError:
			print "Error: Duplicate trigger could not be forcefully removed"
			print "Error: %s will not be loaded" % trigger.name
		return

	def remove_trigger(self, trigger):
		"""
		Remove a new trigger object to the manager.

		@param self: Reference to the TriggerManager instance.
		@type self: A TriggerManager object.

		@param trigger: A trigger.
		@type trigger: A Trigger object.
		"""
		try:
			self.__editor.response()
			name = trigger.name
			trigger.destroy()
			del trigger
			del self.__trigger_dictionary[name]
			self.__update_accelerator_info()
			from operator import not_
			if self.__trigger_dictionary: return
			if self.__is_quiting: self.__destroy()
			self.__editor.response()
		except KeyError:
			print "Error: Trigger named %s not found" % name
		return

	def add_triggers(self, triggers):
		"""
		Add a list of triggers to the manager.

		@param self: Reference to the TriggerManager instance.
		@type self: A TriggerManager object.

		@param trigger: A list of triggers.
		@type trigger: A List object.
		"""
		map(self.add_trigger, triggers)
		return

	def remove_triggers(self, triggers):
		"""
		Remove a list of triggers to the manager.

		@param self: Reference to the TriggerManager instance.
		@type self: A TriggerManager object.

		@param trigger: A list of triggers.
		@type trigger: A List object.
		"""
		map(self.remove_trigger, triggers)
		return

	def trigger(self, trigger_name):
		self.__trigger_dictionary[trigger_name][0].activate()
		return

	def get_trigger_info(self, trigger):
		return

	def get_all_trigger_info(self):
		return

	def get_trigger_names(self):
		return self.__trigger_dictionary.keys()

########################################################################

	def __validate_trigger(self, trigger, accelerator):
		"""
		Check if trigger can be added to manager.

		@param self: Reference to the TriggerManager instance.
		@type self: A TriggerManager object.

		@param trigger: A trigger.
		@type trigger: A Trigger object.

		@param accelerator: Internal representation of an accelerator associated with a trigger.
		@type accelerator: A Tuple object.
		"""
		from Exceptions import InvalidTriggerNameError
		from Exceptions import DuplicateTriggerNameError
		from Exceptions import DuplicateTriggerRemovalError
		from Exceptions import DuplicateTriggerAcceleratorError
		from operator import not_, contains, eq
		if not_(trigger.name): raise InvalidTriggerNameError
		if contains(self.__trigger_dictionary.keys(), trigger.name):
			if trigger.error: raise DuplicateTriggerNameError
			trigger_object, accelerator = self.__trigger_dictionary[trigger.name]
			if not_(trigger_object.removable): raise DuplicateTriggerRemovalError
			del self.__trigger_dictionary[trigger_object.name]
			trigger_object.destroy()
			return
		if not_(accelerator): return
		for trigger_object, trigger_accelerator in self.__trigger_dictionary.values():
			if eq(accelerator, trigger_accelerator):
				if trigger.error:
					raise DuplicateTriggerAcceleratorError
				else:
					if not_(trigger_object.removable): raise DuplicateTriggerRemovalError
					del self.__trigger_dictionary[trigger_object.name]
					trigger_object.destroy()
				break
		return

	def __format_accelerator(self, accelerator):
		"""
		Format accelerator for easy parsing and internal use.

		Accelerator Format Examples:

			(ctrl - alt -s)
			(s)
			(alt - a)

		@param self: Reference to the TriggerManager.
		@type self: A TriggerManager object.

		@param accelerator: A keyboard shortcut associated with a trigger.
		@type accelerator: A String object.
		"""
		from operator import not_
		if not_(accelerator): return None
		accel_list = [accel.strip() for accel in accelerator.split("-")]
		accel = []
		for item in accel_list:
			if item in("Control", "control", "Ctrl", "ctrl"):
				accel.append("ctrl")
			elif item in ("Alt", "alt"):
				accel.append("alt")
			elif item in ("Shift", "shift"):
				accel.append("shift")
			else:
				accel.append(item)
		# Remove duplicate elements
		accel = set(accel)
		accel = list(accel)
		accel.sort()
		return tuple(accel)

	def __update_accelerator_info(self):
		"""
		Populate the accelerator keyname list.

		The list is used to determine if a key pressed has a trigger
		or accelerator associated with it.

		@param self: Reference to the TriggerManager instance.
		@type self: A TriggerManager object.
		"""
		modifiers = ("ctrl", "shift", "alt")
		keyname = set([])
		accelerators = set([])
		from operator import contains, not_
		for trigger_object, accelerator in self.__trigger_dictionary.values():
			if not_(accelerator): continue
			for item in accelerator:
				if contains(modifiers, item): continue
				keyname.add(item)
			accelerators.add(accelerator)
		self.__accelerator_keyname_list = keyname
		self.__accelerators = accelerators
		return

	def __activate_accelerator(self, accelerator):
		"""
		Activate trigger associated with an accelerator.

		@param self: Reference to the TriggerManager instance.
		@type self: A TriggerManager object.

		@param accelerator: An accelerator associated with a trigger.
		@type accelerator: A List object.
		"""
		accelerator.sort()
		accelerator = tuple(accelerator)
		from operator import contains, not_, eq
		if not_(contains(self.__accelerators, accelerator)): return False
		for trigger, accel in self.__trigger_dictionary.values():
			if eq(accel, accelerator):
				trigger.activate()
				break
		return True

	def __precompile_methods(self):
		"""
		Use psyco to precompile some methods.

		@param self: Reference to the TriggerManager instance.
		@type self: A TriggerManager object.
		"""
		try:
			from psyco import bind
			bind(self.__activate_accelerator)
			bind(self.__key_press_event_cb)
			bind(self.__update_accelerator_info)
			bind(self.__format_accelerator)
		except ImportError:
			pass
		return False

	def __destroy(self):
		"""
		Destroy this object.

		@param self: Reference to the TriggerManager instance.
		@type self: A TriggerManager object.
		"""
		self.__accelerator_keyname_list.clear()
		self.__trigger_dictionary.clear()
		self.__accelerators.clear()
		self.__editor.disconnect_signal(self.__signal_id_1, self.__editor.window)
		self.__editor.disconnect_signal(self.__signal_id_2, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_3, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_4, self.__editor)
		self.__editor.disconnect_signal(self.__signal_id_5, self.__editor)
		self.__editor.unregister_object(self.__registration_id)
		del self
		self = None
		return

########################################################################
#
#						Signal and Event Handlers
#
########################################################################

	def __key_press_event_cb(self, window, event):
		"""
		Handles callback when the "key-press-event" signal is emitted.

		@param self: Reference to the TriggerManager instance.
		@type self: A TriggerManager object.

		@param window: A window.
		@type window: A gtk.Window object.

		@param event: An event that occurs within window.
		@type event: A gtk.Event object.

		@return: True to handle the event.
		@rtype: A Boolean object.
		"""
		if self.__bar_is_visible: return False
		from gtk.gdk import CONTROL_MASK, MOD1_MASK, SHIFT_MASK, keyval_name
		from operator import contains, not_
		keyname = keyval_name(event.keyval)
		if not_(contains(self.__accelerator_keyname_list, keyname)): return False
		special_keys = ("Delete", "Insert", "Home", "End", "PageUp",
						"PageDown", "Right", "Left", "Up", "Down", "F1",
						"F12", "F10", "Return")
		# Control and Shift key are pressed.
		if event.state & CONTROL_MASK and event.state & SHIFT_MASK:
			if contains(special_keys, keyname):
				accelerator = ["ctrl", "shift"] + [keyname]
			else:
				accelerator = ["ctrl"] + [keyname]
			return self.__activate_accelerator(accelerator)

		# Alt and Shift key are pressed.
		if event.state & SHIFT_MASK and event.state & MOD1_MASK:
			if contains(special_keys, keyname):
				accelerator = ["alt", "shift"] + [keyname]
			else:
				accelerator = ["alt"] + [keyname]
			return self.__activate_accelerator(accelerator)

		# Control and Alt key are pressed.
		if event.state & CONTROL_MASK and event.state & MOD1_MASK:
			accelerator = ["alt", "ctrl"] + [keyname]
			return self.__activate_accelerator(accelerator)
		# Control key are pressed.
		if event.state & CONTROL_MASK:
			accelerator = ["ctrl"] + [keyname]
			return self.__activate_accelerator(accelerator)

		# Alt key is pressed.
		if event.state & MOD1_MASK:
			accelerator = ["alt"] + [keyname]
			return self.__activate_accelerator(accelerator)
		# No modifiers.
		return self.__activate_accelerator([keyname])

	def __close_document_cb(self, *args):
		"""
		Handles callback when the "close-document" signal is emitted.

		@param self: Reference to the TriggerManager instance.
		@type self: A TriggerManager object.
		"""
		self.__is_quiting = True
		return

	def __close_document_no_save_cb(self, *args):
		"""
		Handles callback when the "close-document-no-save" signal is
		emitted.

		@param self: Reference to the TriggerManager instance.
		@type self: A TriggerManager object.
		"""
		self.__is_quiting = True
		self.__destroy()
		return

	def __show_bar_cb(self, *args):
		self.__bar_is_visible = True
		return

	def __hide_bar_cb(self, *args):
		self.__bar_is_visible = False
		return
