class Manager(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("readonly", self.__readonly_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__view = editor.textview
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __set(self, readonly):
		self.__editor.response()
		self.__view.props.editable = not readonly
		self.__view.props.highlight_current_line = not readonly
		self.__view.props.show_line_numbers = not readonly
		self.__view.props.cursor_visible = not readonly
		self.__editor.response()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __readonly_cb(self, editor, readonly):
		from gobject import idle_add
		idle_add(self.__set, readonly)
		return False
