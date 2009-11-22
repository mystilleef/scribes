class Handler(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("readonly-error", self.__error_cb)
		editor.register_object(self)
		editor.response()

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
		return False

	def __error(self):
		from gettext import gettext as _
		message = _("ERROR: Failed to perform operation in readonly mode")
		self.__editor.update_message(message, "fail")
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __error_cb(self, *args):
		self.__editor.response()
		from gobject import idle_add
		idle_add(self.__error, priority=9999)
		return False
