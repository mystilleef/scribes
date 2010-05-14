from SCRIBES.SignalConnectionManager import SignalManager

class Handler(SignalManager):

	def __init__(self, manager, editor, zeditor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor, zeditor)
		self.connect(manager, "destroy", self.__quit_cb)
		self.connect(manager, "action", self.__action_cb)
		self.connect(manager, "wrap-abbreviation", self.__wrap_cb)
		self.connect(manager, "selection-marks", self.__marks_cb)

	def __init_attributes(self, manager, editor, zeditor):
		self.__manager = manager
		self.__editor = editor
		self.__zeditor = zeditor
		self.__gui = None
		self.__bmark = None
		self.__emark = None
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __create_gui(self):
		from GUI.Manager import Manager
		gui = Manager(self.__manager, self.__editor)
		return gui

	def __show(self):
		if not self.__gui: self.__gui = self.__create_gui()
		self.__gui.show()
		return False

	def __expand(self, abbreviation):
		self.__zeditor.set_context(self.__editor)
		self.__editor.textview.grab_focus()
		if self.__bmark: #raise ValueError
			start_iterator = self.__editor.textbuffer.get_iter_at_mark(self.__bmark)
			end_iterator = self.__editor.textbuffer.get_iter_at_mark(self.__emark)
			self.__editor.textbuffer.select_range(start_iterator, end_iterator)
		self.__manager.emit("action", "wrap_with_abbreviation")
		from zen_core import run_action
		run_action("wrap_with_abbreviation", self.__zeditor, abbreviation)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __action_cb(self, manager, action):
		if action != "wrap_with_abbreviation": return False
		from gobject import idle_add
		idle_add(self.__show)
		return False

	def __wrap_cb(self, manager, abbreviation):
		from gobject import idle_add
		idle_add(self.__expand, abbreviation)
		return False

	def __marks_cb(self, manager, marks):
		self.__bmark, self.__emark = marks
		return False
