from gettext import gettext as _
MESSAGE = _("Rename Document")

class Updater(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect_after("show", self.__show_cb)
		self.__sigid3 = manager.connect_after("hide", self.__hide_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		del self
		self = None
		return False

	def __show(self):
		self.__editor.busy()
		self.__editor.set_message(MESSAGE, "save")
		return False

	def __hide(self):
		self.__editor.busy(False)
		self.__editor.unset_message(MESSAGE, "save")
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __hide_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__hide)
		return False

	def __show_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__show)
		return False
