class Renamer(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("rename", self.__rename_cb)
		self.__sigid3 = manager.connect("encoding", self.__encoding_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__encoding = "utf-8"
		self.__chooser = manager.gui.get_object("FileChooser")
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return False

	def __rename(self):
		self.__editor.response()
		self.__editor.rename_file(self.__chooser.get_uri(), self.__encoding)
		self.__editor.response()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __rename_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__rename)
		return False

	def __encoding_cb(self, manager, encoding):
		self.__encoding = encoding
		return False
