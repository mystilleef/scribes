from SCRIBES.SignalConnectionManager import SignalManager

class Generator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(editor, manager)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "schemes", self.__schemes_cb)

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __process(self, schemes):
		can_remove = lambda scheme: scheme.get_filename().startswith(self.__editor.home_folder)
		get_description = lambda scheme: (scheme.get_name() + " - " + scheme.get_description())
		format = lambda scheme: (get_description(scheme), scheme, can_remove(scheme))
		data = (format(scheme) for scheme in schemes)
		self.__manager.emit("model-data", data)
		return False

	def __process_timeout(self, schemes):
		from gobject import idle_add
		idle_add(self.__process, schemes)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __schemes_cb(self, manager, schemes):
		try:
			from gobject import timeout_add, source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = timeout_add(250, self.__process_timeout, schemes)
		return False
