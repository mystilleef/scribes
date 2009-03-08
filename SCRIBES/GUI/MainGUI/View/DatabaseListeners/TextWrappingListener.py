class Listener(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monid = monitor_add(self.__uri, MONITOR_FILE, self.__changed_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__view = editor.textview
		self.__uri = manager.get_database_uri("TextWrapping.gdb")
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		from gnomevfs import monitor_cancel
		monitor_cancel(self.__monid)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __update(self):
		from gtk import WRAP_NONE, WRAP_WORD_CHAR
		from SCRIBES.TextWrappingMetadata import get_value
		wrap_mode = self.__view.set_wrap_mode
		wrap_mode(WRAP_WORD_CHAR) if get_value() else wrap_mode(WRAP_NONE)
		self.__editor.refresh()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __changed_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__update)
		return False
