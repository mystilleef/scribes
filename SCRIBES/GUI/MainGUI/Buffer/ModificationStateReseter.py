class Reseter(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("checking-file", self.__reset_cb)
		self.__sigid3 = editor.connect("loaded-file", self.__reset_cb)
		self.__sigid4 = editor.connect("load-error", self.__reset_cb)
		self.__sigid5 = editor.connect("saved-file", self.__reset_cb)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__buffer = editor.textbuffer
		return

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

	def __reset(self):
		if self.__buffer.get_modified(): self.__buffer.set_modified(False)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __reset_cb(self, *args):
		self.__reset()
		return False
