class Updater(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("show-error", self.__update_cb, True)
		self.__sigid3 = editor.connect("show-info", self.__update_cb, False)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__window = manager.gui.get_widget("Window")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __update(self, error):
		from gettext import gettext as _
		title = _("ERROR") if error else _("INFORMATION")
		self.__window.set_title(title)
		return False

	def __update_cb(self, editor, title, message, window, busy, error):
		from gobject import idle_add
		idle_add(self.__update, error, priority=9999)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False
