class Grabber(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = self.__window.connect_after("focus-in-event", self.__in_cb)
		self.__sigid3 = self.__window.connect("focus-out-event", self.__out_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__window = editor.window
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__window)
		self.__editor.disconnect_signal(self.__sigid3, self.__window)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __in_cb(self, *args):
		self.__window.grab_add()
		return False

	def __out_cb(self, *args):
		self.__window.grab_remove()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False
