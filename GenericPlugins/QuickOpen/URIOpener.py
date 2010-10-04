class Opener(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("uris", self.__uris_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __open(self, uris):
		self.__editor.open_files(uris)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __uris_cb(self, manager, uris):
		from gobject import idle_add
		idle_add(self.__open, uris)
		return False
