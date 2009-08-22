class Updater(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("loaded-plugin", self.__loaded_cb)
		self.__sigid3 = manager.connect("unloaded-plugin", self.__unloaded_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__plugins = []
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __update(self, data, remove=False):
		self.__editor.response()
		self.__plugins.remove(data) if remove else self.__plugins.append(data)
		self.__editor.response()
		self.__manager.emit("active-plugins", self.__plugins)
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __loaded_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__update, data)
		return False

	def __unloaded_cb(self, manager, data):
		from gobject import idle_add
		idle_add(self.__update, data, True)
		return False
