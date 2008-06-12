class Button(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = self.__button.connect("clicked", self.__clicked_cb)
		self.__sigid3 = manager.connect("valid-trigger", self.__validate_trigger_cb)
#		self.__sigid4 = manager.connect("dialog-hide-window", self.__hide_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__button = manager.dglade.get_widget("SaveButton")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__button)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
#		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__button.destroy()
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __clicked_cb(self, *args):
		self.__manager.emit("process")
		return False

	def __validate_trigger_cb(self, manager, sensitive):
		self.__button.set_property("sensitive", sensitive)
		return False

	def __hide_cb(self, *args):
		self.__button.set_property("sensitive", False)
		return False
