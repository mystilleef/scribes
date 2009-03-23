class Buffer(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__set_properties()
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__buffer = editor.textbuffer
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __set_properties(self):
		self.__buffer.begin_not_undoable_action()
		self.__buffer.set_property("highlight-syntax", True)
		self.__buffer.set_property("highlight-matching-brackets", False)
		self.__buffer.set_property("max-undo-levels", -1)
		self.__buffer.set_text("")
		start, end = self.__buffer.get_bounds()
		self.__buffer.remove_all_tags(start, end)
		self.__buffer.remove_source_marks(start, end)
		self.__buffer.end_not_undoable_action()
		return

	def __quit_cb(self, *args):
		self.__destroy()
		return False
