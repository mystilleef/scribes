from SCRIBES.SignalConnectionManager import SignalManager

class Generator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "generate-uris", self.__generate_cb)
		self.connect(manager, "generate-uris-for-treenode", self.__generate_for_treenode_cb)
		self.connect(manager, "finished-enumerating-children", self.__enumerated_children_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__unique_id = ""
		from collections import deque
		self.__process_queue = deque()
		return

	def __generate(self, folder_uri, treeview_reference=None):
		from uuid import uuid1
		unique_id = str(uuid1())
		self.__process_queue.appendleft((unique_id, folder_uri, treeview_reference))
		from gobject import idle_add
		idle_add(self.__manager.emit, "enumerate-children", (folder_uri, unique_id))
		return False

	def __enumerated_children_cb(self, manager, user_data):
		if not self.__process_queue: return False
		unique_id, folder_uri, treeview_reference = self.__process_queue.pop()
		if unique_id != user_data[-1]: return False
		if folder_uri != user_data[1]: return False
		fileinfos, folder_uri, unique_id = user_data
		from gobject import idle_add
		idle_add(self.__manager.emit, "generate-data-for-treeview", (folder_uri, fileinfos, treeview_reference))
		return False

	def __generate_cb(self, manager, folder_uri):
		from gobject import idle_add
		idle_add(self.__generate, folder_uri)
		return False

	def __generate_for_treenode_cb(self, manager, data):
		folder_uri, treeview_reference = data
		from gobject import idle_add
		idle_add(self.__generate, folder_uri, treeview_reference)
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False
