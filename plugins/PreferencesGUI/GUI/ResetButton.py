class Button(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("sensitive", self.__sensitive_cb)
		self.__sigid3 = self.__button.connect("clicked", self.__clicked_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__button = manager.gui.get_object("ResetButton")
		return

	def __destroy(self):
		signals_data = (
			(self.__sigid1, self.__manager),
			(self.__sigid2, self.__manager),
			(self.__sigid3, self.__button),
		)
		self.__editor.disconnect_signals(signals_data)
		del self
		self = None
		return False

	def __sensitive_cb(self, manager, sensitive):
		self.__button.set_property("sensitive", sensitive)
		return False

	def __clicked_cb(self, *args):
		self.__manager.emit("reset")
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
