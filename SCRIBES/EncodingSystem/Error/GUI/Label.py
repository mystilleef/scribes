class Label(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("activate", self.__activate_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__label = manager.gui.get_widget("TitleLabel")
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return

	def __set_label(self, uri):
		self.__label.set_label("<b>" + uri + "</b>")
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __activate_cb(self, manager, uri, *args):
		from gobject import idle_add
		idle_add(self.__set_label, uri)
		return False
