class Manager(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("toggle-fullscreen", self.__toggle_cb)
		self.__sigid3 = editor.connect("fullscreen", self.__fullscreen_cb)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__enabled = False
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __toggle(self):
		enable = False if self.__enabled else True
		self.__editor.emit("fullscreen", enable)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __toggle_cb(self, *args):
		self.__toggle()
		return False

	def __fullscreen_cb(self, editor, enable):
		self.__enabled = enable
		return False
