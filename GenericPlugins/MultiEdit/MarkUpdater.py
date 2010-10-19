from SCRIBES.SignalConnectionManager import SignalManager

class Updater(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "deactivate", self.__clear_cb)
		self.connect(manager, "clear", self.__clear_cb)
		self.connect(manager, "add-mark", self.__add_cb)
		self.connect(manager, "remove-mark", self.__remove_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__marks = []
		self.__buffer = editor.textbuffer
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __add(self, mark):
		self.__marks.append(mark)
		self.__manager.emit("edit-points", self.__marks)
		return False

	def __remove(self, mark):
		if mark in self.__marks: self.__marks.remove(mark)
		self.__manager.emit("edit-points", self.__marks)
		return False

	def __delete_marks(self):
		self.__manager.emit("edit-points", [])
		from copy import copy
		self.__editor.textview.window.freeze_updates()
		from Utils import delete_mark
		[delete_mark(self.__buffer, mark) for mark in copy(self.__marks)]
		self.__marks = []
		self.__editor.textview.window.thaw_updates()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __add_cb(self, manager, mark):
		self.__add(mark)
		return False

	def __remove_cb(self, manager, marks):
		[self.__remove(mark) for mark in marks]
		return False

	def __clear_cb(self, *args):
		self.__delete_marks()
		return False
