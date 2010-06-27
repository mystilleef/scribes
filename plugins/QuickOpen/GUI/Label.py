class Label(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("message", self.__message_cb)
		self.__sigid3 = manager.connect("clear-message", self.__clear_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__label = manager.gui.get_object("FeedbackLabel")
		self.__message = ""
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return False

	def __set(self, message):
		if self.__message == message: return False
		self.__label.set_markup(message)
		self.__label.show()
		self.__message = message
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __message_cb(self, manager, message):
		from gobject import idle_add
		idle_add(self.__set, message)
		return False

	def __clear_cb(self, *args):
		self.__label.hide()
		return False
