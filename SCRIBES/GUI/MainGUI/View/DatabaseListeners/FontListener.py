class Listener(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monid = monitor_add(self.__uri, MONITOR_FILE, self.__changed_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__view = editor.textview
		self.__uri = manager.get_database_uri("Font.gdb")
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
		self.__editor.response()
		from pango import FontDescription
		from SCRIBES.FontMetadata import get_value
		new_font = FontDescription(get_value())
		self.__view.modify_font(new_font)
		self.__editor.response()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __changed_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__update)
		return False
