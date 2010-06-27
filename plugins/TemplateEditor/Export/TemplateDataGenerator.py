class Generator(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("selected-templates-dictionary-keys", self.__keys_cb)
		self.__sigid3 = manager.connect("templates-dictionary", self.__dictionary_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__dictionary = {}
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return False

	def __get_data(self, key):
		language, trigger = key.split("|")
		description, template = self.__dictionary[key]
		return language, trigger, description, template

	def __generate(self, keys):
		data = [self.__get_data(key) for key in keys]
		self.__manager.emit("export-template-data", data)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __keys_cb(self, manager, keys):
		self.__generate(keys)
		return False

	def __dictionary_cb(self, manager, dictionary):
		self.__dictionary = dictionary
		return False
