from SCRIBES.SignalConnectionManager import SignalManager

class Activator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "quit", self.__quit_cb)
		self.connect(manager, "add", self.__add_cb)
		self.connect(manager, "remove", self.__remove_cb)
		self.connect(self.__accelgroup, "accel-activate", self.__activate_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		# Dictionary Format: {(keyval, modifier): trigger}
		self.__dictionary = {}
		from gtk import accel_groups_from_object
		self.__accelgroup = accel_groups_from_object(self.__editor.window)[0]
		return False

	def __add(self, trigger):
		if not trigger.accelerator: return False
		from gtk import accelerator_parse, ACCEL_LOCKED
		keyval, modifier = accelerator_parse(trigger.accelerator)
		add = self.__editor.window.add_accelerator
		add("scribes-key-event", self.__accelgroup, keyval, modifier, ACCEL_LOCKED)
		self.__dictionary[(keyval, modifier)] = trigger
		return False

	def __remove(self, trigger):
		if not (trigger in self.__dictionary.values()): return False
		remove = self.__editor.window.remove_accelerator
		keyval, modifier = self.__get_keyval_modifier_from(trigger)
		remove(self.__accelgroup, keyval, modifier)
		del self.__dictionary[(keyval, modifier)]
		if not self.__dictionary: self.__manager.emit("triggers-cleared")
		return False

	def __get_keyval_modifier_from(self, trigger):
		for keyvalmodifier, _trigger in self.__dictionary.iteritems():
			if trigger == _trigger: return keyvalmodifier

	def __activate(self, keyvalmodifier):
		self.__dictionary[keyvalmodifier].activate()
		return False

	def __activate_cb(self, accelgroup, window, keyval, modifier, *args):
		self.__activate((keyval, modifier))
		return False

	def __add_cb(self, manager, trigger):
		self.__add(trigger)
		return False

	def __remove_cb(self, manager, trigger):
		self.__remove(trigger)
		return False

	def __quit_cb(self, *args):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False
