from SCRIBES.SignalConnectionManager import SignalManager

class Reseter(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "lines", self.__lines_cb)
		self.connect(editor, "reset-buffer", self.__reset_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__lines = ()
		self.__update = True
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __reset(self, operation):
		if operation == "begin":
			self.__update = False
			self.__manager.emit("feedback", False)
		else:
			self.__manager.emit("remove-all")
			self.__manager.emit("bookmark-lines", self.__lines)
			self.__update = True
			from gobject import timeout_add
			timeout_add(250, self.__enable_feedback, priority=9999)
		return False

	def __enable_feedback(self):
		self.__manager.emit("feedback", True)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __reset_cb(self, editor, operation):
		self.__reset(operation)
		return False

	def __lines_cb(self, manager, lines):
		if self.__update is False: return False
		self.__lines = lines
		return False
