class Reconstructor(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("current-path", self.__path_cb)
		self.__sigid3 = manager.connect("selected-paths", self.__selection_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__path = ""
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return False

	def __fullpath(self, _path):
		from os.path import join
		self.__editor.response()
		return join(self.__path, _path)

	def __reconstruct(self, paths):
		uris = [self.__fullpath(_path) for _path in paths]
		self.__manager.emit("uris", uris)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __selection_cb(self, manager, paths):
		from gobject import idle_add
		idle_add(self.__reconstruct, paths)
		return False

	def __path_cb(self, manager, path):
		self.__path = path
		return False
