from SCRIBES.SignalConnectionManager import SignalManager

class Manager(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(editor, "save-file", self.__save_cb)
		self.connect(editor, "rename-file", self.__rename_cb, True)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		return

	def __process(self, uri, encoding):
		try:
			from gobject import idle_add, PRIORITY_LOW
			data = uri, encoding
			if self.__editor.readonly: raise AssertionError
			if self.__editor.generate_filename: raise ValueError
			idle_add(self.__manager.emit, "new-save-job", data)
		except AssertionError:
			idle_add(self.__manager.emit, "readonly-error")
		except ValueError:
			idle_add(self.__manager.emit, "generate-name", data, priority=PRIORITY_LOW)
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __save_cb(self, editor, uri, encoding):
		from gobject import idle_add
		idle_add(self.__process, uri, encoding)
		return False

	def __rename_cb(self, editor, uri, encoding):
		from gobject import idle_add
		idle_add(self.__editor.save_file, uri, encoding)
		return False
