class Label(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("load-error", self.__load_error_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__label = manager.glade.get_widget("TitleLabel")
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		del self
		self = None
		return

	def __set_label(self, uri):
		self.__label.set_label("<b>" + uri + "</b>")
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __load_error_cb(self, editor, uri, *args):
		self.__set_label(uri)
		return False
