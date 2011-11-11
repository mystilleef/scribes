from SCRIBES.SignalConnectionManager import SignalManager

class Updater(SignalManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		self.__init_attributes(editor)
		self.connect(editor, "close", self.__quit_cb)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__buffer = editor.textbuffer
		return

	def __destroy(self):
		self.disconnect()
		self.__update()
		self.__editor.unregister_object(self)
		del self
		return False

	def __update(self):
		if not self.__editor.uri: return False
		cursor = self.__editor.cursor
		position = cursor.get_line(), cursor.get_line_index()
		from SCRIBES.CursorMetadata import set_value
		set_value(self.__editor.uri, position)
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False
