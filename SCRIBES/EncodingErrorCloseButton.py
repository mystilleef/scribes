class Button(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("quit", self.__quit_cb)
		self.__sigid2 = self.__button.connect("clicked", self.__clicked_cb)
		self.__button.set_property("sensitive", True)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__button = manager.glade.get_widget("CloseButton")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__button)
		del self
		self = None
		return

	def __quit_cb(self, *args):
		self.__destroy()
		return

	def __clicked_cb(self, *args):
		self.__manager.emit("hide-window")
		return False
