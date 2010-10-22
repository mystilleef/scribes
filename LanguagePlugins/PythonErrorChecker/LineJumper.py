from SCRIBES.SignalConnectionManager import SignalManager

class Jumper(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "syntax-error", self.__syntax_cb)
		self.connect(manager, "tree-error", self.__tree_cb)
		self.connect(manager, "activate", self.__activate_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__can_jump = False
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __jump(self, lineno):
		iterator = self.__editor.textbuffer.get_iter_at_line(lineno-1)
		self.__editor.textbuffer.place_cursor(iterator)
		self.__editor.move_view_to_cursor(True, iterator.copy())
		self.__editor.textview.grab_focus()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __tree_cb(self, manager, data):
		if self.__can_jump is False: return False
		from gobject import idle_add, PRIORITY_HIGH
		idle_add(self.__jump, data.lineno, priority=PRIORITY_HIGH)
		self.__can_jump = False
		return False

	def __syntax_cb(self, manager, data):
		if self.__can_jump is False: return False
		from gobject import idle_add, PRIORITY_HIGH
		idle_add(self.__jump, data[0], priority=PRIORITY_HIGH)
		self.__can_jump = False
		return False

	def __activate_cb(self, *args):
		self.__can_jump = True
		return False
