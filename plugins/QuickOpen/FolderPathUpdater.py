class Updater(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("parent-path", self.__parent_cb)
		self.__sigid3 = manager.connect("show", self.__show_cb)
		self.__sigid4 = manager.connect("hide", self.__hide_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__path = ""
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		del self
		self = None
		return False

	def __update(self, parent=False):
		pwduri = self.__path if self.__path else self.__editor.pwd_uri
		from gio import File
		self.__path = File(pwduri).get_parent().get_uri() if parent else pwduri
		self.__manager.emit("current-path", self.__path)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __parent_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__update, True)
		return False

	def __show_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__update)
		return False

	def __hide_cb(self, *args):
		self.__path = ""
		return False
