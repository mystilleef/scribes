from SCRIBES.SignalConnectionManager import SignalManager

class Reader(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(editor, "loaded-file", self.__update_cb)
		self.connect(manager, "destroy", self.__destroy_cb)
		from gobject import idle_add
		idle_add(self.__update, priority=9999)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __update(self):
		uri = self.__editor.uri
		if not uri: return False
		from Metadata import get_value
		self.__editor.response()
		lines = get_value(str(uri))
		self.__editor.response()
		if not lines: return False
		self.__manager.emit("bookmark-lines", lines)
		return False

	def __update_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__update, priority=9999)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
