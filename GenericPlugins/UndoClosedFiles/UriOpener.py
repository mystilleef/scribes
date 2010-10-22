from SCRIBES.SignalConnectionManager import SignalManager

class Opener(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "recent-uris", self.__uris_cb)
		self.connect(manager, "open-last-file", self.__open_file_cb)
		self.connect(manager, "open-last-files", self.__open_files_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__uris = []
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __open(self, number):
		count = 0
		uris = []
		for uri in self.__uris:
			if uri in self.__editor.uris: continue
			count += 1
			uris.append(uri)
			if count == number: break
		if not uris: return False
		self.__editor.open_files(uris)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __uris_cb(self, manager, uris):
		self.__uris = uris
		return False

	def __open_file_cb(self, *args):
		self.__open(1)
		return False

	def __open_files_cb(self, *args):
		self.__open(5)
		return False
