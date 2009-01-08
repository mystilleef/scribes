class Manager(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("updated-dictionary", self.__updated_dictionary_cb)
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=9999)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__dictionary = {}
		return 

	def __destroy(self):
		self.__dictionary.clear()
		del self.__dictionary
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return 

	def __update(self, dictionary):
		self.__dictionary.clear()
		self.__dictionary.update(dictionary)
		self.__manager.emit("dictionary", self.__dictionary)
		self.__manager.emit("finished-indexing")
		return False

	def __precompile_methods(self):
		methods = (self.__update, self.__updated_dictionary_cb,)
		self.__editor.optimize(methods)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __updated_dictionary_cb(self, manager, dictionary):
		from gobject import idle_add
		idle_add(self.__update, dictionary, priority=9999)
		return False
