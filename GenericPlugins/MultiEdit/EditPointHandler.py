from SCRIBES.SignalConnectionManager import SignalManager
from Utils import MARK_NAME

class Handler(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "toggle-edit-point", self.__toggle_cb)
		self.connect(manager, "add-edit-point", self.__add_cb)
		self.connect(manager, "remove-edit-point", self.__remove_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__buffer = editor.textbuffer
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __is_valid(self, mark):
		if mark.get_name() is None: return False
		if mark.get_name().startswith(MARK_NAME): return True
		return False

	def __edit_point_exists(self):
		marks = self.__editor.cursor.get_marks()
		if not marks: return False
		edit_point_exists = lambda mark: 1 if self.__is_valid(mark) else 0
		results = [edit_point_exists(mark) for mark in marks]
		if 1 in results: return True
		return False

	def __toggle(self):
		emit = self.__manager.emit
		emit("remove-edit-point") if self.__edit_point_exists() else emit("add-edit-point")
		return False

	def __add(self):
		if self.__edit_point_exists(): return False
		from time import time
		name = MARK_NAME + str(time())
		self.__editor.refresh(False)
		mark = self.__buffer.create_mark(name, self.__editor.cursor)
		self.__editor.refresh(False)
		mark.set_visible(True)
		self.__editor.refresh(False)
		self.__manager.emit("add-mark", mark)
		return False

	def __remove(self):
		marks = self.__editor.cursor.get_marks()
		edit_points = [mark for mark in marks if self.__is_valid(mark)]
		self.__manager.emit("remove-mark", edit_points)
		from Utils import delete_mark
		from copy import copy
		[delete_mark(self.__buffer, mark) for mark in copy(edit_points)]
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __toggle_cb(self, *args):
		self.__toggle()
		return False

	def __add_cb(self, *args):
		self.__add()
		return False

	def __remove_cb(self, *args):
		self.__remove()
		return False
