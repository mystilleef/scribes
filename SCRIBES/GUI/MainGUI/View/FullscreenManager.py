from SCRIBES.SignalConnectionManager import SignalManager

class Manager(SignalManager):

	def __init__(self, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(editor)
		self.connect(editor, "fullscreen", self.__fullscreen_cb, True)
		self.connect(editor, "quit", self.__quit_cb)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__view = editor.textview
		self.__justification = self.__view.get_justification()
		self.__lmargin = self.__view.get_left_margin()
		self.__rmargin = self.__view.get_right_margin()
		return False

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __update(self, fullscreen):
		self.__editor.response()
		self.__view.set_property("show-right-margin", False if fullscreen else self.__margin())
		self.__view.set_property("show-line-numbers", False if fullscreen else True)
		self.__view.set_left_margin(self.__adjust_margin() if fullscreen else self.__lmargin)
#		self.__view.set_right_margin(self.__adjust_margin(width, False) if fullscreen else self.__rmargin)
		self.__editor.response()
		return False

	def __adjust_margin(self, left=True):
		width = self.__view.get_visible_rect()[2]
		multiplier = 0.4 if left else 0.666
		return int(multiplier * width)

	def __margin(self):
		language = self.__editor.language
		language = language	if language else "plain text"
		from SCRIBES.DisplayRightMarginMetadata import get_value as show_margin
		return show_margin(language)

	def __fullscreen_cb(self, editor, fullscreen):
		from gobject import idle_add
		idle_add(self.__update, fullscreen, priority=9999)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False
