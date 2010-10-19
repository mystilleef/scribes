from SCRIBES.SignalConnectionManager import SignalManager

class Manager(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "quit", self.__quit_cb)
		self.connect(manager, "add", self.__add_cb)
		self.connect(manager, "remove", self.__remove_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__triggers = []
		return False

	def __destroy(self):
		self.disconnect()
		self.__triggers = []
		del self
		return False

	def __add(self, trigger):
		self.__triggers.append(trigger)
		return False

	def __remove(self, trigger):
		if trigger in self.__triggers: self.__triggers.remove(trigger)
		return False

	def __update(self, function, trigger):
		function(trigger)
		self.__editor.set_data("triggers", self.__triggers)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __add_cb(self, manager, trigger):
		self.__update(self.__add, trigger)
		return False

	def __remove_cb(self, manager, trigger):
		self.__update(self.__remove, trigger)
		return False
