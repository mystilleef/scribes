#FIXME: Implement keyboard shortcut validation.

class Manager(object):
	"""
	This class manages and activates triggers. Triggers map keyboard
	shortcuts to actions.
	"""

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__init_window_bindings()
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = self.__accelgroup.connect("accel-activate", self.__accel_activate_cb)
		self.__sigid3 = editor.connect("trigger", self.__trigger_cb)
		self.__sigid4 = editor.connect("add-trigger", self.__add_trigger_cb)
		self.__sigid5 = editor.connect("remove-trigger", self.__remove_trigger_cb)
		self.__sigid6 = editor.connect("add-triggers", self.__add_triggers_cb)
		self.__sigid7 = editor.connect("remove-triggers", self.__remove_triggers_cb)
		self.__sigid8 = editor.connect("bar-is-active", self.__active_cb)
		self.__sigid9 = editor.window.connect("scribes-close-window", self.__close_window_cb)
		self.__sigid10 = editor.window.connect("scribes-close-window-nosave", self.__close_window_nosave_cb)
		self.__sigid11 = editor.window.connect("shutdown", self.__shutdown_cb)
		self.__sigid12 = editor.window.connect("fullscreen", self.__fullscreen_cb)
		editor.response()
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=9999)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		# A mapping of the format: {trigger_name: (trigger_object, shortcut)}
		self.__trigger_dictionary = {}
		self.__accel_dictionary = {}
		from gtk import accel_groups_from_object
		self.__accelgroup = accel_groups_from_object(self.__editor.window)[0]
		self.__bar_is_active = False
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__accelgroup)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.disconnect_signal(self.__sigid5, self.__editor)
		self.__editor.disconnect_signal(self.__sigid6, self.__editor)
		self.__editor.disconnect_signal(self.__sigid7, self.__editor)
		self.__editor.disconnect_signal(self.__sigid8, self.__editor)
		self.__editor.disconnect_signal(self.__sigid9, self.__editor.window)
		self.__editor.disconnect_signal(self.__sigid10, self.__editor.window)
		self.__editor.disconnect_signal(self.__sigid11, self.__editor.window)
		self.__editor.disconnect_signal(self.__sigid12, self.__editor.window)
		self.__editor.unregister_object(self)
		del self
		self = None
		return

	def __init_window_bindings(self):
		self.__bind_shortcut("ctrl+w", "scribes-close-window")
		self.__bind_shortcut("ctrl+shift+w", "scribes-close-window-nosave")
		self.__bind_shortcut("ctrl+q", "shutdown")
		self.__bind_shortcut("F11", "fullscreen")
		return False

	def __get_keyval(self, shortcut):
		keyname = shortcut.split("+")[-1]
		from gtk.gdk import keyval_from_name
		return keyval_from_name(keyname)

	def __get_modifier(self, shortcut):
		mask = 0
		modifiers = shortcut.split("+")
		from gtk.gdk import MOD1_MASK, SHIFT_MASK, CONTROL_MASK
		if "ctrl" in (modifiers): mask |= CONTROL_MASK
		if "alt" in (modifiers): mask |= MOD1_MASK
		if "shift" in modifiers: mask |= SHIFT_MASK
		return mask

	def __bind_shortcut(self, shortcut, event_name="scribes-key-event"):
		if not shortcut: return False
		keyval = self.__get_keyval(shortcut)
		modifier = self.__get_modifier(shortcut)
		if (keyval, modifier) in self.__editor.get_shortcuts(): return False
		from gtk import binding_entry_add_signal as bind
		bind(self.__editor.window, keyval, modifier, event_name, str, shortcut)
		self.__editor.add_shortcut((keyval, modifier))
		return False

	def __btest(self, shortcut, trigger):
		if not shortcut: return False
		keyval = self.__get_keyval(shortcut)
		modifier = self.__get_modifier(shortcut)
		add = self.__editor.window.add_accelerator
		from gtk import ACCEL_LOCKED
		add("scribes-key-event", self.__accelgroup, keyval, modifier, ACCEL_LOCKED)
		self.__accel_dictionary[(keyval, modifier)] = trigger
		return False

	def __precompile_methods(self):
		methods = (self.__accel_activate_cb, self.__activate)
		self.__editor.optimize(methods)
		return False

	def __add_trigger(self, trigger):
		try:
			from Exceptions import InvalidTriggerNameError
			from Exceptions import DuplicateTriggerNameError
			from Exceptions import DuplicateTriggerRemovalError
			from Exceptions import DuplicateTriggerAcceleratorError
			shortcut = trigger.accelerator #self.__format_accelerator(trigger.accelerator)
			self.__validate_trigger(trigger, shortcut)
			self.__trigger_dictionary[trigger.name] = trigger, shortcut
			self.__btest(shortcut, trigger)
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
		finally:
			self.__editor.response()
		return

	def __remove_trigger(self, trigger):
		try:
			name = trigger.name
			trigger.destroy()
			del trigger
			del self.__trigger_dictionary[name]
		except KeyError:
			print "Error: Trigger named %s not found" % name
		finally:
			self.__editor.response()
		return

	def __add_triggers(self, triggers):
		return [self.__add_trigger(trigger) for trigger in triggers]

	def __remove_triggers(self, triggers):
		return [self.__remove_trigger(trigger) for trigger in triggers]

	def __trigger(self, trigger_name):
		if self.__bar_is_active: return
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

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __accel_activate_cb(self, accelgroup, window, keyval, mod, *args):
		if self.__bar_is_active: return True
		self.__accel_dictionary[(keyval, mod)].activate()
		return True

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

	def __active_cb(self, editor, active):
		self.__bar_is_active = active
		return False

	def __trigger_cb(self, editor, name):
		self.__trigger(name)
		return False

	def __close_window_cb(self, *args):
		if self.__bar_is_active: return True
		self.__editor.close()
		return False

	def __close_window_nosave_cb(self, *args):
		if self.__bar_is_active: return True
		self.__editor.close(False)
		return False

	def __shutdown_cb(self, *args):
		self.__editor.shutdown()
		return False

	def __fullscreen_cb(self, *args):
		self.__editor.toggle_fullscreen()
		return False
