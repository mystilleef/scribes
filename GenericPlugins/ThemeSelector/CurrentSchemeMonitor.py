class Monitor(object):

	def __init__(self, editor, manager):
		editor.refresh()
		self.__init_attributes(editor, manager)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("populated-model", self.__populated_model_cb)
		editor.refresh()

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		self.__scheme_manager = editor.style_scheme_manager
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return 

	def __send_scheme(self):
		from Metadata import get_value
		scheme = self.__scheme_manager.get_scheme(get_value())
		self.__manager.emit("current-scheme", scheme)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __populated_model_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__send_scheme)
		return False
