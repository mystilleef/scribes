class Generator(object):

	def __init__(self, manager):
		self.__init_attributes(manager)
		manager.connect("update", self.__update_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		self.__dictionary = {}
		from dbus import Dictionary, String, Int32
		try:
			self.__empty_dict = Dictionary({}, signature="ss")
		except:
			self.__empty_dict = Dictionary({}, key_type=String, value_type=Int32)
		return

	def __update(self, dictionary):
		try:
			from Utils import merge, no_zero_value_dictionary, utf8_dictionary
			_dictionary = merge(self.__dictionary, dictionary) if self.__dictionary else dictionary
			__dictionary = no_zero_value_dictionary(_dictionary)
			if not __dictionary: raise ValueError
			self.__dictionary = utf8_dictionary(__dictionary)
			self.__manager.emit("finished", self.__dictionary)
		except ValueError:
			self.__manager.emit("finished", self.__empty_dict)
		return False

	def __remove_timer(self):
		try:
			from gobject import source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		return

	def __update_cb(self, manager, dictionary):
		self.__remove_timer()
		from gobject import idle_add, PRIORITY_LOW
		self.__timer = idle_add(self.__update, dictionary, priority=PRIORITY_LOW)
		return False
