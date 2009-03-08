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
		self.__uri = manager.get_database_uri("DisplayRightMargin.gdb")
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
		from SCRIBES.DisplayRightMarginMetadata import get_value
		self.__view.set_property("show-right-margin", get_value())
		self.__editor.refresh()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __changed_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__update)
		return False
