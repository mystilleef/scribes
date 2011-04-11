from SCRIBES.SignalConnectionManager import SignalManager

class Activator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "trigger", self.__activate_cb)
		self.connect(manager, "add", self.__add_cb)
		self.connect(manager, "remove", self.__remove_cb)
		self.connect(manager, "quit", self.__quit_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		# Dictionary Format: {trigger_name: trigger}
		self.__dictionary = {}
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __add(self, trigger):
		self.__dictionary[trigger.name] = trigger
		return False

	def __remove(self, trigger):
		try:
			name = trigger.name
			trigger.destroy()
			del trigger
			del self.__dictionary[name]
		except KeyError:
			# print "Error: Trigger named %s not found" % name
			pass
		finally:
			if not self.__dictionary: self.__manager.emit("triggers-cleared")
		return False

	def __activate(self, name):
		self.__dictionary[name].activate()
		return False

	def __activate_cb(self, editor, name):
		from gobject import idle_add
		idle_add(self.__activate, name)
		return False

	def __add_cb(self, manager, trigger):
		from gobject import idle_add
		idle_add(self.__add, trigger)
		return False

	def __remove_cb(self, manager, trigger):
		from gobject import idle_add
		idle_add(self.__remove, trigger)
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False
