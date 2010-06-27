class Updater(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("set-data", self.__set_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __set(self, indentation):
		from Metadata import set_value
		set_value(indentation)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __set_cb(self, manager, indentation):
		from gobject import idle_add
		idle_add(self.__set, indentation, priority=9999)
		return False
