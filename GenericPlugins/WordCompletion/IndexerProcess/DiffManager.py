from SCRIBES.SignalConnectionManager import SignalManager

class Manager(SignalManager):

	def __init__(self, manager):
		SignalManager.__init__(self)
		self.__init_attributes(manager)
		self.connect(manager, "index", self.__index_cb)

	def __init_attributes(self, manager):
		self.__manager = manager
		self.__old_text = ""
		from difflib import Differ
		self.__differ = Differ()
		return

	def __index(self, content):
		text1 = self.__old_text.splitlines(1)
		text2 = content.splitlines(1)
		result = self.__differ.compare(text1, text2)
		is_delta = lambda line: line.startswith("+") or line.startswith("-")
		diff_lines = [line for line in result if is_delta(line)]
		from Utils import index, merge, no_zero_value_dictionary
		removed_lines = "".join([line for line in diff_lines if line.startswith("-")])
		removed_dictionary = index(removed_lines, negative=True)
		added_lines = "".join([line for line in diff_lines if line.startswith("+")])
		added_dictionary = index(added_lines)
		merged_dictionary = merge(removed_dictionary, added_dictionary)
		diff_dictionary = no_zero_value_dictionary(merged_dictionary)
		if diff_dictionary:
			self.__manager.emit("update", diff_dictionary)
		else:
			self.__manager.emit("no-change")
		self.__old_text = content
		return

	def __index_cb(self, manager, content):
		self.__index(content)
		return False
