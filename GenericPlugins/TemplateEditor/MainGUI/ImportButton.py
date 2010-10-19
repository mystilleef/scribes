class Button(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect_after("selected-language-id", self.__language_cb)
		self.__sigid3 = manager.connect("language-treeview-cursor-changed", self.__changed_cb)
		self.__sigid4 = self.__button.connect("clicked", self.__clicked_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__button = manager.gui.get_widget("ImportButton")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__button)
		self.__button.destroy()
		del self
		self = None
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __language_cb(self, *args):
		self.__button.set_property("sensitive", True)
		return False

	def __changed_cb(self, *args):
		self.__button.set_property("sensitive", False)
		return False

	def __clicked_cb(self, *args):
		self.__manager.emit("show-import-window")
		return False
