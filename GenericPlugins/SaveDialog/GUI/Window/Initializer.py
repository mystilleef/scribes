class Initializer(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = self.__manager.connect("destroy", self.__destroy_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__window = manager.gui.get_object("Window")
		return

	def __set_properties(self):
		self.__window.set_property("sensitive", True)
		self.__window.set_transient_for(self.__editor.window)
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
