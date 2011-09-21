from SCRIBES.SignalConnectionManager import SignalManager

class Monitor(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "saving-in-progress", self.__saving_cb, True)
		self.connect(manager, "finished-save-job", self.__job_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__is_saving = False
		self.__job = []
		return False

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		print "Destroying save job monitor instance"
		del self
		return False

	def __saving_cb(self, manager, is_saving):
		if is_saving: return False
		signal_name = "save-succeeded" if len(self.__job) == 3 else "save-failed"
		from gobject import idle_add
		idle_add(self.__manager.emit, signal_name, self.__job)
		return False

	def __job_cb(self, manager, job):
		self.__job = job
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False
