from SCRIBES.SignalConnectionManager import SignalManager

class SpinButton(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "show", self.__show_cb, True)
		self.connect(self.__button, "activate", self.__activate_cb)
		self.__sigid1 = self.connect(self.__button, "value-changed", self.__changed_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__button = manager.gui.get_object("SpinButton")
		return

	def __destroy(self):
		self.disconnect()
		del self
		return

	def __set_value(self):
		self.__button.handler_block(self.__sigid1)
		self.__button.set_range(1, self.__editor.textbuffer.get_line_count())
		line = self.__editor.cursor.get_line() + 1
		self.__button.set_value(line)
		self.__button.handler_unblock(self.__sigid1)
		self.__button.props.sensitive = True
		self.__button.grab_focus()
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __show_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__set_value)
		return False

	def __activate_cb(self, *args):
		self.__manager.emit("hide")
		return False

	def __changed_cb(self, *args):
		self.__manager.emit("line-number", self.__button.get_value())
		return False
