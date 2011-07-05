from SCRIBES.SignalConnectionManager import SignalManager

class Navigator(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "go-up", self.__up_cb)
		self.connect(manager, "go-home", self.__home_cb)
		self.connect(manager, "generate-uris", self.__generate_uris_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__folder_uri = ""
		return

	def __go_up(self):
		from gio import File
		gfile = File(self.__folder_uri).get_parent()
		if not gfile: return False
		from gobject import idle_add
		idle_add(self.__manager.emit, "generate-uris", gfile.get_uri())
		return False

	def __go_home(self):
		from gobject import idle_add
		idle_add(self.__manager.emit, "generate-uris", self.__editor.home_folder_uri)
		return False

	def __up_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__go_up)
		return False

	def __home_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__go_home)
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False

	def __generate_uris_cb(self, manager, folder_uri):
		self.__folder_uri = folder_uri
		return False
