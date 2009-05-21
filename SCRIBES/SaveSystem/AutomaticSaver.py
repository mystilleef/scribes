SAVE_TIMER = 7000

class Saver(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("modified-file", self.__modified_cb)
		self.__sigid3 = editor.connect("close", self.__close_cb)
		self.__sigid4 = manager.connect("reset-modification-flag", self.__modified_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__remove_timer()
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __remove_timer(self):
		try:
			from gobject import source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		return False

	def __process(self):
		self.__remove_timer()
		from gobject import timeout_add
		self.__timer = timeout_add(SAVE_TIMER, self.__save, priority=9999)
		return False

	def __save(self):
		if not self.__editor.uri: return False
		if self.__editor.modified is False: return False
		self.__editor.save_file(self.__editor.uri, self.__editor.encoding)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __close_cb(self, *args):
		self.__remove_timer()
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		return False

	def __modified_cb(self, *args):
		self.__process()
		return False
