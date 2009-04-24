class Monitor(object):

	def __init__(self, editor):
		editor.response()
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("save-file", self.__unmonitor_cb)
		self.__sigid3 = editor.connect("saved-file", self.__monitor_cb)
		self.__sigid4 = editor.connect("save-error", self.__monitor_cb)
		self.__sigid5 = editor.connect("loaded-file", self.__modified_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__monitor = False
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.disconnect_signal(self.__sigid5, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __reload(self):
		if not self.__monitor: return False
		self.__editor.emit("reload-file")
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __unmonitor_cb(self, *args):
		self.__monitor = False
		return False

	def __monitor_cb(self, *args):
		self.__monitor = True
		return False
