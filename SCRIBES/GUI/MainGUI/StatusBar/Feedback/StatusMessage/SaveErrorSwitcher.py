class Switcher(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("save-error", self.__error_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __update(self):
		from gettext import gettext as _
		message = _("Failed to save file")
		self.__manager.emit("update", message, "no", 7)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __error_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__update, priority=9999)
		return False
