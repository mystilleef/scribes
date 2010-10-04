class Button(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("valid-trigger", self.__valid_cb)
		self.__sigid3 = self.__button.connect("clicked", self.__clicked_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__button = manager.editor_gui.get_widget("SaveButton")
		return  

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__button)
		del self
		self = None
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __valid_cb(self, manager, valid):
		self.__button.set_property("sensitive", valid)
		return False

	def __clicked_cb(self, *args):
		self.__manager.emit("updating-database")
		return False
