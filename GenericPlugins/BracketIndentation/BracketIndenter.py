from SCRIBES.SignalConnectionManager import SignalManager

class Indenter(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "empty-brackets", self.__brackets_cb, True)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __format(self, brackets):
		indentation = self.__editor.line_indentation
		newline = self.__editor.newline_character
		open_bracket, close_bracket = brackets
		tab_width = self.__editor.tab_width
		whitespace = "\t" if self.__editor.tabs_instead_of_spaces else " " * tab_width
		string = "%s%s%s%s%s%s%s" % (
			open_bracket, newline,
			indentation, whitespace, newline, 
			indentation, close_bracket
		)
		self.__manager.emit("insert", string)
		return False

	def __brackets_cb(self, manager, brackets):
		self.__format(brackets)
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False
