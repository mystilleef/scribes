class Remover(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("remove-trigger", self.__trigger_cb)
		self.__sigid3 = editor.connect("remove-triggers", self.__triggers_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __remove(self, trigger):
		self.__editor.response()
		self.__manager.emit("remove", trigger)
		self.__editor.response()
		return False

	def __remove_triggers(self, triggers):
		[self.__remove(trigger) for trigger in triggers]
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
		self.__destroy()
		return False
