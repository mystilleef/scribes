from SCRIBES.SignalConnectionManager import SignalManager

class Checker(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "check-pair-range", self.__check_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __check(self, offsets):
		from Exceptions import OutOfRange
		try:
			end_offset = offsets[1]
			editor = self.__editor
			cursor_offset = editor.selection_bounds[1].get_offset() if editor.has_selection else editor.cursor.get_offset()
			if end_offset < cursor_offset: raise OutOfRange
			self.__manager.emit("select-offsets", offsets)
		except OutOfRange:
			self.__manager.emit("find-open-character", offsets[0]-1)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __check_cb(self, manager, offsets):
		from gobject import idle_add
		idle_add(self.__check, offsets)
		return False
