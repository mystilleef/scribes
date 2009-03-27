class Container(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("show", self.__show_cb)
		self.__sigid3 = manager.connect("hide", self.__hide_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		self.__container = editor.gui.get_widget("StatusContainer")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __show(self):
		self.__editor.response()
		self.__container.show()
		self.__editor.response()
		return False

	def __hide(self):
		self.__editor.response()
		self.__container.hide()
		self.__editor.response()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __hide_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__hide, priority=9999)
		return False

	def __show_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__show, priority=9999)
		return False
