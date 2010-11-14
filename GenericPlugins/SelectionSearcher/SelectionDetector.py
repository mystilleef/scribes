from SCRIBES.SignalConnectionManager import SignalManager

class Detector(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(editor, "cursor-moved", self.__moved_cb, True)
		self.connect(editor.textview, "focus-in-event", self.__moved_cb, True)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __emit(self):
		try:
			if self.__editor.has_selection is False: return False
			if self.__editor.selection_range > 1: return False
			from Utils import valid_selection
			if not valid_selection(*self.__editor.selection_bounds): return False
			self.__manager.emit("search", self.__editor.selected_text)
		except AttributeError:
			# Prevent harmless error messages from appearing in stderr.
			# Usually happens when editor object is being destroyed.
			pass
		return False

	def __emit_tcb(self):
		from gobject import idle_add, PRIORITY_LOW
		self.__timer = idle_add(self.__emit, priority=PRIORITY_LOW)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __moved_cb(self, *args):
		try:
			from gobject import source_remove, timeout_add, PRIORITY_LOW
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = timeout_add(1000, self.__emit_tcb, priority=PRIORITY_LOW)
		return False
