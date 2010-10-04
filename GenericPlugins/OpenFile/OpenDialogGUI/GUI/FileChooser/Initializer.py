class Initializer(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__chooser = manager.open_gui.get_object("FileChooser")
		return

	def __set_properties(self):
		self.__chooser.set_property("sensitive", True)
		self.__add_filters()
		return False

	def __add_filters(self):
		for filter_ in self.__editor.dialog_filters:
			self.__editor.response()
			self.__chooser.add_filter(filter_)
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		del self
		self = None
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
