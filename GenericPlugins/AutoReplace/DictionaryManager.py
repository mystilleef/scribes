class Manager(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("database-update", self.__dupdate_cb)
		self.__sigid3 = manager.connect("update-dictionary", self.__dicupdate_cb)
		self.__update()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return False

	def __add(self, key, value):
		from Metadata import set_value, get_value
		dictionary = get_value()
		dictionary[key] = value
		set_value(dictionary)
		return False

	def __remove(self, key):
		from Metadata import set_value, get_value
		dictionary = get_value()
		del dictionary[key]
		set_value(dictionary)
		return False

	def __update(self):
		from Metadata import get_value
		self.__manager.emit("dictionary", get_value())
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __dupdate_cb(self, *args):
		self.__update()
		return False

	def __dicupdate_cb(self, manager, data):
		key, value, add = data
		self.__add(key, value) if add else self.__remove(key)
		return False
