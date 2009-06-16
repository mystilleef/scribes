class Manager(object):

	def __init__(self, editor):
		editor.response()
		self.__init_attributes(editor)
		self.__sigid4 = editor.connect("quit", self.__quit_cb)
		self.__sigid6 = editor.connect("new-encoding-list", self.__new_encoding_list_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__utf8_encodings = ["utf-8", "utf8", "UTF8", "UTF-8", "Utf-8"]
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.disconnect_signal(self.__sigid6, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return

	def __set_encoding_list(self, new_encoding_list):
		from EncodingMetadata import set_value
		set_value(new_encoding_list)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return

	def __new_encoding_list_cb(self, editor, new_encoding_list):
		self.__set_encoding_list(new_encoding_list)
		return False
