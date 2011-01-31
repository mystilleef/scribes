from SCRIBES.SignalConnectionManager import SignalManager

class Monitor(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(self.__view, "key-press-event", self.__event_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__view = editor.textview
		self.__buffer = editor.textbuffer
		self.__brackets = {"}":"{", "]":"[", ">":"<", ")":"("}
		return

	def __get_bracket_data(self):
		close_bracket, open_bracket = None, None
		close_iter, open_iter = None, None
		start_pos, end_pos = self.__editor.get_line_bounds()
		iterator = self.__editor.cursor.copy()
		from gtk import TEXT_SEARCH_VISIBLE_ONLY as VISIBLE
		for close_bracket in self.__brackets:
			match = iterator.forward_search(close_bracket, VISIBLE, limit=end_pos)
			if not match: continue
			close_iter = match[1]
			open_bracket = self.__brackets[close_bracket]
			match = iterator.backward_search(open_bracket, VISIBLE, limit=start_pos)
			if not match: continue
			open_iter = match[0]
			break
		result = close_bracket and open_bracket and close_iter and open_iter
		if result: return open_iter, close_iter, open_bracket, close_bracket
		return None

	def __bracket_is_empty(self, bracket_region):
		string = self.__buffer.get_text(*bracket_region)[1:-1]
		if not string: return True
		return string.isspace()

	def __event_cb(self, view, event):
		from gtk.keysyms import Return
		if event.keyval != Return: return False
		bracket_data = self.__get_bracket_data()
		if not bracket_data: return False
		open_iter, close_iter, open_bracket, close_bracket = bracket_data
		if self.__bracket_is_empty((open_iter, close_iter)) is False: return False
		self.__manager.emit("mark-bracket-region", (open_iter, close_iter))
		self.__manager.emit("empty-brackets", (open_bracket, close_bracket))
		return True

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False
