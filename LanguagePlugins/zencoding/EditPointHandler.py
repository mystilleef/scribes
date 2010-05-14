from SCRIBES.SignalConnectionManager import SignalManager

ACTION_LIST = ("expand_abbreviation", "expand_with_abbreviation", "wrap_with_abbreviation")

class Handler(SignalManager):

	def __init__(self, manager, editor, zeditor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor, zeditor)
		self.connect(manager, "destroy", self.__quit_cb)
		self.connect(manager, "action", self.__action_cb)
		self.connect(manager, "insertion-offsets", self.__offsets_cb)

	def __init_attributes(self, manager, editor, zeditor):
		self.__manager = manager
		self.__editor = editor
		self.__zeditor = zeditor
		self.__ignore = False
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __place_cursor_at_edit_point(self, offsets):
		start_offset, end_offset = offsets
		iterator = self.__editor.textbuffer.get_iter_at_offset(start_offset+1)
		self.__editor.textbuffer.place_cursor(iterator)
		from zen_actions import next_edit_point
		next_edit_point(self.__zeditor)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __offsets_cb(self, manager, offsets):
		if self.__ignore: return False
		self.__place_cursor_at_edit_point(offsets)
		return False

	def __action_cb(self, manager, action):
		self.__ignore = False if action in ACTION_LIST else True
		return False
