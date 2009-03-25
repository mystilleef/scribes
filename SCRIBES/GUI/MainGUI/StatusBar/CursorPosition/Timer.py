class Timer(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("cursor-moved", self.__moved_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self, *args):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __notify(self):
		self.__remove_timers()
		from gobject import timeout_add
		self.__timer1 = timeout_add(500, self.__timeout_notify, priority=9999)
		return False

	def __timeout_notify(self):
		from gobject import idle_add
		self.__timer2 = idle_add(self.__idle_notify, priority=9999)
		return False

	def __idle_notify(self):
		self.__manager.emit("calculate")
		return False

	def __remove_timers(self):
		try:
			from gobject import source_remove
			source_remove(self.__timer1)
			source_remove(self.__timer2)
		except AttributeError:
			pass
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __moved_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__notify, priority=9999)
		return False
