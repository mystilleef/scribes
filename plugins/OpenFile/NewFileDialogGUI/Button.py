class Button(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("validation-error", self.__error_cb)
		self.__sigid3 = manager.connect("validation-pass", self.__pass_cb)
		self.__sigid4 = self.__button.connect("clicked", self.__clicked_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__button = manager.new_gui.get_widget("NewButton")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__button)
		del self
		self = None
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __error_cb(self, *args):
		self.__button.props.sensitive = False
		return False

	def __pass_cb(self, *args):
		self.__button.props.sensitive = True
		return False

	def __clicked_cb(self, *args):
		self.__manager.emit("create")
		return False
