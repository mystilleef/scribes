from SCRIBES.SignalConnectionManager import SignalManager

class Dispatcher(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(editor, manager)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "theme-folder-update", self.__dispatch_cb)
		self.__scheme_manager.force_rescan()

	def __init_attributes(self, editor, manager):
		self.__manager = manager
		self.__editor = editor
		self.__scheme_manager = editor.style_scheme_manager
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __dispatch(self):
		self.__scheme_manager.force_rescan()
		get_scheme = self.__scheme_manager.get_scheme
		schemes = [get_scheme(id_) for id_ in self.__scheme_manager.get_scheme_ids()]
		self.__manager.emit("schemes", schemes)
		return False

	def __dispatch_timeout(self):
		from gobject import idle_add
		idle_add(self.__dispatch, priority=99999)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __dispatch_cb(self, *args):
		try:
			from gobject import idle_add, source_remove, timeout_add
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = timeout_add(250, self.__dispatch_timeout, priority=99999)
		return False
