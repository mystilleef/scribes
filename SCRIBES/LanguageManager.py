class Manager(object):

	def __init__(self, editor, uri):
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("checking-file", self.__loaded_file_cb)
		self.__sigid3 = editor.connect("renamed-file", self.__loaded_file_cb)
		self.__sigid4 = editor.connect("load-error", self.__load_error_cb)
		self.__set(uri)
		self.__editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __set(self, uri):
		from Utils import get_language
		language_object = get_language(uri) if uri else None
		self.__editor.set_data("language_object", language_object)
		language = language_object.get_id() if language_object else ""
		self.__editor.set_data("language", language)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __loaded_file_cb(self, editor, uri, *args):
		self.__set(uri)
		return False

	def __load_error_cb(self, *args):
		self.__set(None)
		return False
