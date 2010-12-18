from SCRIBES.SignalConnectionManager import SignalManager

class Remover(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "placeholder-marks", self.__marks_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __rm(self, marks):
		giam = self.__editor.textbuffer.get_iter_at_mark
		start, end = giam(marks[0]), giam(marks[1])
		self.__editor.textbuffer.delete(start, end)
		return False

	def __remove(self, placeholder_marks):
		[self.__rm(marks) for marks in placeholder_marks]
		self.__manager.emit("removed-placeholders")
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False

	def __marks_cb(self, manager, placeholder_marks):
		self.__remove(placeholder_marks)
		return False
