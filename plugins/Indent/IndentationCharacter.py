from SCRIBES.SignalConnectionManager import SignalManager

class Character(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "indent", self.__process_cb)
		self.connect(manager, "unindent", self.__process_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __send_character(self):
		use_spaces = self.__editor.textview.get_insert_spaces_instead_of_tabs()
		if use_spaces:
			width = self.__editor.textview.get_tab_width()
			self.__manager.emit("character", (" " * width))
		else:
			self.__manager.emit("character", "\t")
		return

	def __destroy(self):
		self.disconnect()
		del self
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __process_cb(self, *args):
		self.__send_character()
		return False
