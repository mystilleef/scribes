class Activator(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("quit", self.__quit_cb)
		self.__sigid2 = self.__accelgroup.connect("accel-activate", self.__activate_cb)
		self.__sigid3 = manager.connect("add", self.__add_cb)
		self.__sigid4 = manager.connect("remove", self.__remove_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		# Dictionary Format: {(keyval, modifier): trigger}
		self.__dictionary = {}
		from gtk import accel_groups_from_object
		self.__accelgroup = accel_groups_from_object(self.__editor.window)[0]
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__accelgroup)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
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

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __activate_cb(self, accelgroup, window, keyval, modifier, *args):
		from gobject import idle_add
		idle_add(self.__activate, (keyval, modifier))
		return False

	def __add_cb(self, manager, trigger):
		from gobject import idle_add
		idle_add(self.__add, trigger)
		return False

	def __remove_cb(self, manager, trigger):
		from gobject import idle_add
		idle_add(self.__remove, trigger)
		return False
