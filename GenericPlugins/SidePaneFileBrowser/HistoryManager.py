from SCRIBES.SignalConnectionManager import SignalManager

class Manager(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "go-back", self.__back_cb)
		self.connect(manager, "generate-uris", self.__generate_uris_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		from collections import deque
		self.__history = deque()
		self.__current_folder = ""
		return

	def __pop_from_history(self):
		try:
			folder_uri = self.__history.pop()
		except IndexError:
			folder_uri = ""
		finally:
			from gobject import idle_add
			idle_add(self.__manager.emit, "history-depth", len(self.__history))
		return folder_uri

	def __append_to_history(self, folder_uri):
		if self.__history and (folder_uri == self.__history[-1]): return False
		self.__history.append(folder_uri)
		from gobject import idle_add
		idle_add(self.__manager.emit, "history-depth", len(self.__history))
		return False

	def __go_back(self):
		folder_uri = self.__pop_from_history()
		if not folder_uri: return False
		self.__current_folder = folder_uri
		from gobject import idle_add
		idle_add(self.__manager.emit, "generate-uris", folder_uri)
		return False

	def __update_history(self, folder_uri):
		if self.__current_folder == folder_uri: return False
		if self.__current_folder: self.__append_to_history(self.__current_folder)
		self.__current_folder = folder_uri
		return False

	def __back_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__go_back)
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False

	def __generate_uris_cb(self, manager, folder_uri):
		from gobject import idle_add
		idle_add(self.__update_history, folder_uri)
		return False
