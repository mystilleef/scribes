from SCRIBES.SignalConnectionManager import SignalManager

class Remover(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "quit", self.__quit_cb)
		self.connect(editor, "remove-trigger", self.__trigger_cb)
		self.connect(editor, "remove-triggers", self.__triggers_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return False

	def __remove(self, trigger):
		self.__manager.emit("remove", trigger)
		return False

	def __remove_triggers(self, triggers):
		from gobject import idle_add
		[idle_add(self.__remove, trigger) for trigger in triggers]
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __trigger_cb(self, editor, trigger):
		from gobject import idle_add
		idle_add(self.__remove_triggers, (trigger,))
		return False

	def __triggers_cb(self, editor, triggers):
		from gobject import idle_add
		idle_add(self.__remove_triggers, triggers)
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False
