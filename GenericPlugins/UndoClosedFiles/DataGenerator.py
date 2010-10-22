from SCRIBES.SignalConnectionManager import SignalManager

class Generator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(editor, manager)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(editor, "recent-infos", self.__info_cb)
		from gobject import idle_add
		idle_add(self.__process)

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		self.__infos = editor.recent_infos
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __get_uri(self, info):
		self.__editor.response()
		return info.get_uri()

	def __process(self):
		from copy import copy
		data = [self.__get_uri(info) for info in copy(self.__infos)]
		self.__manager.emit("recent-uris", data)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __info_cb(self, editor, infos):
		self.__infos = infos
		from gobject import idle_add
		idle_add(self.__process)
		return False
