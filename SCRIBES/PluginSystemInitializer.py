class Initializer(object):

	def __init__(self, editor, uri):
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect_after("loaded-file", self.__loaded_cb)
		self.__sigid2 = editor.connect("load-error", self.__loaded_cb)
		if not uri: self.__init_plugins()

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
		self.__editor.refresh()
		self.__editor.move_view_to_cursor(True)
		self.__editor.refresh()
		self.__editor.emit("ready")
		from PluginManager import Manager
		Manager(self.__editor)
		from LanguagePluginManager import Manager
		Manager(self.__editor)
		self.__destroy()
		return False

	def __loaded_cb(self, *args):
		self.__init_plugins()
		return False
