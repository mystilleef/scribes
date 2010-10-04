class Selector(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__select()
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect_after("show-open-dialog-window", self.__show_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__chooser = manager.open_gui.get_object("FileChooser")
		return

	def __select(self):
		self.__editor.response()
		if not (self.__editor.uri): return False
		self.__editor.response()
		self.__chooser.set_uri(self.__editor.uri)
		self.__editor.response()
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __show_cb(self, *args):
		self.__select()
		return False
