from SCRIBES.SignalConnectionManager import SignalManager

class Commenter(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "comment", self.__comment_cb)
		self.connect(manager, "uncomment", self.__uncomment_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __comment(self, text):
		commented_lines = (self.__comment_line(line) for line in text.splitlines())
		string = self.__editor.newline_character.join(commented_lines)
		from gobject import idle_add
		idle_add(self.__manager.emit, "processed", string)
		return False

	def __uncomment(self, text):
		uncommented_lines = (self.__uncomment_line(line) for line in text.splitlines())
		string = self.__editor.newline_character.join(uncommented_lines)
		from gobject import idle_add
		idle_add(self.__manager.emit, "processed", string)
		return False

	def __comment_line(self, string):
		if self.__is_empty_line(string): return string
		indentation = self.__get_indentation(string)
		_string = string.lstrip(" \t")
		if _string.startswith("#"): return string
		return "%s%s%s" % (indentation, "# ", _string)

	def __uncomment_line(self, string):
		if self.__is_empty_line(string): return string
		indentation = self.__get_indentation(string)
		_string = string.lstrip(" \t")
		if _string.startswith("#") is False: return string
		_string = _string.lstrip("# \t") if indentation else _string.lstrip("#")
		if not indentation and _string.startswith(" "): _string = _string[1:]
		return "%s%s" % (indentation, _string)

	def __get_indentation(self, string):
		indentation = []
		for character in string:
			if character not in (" ", "\t"): break
			indentation.append(character)
		return "".join(indentation)

	def __is_empty_line(self, string):
		if not string: return True
		if not string.strip(" \t"): return True
		return False

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __comment_cb(self, manager, text):
		from gobject import idle_add
		idle_add(self.__comment, text)
		return False

	def __uncomment_cb(self, manager, text):
		from gobject import idle_add
		idle_add(self.__uncomment, text)
		return False

	def __destroy_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False
