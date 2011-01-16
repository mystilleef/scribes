from SCRIBES.SignalConnectionManager import SignalManager

class Inserter(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "valid-string", self.__valid_cb)
		self.connect(manager, "insert-text", self.__insert_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__string = ""
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __insert(self, text):
		self.__manager.emit("inserting-text")
		self.__editor.begin_user_action()
		self.__editor.textbuffer.insert_at_cursor(text[len(self.__string):].encode("utf8"))
		self.__manager.emit("inserted-text")
		self.__editor.end_user_action()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __valid_cb(self, manager, string):
		self.__string = string
		return False

	def __insert_cb(self, manager, text):
		from gobject import idle_add, PRIORITY_HIGH
		idle_add(self.__insert, text, priority=PRIORITY_HIGH)
#		self.__insert(text)
		return False
