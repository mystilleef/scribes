class Setter(object):

	def __init__(self, editor):
		editor.response()
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect_after("checking-file", self.__checking_cb)
		self.__sigid3 = editor.connect("load-error", self.__error_cb)
		self.__sigid4 = editor.connect_after("renamed-file", self.__checking_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__buffer = editor.textbuffer
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return

	def __set(self, language):
		self.__editor.refresh()
		self.__buffer.set_language(language)
		self.__editor.refresh()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __checking_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__set, self.__editor.language_object)
		return False

	def __error_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__set, None)
		return False
