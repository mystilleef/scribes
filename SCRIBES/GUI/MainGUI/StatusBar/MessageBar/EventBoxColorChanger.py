from SCRIBES.SignalConnectionManager import SignalManager

class Changer(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__destroy_cb)
		self.connect(manager, "bar", self.__bar_cb)
		self.connect(editor, "syntax-color-theme-changed", self.__changed_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__bar = None
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __change_color(self):
		if not self.__bar: return False
		self.__bar.set_style(None)
		color = self.__editor.view_bg_color
		if color is None: return False
		style = self.__bar.get_style().copy()
		from gtk import STATE_NORMAL
		style.bg[STATE_NORMAL] = color
		self.__bar.set_style(style)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __bar_cb(self, manager, bar):
		self.__bar = bar
		from gobject import idle_add
		idle_add(self.__change_color)
		return False

	def __changed_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__change_color)
		return False
