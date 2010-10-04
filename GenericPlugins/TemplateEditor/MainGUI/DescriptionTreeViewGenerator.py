class Generator(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect_after("selected-language-id", self.__language_cb)
		self.__sigid3 = manager.connect("templates-dictionary", self.__dictionary_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__language = None
		self.__dictionary = {}
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return False

	def __send_treeview_data(self):
		data = self.__get_data()
		self.__manager.emit("description-treeview-data", data)
		return

	def __get_data(self):
		if not self.__language: return []
		if not self.__dictionary: return []
		language =self.__language + "|"
		data = []
		for key in self.__dictionary.keys():
			if not (key.startswith(language)): continue
			description = self.__dictionary[key][0]
			trigger = key[len(language):]
			data.append((trigger, description, key))
		return data

	def __precompile_methods(self):
		methods = (self.__send_treeview_data, self.__get_data)
		self.__editor.optimize(methods)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __language_cb(self, manager, language):
		self.__language = language
		self.__send_treeview_data()
		return False

	def __dictionary_cb(self, manager, dictionary):
		self.__dictionary = dictionary
		self.__send_treeview_data()
		return False
