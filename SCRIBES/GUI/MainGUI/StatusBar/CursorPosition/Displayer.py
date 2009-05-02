from gettext import gettext as _

class Displayer(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("update", self.__update_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		self.__label = editor.gui.get_widget("StatusCursorPosition")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __update(self, position):
		line, column = position
		self.__label.set_label(_("<b>Ln</b> %s <b>Col</b> %s") % (str(line), str(column)))
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __update_cb(self, manager, position):
		from gobject import idle_add
		idle_add(self.__update, position, priority=9999)
		return False
