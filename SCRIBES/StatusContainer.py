class Container(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__container.show()
		editor.response()
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__container = editor.gui.get_widget("StatusContainer")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return

	def __quit_cb(self, *args):
		self.__destroy()
		return False
