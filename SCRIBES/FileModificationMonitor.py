class Monitor(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		editor.set_data("modified", False)
		self.__sigid1 = editor.connect("modified-file", self.__modified_cb)
		self.__sigid2 = editor.connect("quit", self.__quit_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		del self
		self = None
		return False

	def __modified_cb(self, editor, modified):
		self.__editor.set_data("modified", modified)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False
