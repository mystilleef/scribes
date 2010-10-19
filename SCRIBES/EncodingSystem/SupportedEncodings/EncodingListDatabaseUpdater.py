class Updater(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("selected-encodings", self.__encodings_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return

	def __update(self, encodings):
		from ..EncodingListMetadata import set_value
		set_value(encodings)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __encodings_cb(self, manager, encodings):
		from gobject import idle_add
		idle_add(self.__update, encodings, priority=9999)
		return False
