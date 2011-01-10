from SCRIBES.SignalConnectionManager import SignalManager

class NewLineInserter(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.__sigid1 = self.connect(editor.textbuffer, "insert-text", self.__insert_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __insert_cb(self, textbuffer, iterator, text, length):
		if text not in ("\n", "\r", "\r\n"): return False
		textbuffer.emit_stop_by_name("insert-text")
		self.__editor.freeze()
		textbuffer.handler_block(self.__sigid1)
		indentation = self.__editor.line_indentation
		newline = self.__editor.newline_character
		text = "%s%s" % (newline, indentation)
		textbuffer.begin_user_action()
		textbuffer.insert_at_cursor(text)
		textbuffer.end_user_action()		
		textbuffer.handler_unblock(self.__sigid1)
		self.__editor.thaw()
		return True

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False
