from SCRIBES.SignalConnectionManager import SignalManager

class Enumerator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "enumerate-children", self.__enumerate_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __enumerate(self, user_data):
		folder_uri, unique_id = user_data
		attributes = "standard::*"
		from gio import File
		File(folder_uri).enumerate_children_async(
			attributes,
			self.__enumerate_children_cb,
			user_data=user_data
		)
		return False

	def __enumerate_children_cb(self, gfile, result, user_data):
		enumerator = gfile.enumerate_children_finish(result)
		enumerator.next_files_async(1000, self.__next_files_cb, user_data=user_data)
		return False

	def __next_files_cb(self, enumerator, result, user_data):
		fileinfos = enumerator.next_files_finish(result)
		folder_uri, unique_id = user_data
		from gobject import idle_add 
		idle_add(self.__manager.emit, "finished-enumerating-children", (fileinfos, folder_uri, unique_id))
		return False

	def __enumerate_cb(self, manager, user_data):
		from gobject import idle_add
		idle_add(self.__enumerate, user_data)
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False
