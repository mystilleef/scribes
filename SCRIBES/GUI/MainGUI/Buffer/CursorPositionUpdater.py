class Updater(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("cursor-moved", self.__update_cb)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__buffer = editor.textbuffer
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__remove_timers()
		self.__update()
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __update_database(self):
		self.__remove_timers()
		from gobject import timeout_add
		self.__timer = timeout_add(3000, self.__update_async, priority=9999)
		return False

	def __update_async(self):
		from gobject import idle_add
		self.__timer1 = idle_add(self.__update, priority=9999)
		return False

	def __update(self):
		if not self.__editor.uri: return False
		cursor = self.__editor.cursor
		position = cursor.get_line(), cursor.get_line_index()
		from SCRIBES.CursorMetadata import set_value
		set_value(self.__editor.uri, position)
		return False

	def __remove_timers(self):
		try:
			from gobject import source_remove
			source_remove(self.__timer)
			source_remove(self.__timer1)
		except AttributeError:
			pass
		return  

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __update_cb(self, *args):
		self.__update_database()
		return False
