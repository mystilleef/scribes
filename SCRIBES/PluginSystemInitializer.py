class Initializer(object):

	def __init__(self, editor, uri):
		editor.response()
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect_after("loaded-file", self.__loaded_cb)
		self.__sigid2 = editor.connect("load-error", self.__loaded_cb)
		if not uri: self.__init_plugins()
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		del self
		self = None
		return

	def __init_plugins(self):
		self.__editor.response()
#		self.__editor.textview.window.freeze_updates()
#		self.__editor.move_view_to_cursor(True)
#		self.__editor.textview.window.thaw_updates()
		from PluginInitializer.Manager import Manager
		Manager(self.__editor)
		self.__editor.emit("ready")
		self.__editor.refresh()
		self.__destroy()
		return False

	def __loaded_cb(self, *args):
		self.__editor.response()
		from gobject import idle_add
		idle_add(self.__init_plugins, priority=999999)
		return False
