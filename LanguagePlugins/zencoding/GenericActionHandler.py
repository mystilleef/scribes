from SCRIBES.SignalConnectionManager import SignalManager

IGNORE_LIST = ("wrap_with_abbreviation", )

class Handler(SignalManager):

	def __init__(self, manager, editor, zeditor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor, zeditor)
		self.connect(manager, "destroy", self.__quit_cb)
		self.connect(manager, "action", self.__action_cb)

	def __init_attributes(self, manager, editor, zeditor):
		self.__manager = manager
		self.__editor = editor
		self.__zeditor = zeditor
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __action(self, action):
		from zen_core import run_action
		self.__zeditor.set_context(self.__editor)
		run_action(action, self.__zeditor)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __action_cb(self, manager, action):
		if action in IGNORE_LIST: return False
		from gobject import idle_add
		idle_add(self.__action, action)
		return False
