class Destroyer(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid2 = editor.connect("loaded-file", self.__loaded_file_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__manager.emit("destroy")
		self.__editor.textview.grab_focus()
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		del self
		return False

	def __loaded_file_cb(self, *args):
		self.__destroy()
		return False
