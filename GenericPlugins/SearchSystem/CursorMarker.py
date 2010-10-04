class Marker(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("show-bar", self.__show_cb)
		self.__sigid3 = manager.connect("hide-bar", self.__hide_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__mark = None
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return

	def __update(self):
		self.__mark = self.__editor.mark(self.__editor.cursor)
		self.__manager.emit("cursor-mark", self.__mark)
		return False

	def __delete(self):
		self.__editor.delete_mark(self.__mark)
		self.__mark = None
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __show_cb(self, *args):
		self.__update()
		return False

	def __hide_cb(self, *args):
		self.__delete()
		return False
