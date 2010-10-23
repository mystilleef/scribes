class Listener(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__monitor.connect("changed", self.__changed_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		self.__view = editor.textview
		from gio import File, FILE_MONITOR_NONE
		self.__monitor = File(manager.get_path("TextWrapping.gdb")).monitor_file(FILE_MONITOR_NONE, None)
		return

	def __destroy(self):
		self.__monitor.cancel()
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.unregister_object(self)
		del self
		return False

	def __update(self):
		from gtk import WRAP_NONE, WRAP_WORD_CHAR
		from SCRIBES.TextWrappingMetadata import get_value
		wrap_mode = self.__view.set_wrap_mode
		wrap_mode(WRAP_WORD_CHAR) if get_value(self.__manager.get_language()) else wrap_mode(WRAP_NONE)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __changed_cb(self, *args):
		monitor, gfile, otherfile, event = args
		if not (event in (0,2,3)): return False
		from gobject import idle_add
		idle_add(self.__update)
		return False
