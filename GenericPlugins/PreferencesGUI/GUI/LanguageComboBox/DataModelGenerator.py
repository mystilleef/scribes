class Generator(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		from gobject import idle_add
		idle_add(self.__generate, priority=9999)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signals(((self.__sigid1, self.__manager),))
		del self
		self = None
		return False

	def __extract(self, _object):
		self.__editor.response()
		return _object.get_name(), _object.get_id()

	def __generate(self):
		data = [self.__extract(_object) for _object in self.__editor.language_objects]
		self.__manager.emit("language-combobox-data", data)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
