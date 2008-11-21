class Button(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = self.__manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = self.__button.connect("clicked", self.__clicked_cb)
		self.__sigid3 = self.__manager.connect("add-button-sensitivity", self.__sensitive_cb)
		self.__button.set_property("sensitive", True)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__button = manager.gui.get_widget("AddButton")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__button)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__button.destroy()
		del self
		self = None
		return False

	def __destroy_cb(self, manager):
		self.__destroy()
		return

	def __clicked_cb(self, *args):
		self.__manager.emit("add-row")
		return False

	def __sensitive_cb(self, manager, sensitive):
		self.__button.set_property("sensitive", sensitive)
		return False
