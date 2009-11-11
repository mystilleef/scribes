class Saver(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid3 = editor.connect("close", self.__close_cb)
		self.__sigid2 = editor.connect("window-focus-out", self.__out_cb)
		self.__sigid4 = manager.connect("save-failed", self.__failed_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__error = False
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __save(self):
		try:
			if self.__error is False: raise AssertionError
			#if not self.__editor.uri: return False
			if not self.__editor.modified: return False
			self.__editor.save_file(self.__editor.uri, self.__editor.encoding)
		except AssertionError:
			self.__error = False
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __out_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__save, priority=9999)
		return False

	def __close_cb(self, *args):
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		return False
	
	def __failed_cb(self, *args):
		self.__error = True
		return False
