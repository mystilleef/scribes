class Manager(object):
	"""
	This class manages and activates triggers. Triggers map keyboard
	shortcuts to actions.
	"""

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.window.connect("key-press-event", self.__key_press_event_cb)
		self.__sigid3 = editor.connect("trigger", self.__trigger_cb)
		self.__sigid4 = editor.connect("add-trigger", self.__add_trigger_cb)
		self.__sigid5 = editor.connect("remove-trigger", self.__remove_trigger_cb)
		self.__sigid6 = editor.connect("add-triggers", self.__add_triggers_cb)
		self.__sigid7 = editor.connect("remove-triggers", self.__remove_triggers_cb)
		editor.register_object(self)
		editor.response()
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=9999)

	def __init_attributes(self, editor):
		self.__editor = editor
		# Precached list of keyboard shortcuts
		self.__shortcuts = set([])
		# A mapping of the format: {trigger_name: (trigger_object, shortcut)}
		self.__trigger_dictionary = {}
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor.window)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.disconnect_signal(self.__sigid5, self.__editor)
		self.__editor.disconnect_signal(self.__sigid6, self.__editor)
		self.__editor.disconnect_signal(self.__sigid7, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return

	def __precompile_methods(self):
		methods = (self.__precompile_methods, self.__process_event,
			self.__is_shortcut, self.__get_modifier, self.__get_shortcut,
			self.__activate)
		self.__editor.optimize(methods)
		return False
########################################################################
#
#							Public API
#
########################################################################

	def __add_trigger(self, trigger):
		try:
			from Exceptions import InvalidTriggerNameError
			from Exceptions import DuplicateTriggerNameError
			from Exceptions import DuplicateTriggerRemovalError
			from Exceptions import DuplicateTriggerAcceleratorError
			shortcut = self.__format_accelerator(trigger.accelerator)
			self.__validate_trigger(trigger, shortcut)
			self.__trigger_dictionary[trigger.name] = trigger, shortcut
			self.__update_shortcuts()
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

	def __remove_trigger(self, trigger):
		try:
			name = trigger.name
			trigger.destroy()
			del trigger
			del self.__trigger_dictionary[name]
			self.__update_shortcuts()
		except KeyError:
			print "Error: Trigger named %s not found" % name
		return

	def __add_triggers(self, triggers):
		return [self.__add_trigger(trigger) for trigger in triggers]

	def __remove_triggers(self, triggers):
		return [self.__remove_trigger(trigger) for trigger in triggers]

	def __trigger(self, trigger_name):
		self.__trigger_dictionary[trigger_name][0].activate()
		return

	def __get_trigger_info(self, trigger):
		return

	def __get_all_trigger_info(self):
		return self.__trigger_dictionary

	def __get_trigger_names(self):
		return self.__trigger_dictionary.keys()

########################################################################

	def __validate_trigger(self, trigger, accelerator):
		from Exceptions import InvalidTriggerNameError
		from Exceptions import DuplicateTriggerNameError
		from Exceptions import DuplicateTriggerRemovalError
		from Exceptions import DuplicateTriggerAcceleratorError
		if not (trigger.name): raise InvalidTriggerNameError
		if trigger.name in self.__trigger_dictionary.keys():
			if trigger.error: raise DuplicateTriggerNameError
			trigger_object, accelerator = self.__trigger_dictionary[trigger.name]
			if not (trigger_object.removable): raise DuplicateTriggerRemovalError
			del self.__trigger_dictionary[trigger_object.name]
			trigger_object.destroy()
			return
		if not (accelerator): return
		for trigger_object, trigger_accelerator in self.__trigger_dictionary.values():
			if (accelerator == trigger_accelerator):
				if trigger.error:
					raise DuplicateTriggerAcceleratorError
				else:
					if not (trigger_object.removable): raise DuplicateTriggerRemovalError
					del self.__trigger_dictionary[trigger_object.name]
					trigger_object.destroy()
				break
		return

	def __format_accelerator(self, accelerator):
		if not accelerator: return None
		accel_list = [accel.strip() for accel in accelerator.split("-")]
		accel = []
		for item in accel_list:
			if item in ("Control", "control", "Ctrl", "ctrl"):
				accel.append("ctrl")
			elif item in ("Alt", "alt"):
				accel.append("alt")
			elif item in ("Shift", "shift"):
				accel.append("shift")
			else:
				accel.append(item)
		# Remove duplicate elements
		accel = list(set(accel))
		accel.sort()
		return tuple(accel)

	def __update_shortcuts(self):
		modifiers = ("ctrl", "shift", "alt")
		accelerators = set([])
		for trigger_object, accelerator in self.__trigger_dictionary.values():
			if not (accelerator): continue
			#accelerator = self.__format_accelerator(accelerator)
			accelerators.add(accelerator)
		self.__shortcuts = accelerators
		return

	def __activate(self, shortcut):
		for trigger, accel in self.__trigger_dictionary.values():
			if accel != shortcut: continue
			trigger.activate()
			break
		return False

########################################################################
#
#						Signal and Event Handlers
#
########################################################################

	def __get_modifier(self, state):
		modifiers = []
		from gtk.gdk import CONTROL_MASK, MOD1_MASK, SHIFT_MASK
		if state & CONTROL_MASK:
			modifiers.append("ctrl")
		if state & SHIFT_MASK:
			modifiers.append("shift")
		if state & MOD1_MASK:
			modifiers.append("alt")
		if modifiers == ["shift"]: return []
		return modifiers

	def __get_shortcut(self, modifiers, keyname):
		# FIXME: Use regular expression here.
		if len(keyname) == 1 and keyname.isalpha(): keyname = keyname.lower()
		shortcut = modifiers + [keyname]
		shortcut.sort()
		return tuple(shortcut)
		
	def __is_shortcut(self, event): 
		modifiers = self.__get_modifier(event.state)
		from gtk.gdk import keyval_name
		keyname = keyval_name(event.keyval)
		keys = ["Escape", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", 
			"F9", "F10", "F11", "F12"]
		if not modifiers and not(keyname in keys): return None
		shortcut = self.__get_shortcut(modifiers, keyname)
		if shortcut in self.__shortcuts: return shortcut
		return None

	def __process_event(self, event): 
		shortcut = self.__is_shortcut(event)
		if shortcut is None: return False
		self.__editor.window.emit_stop_by_name("key-press-event")
		self.__activate(shortcut)
		return True

	def __quit_cb(self, *args):
		self.__destroy()
		return False
		
	def __key_press_event_cb(self, window, event):
		return self.__process_event(event)

	def __add_trigger_cb(self, editor, trigger):
		self.__add_trigger(trigger)
		return False
	
	def __add_triggers_cb(self, editor, triggers):
		self.__add_triggers(triggers)
		return False
	
	def __remove_trigger_cb(self, editor, trigger):
		self.__remove_trigger(trigger)
		return False

	def __remove_triggers_cb(self, editor, triggers):
		self.__remove_triggers(triggers)
		return False

	def __trigger_cb(self, editor, name):
		self.__trigger(name)
		return False
