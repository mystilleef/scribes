class Manager(object):

	def __init__(self, editor, uri):
		self.__init_attributes(editor, uri)
		self.__set(uri)
		self.__sigid1 = editor.connect("checking-file", self.__checking_file_cb)
		self.__sigid2 = editor.connect("load-error", self.__load_error_cb)
		self.__sigid3 = editor.connect("saved-file", self.__saved_file_cb)
		self.__sigid4 = editor.connect("quit", self.__destroy_cb)
		editor.register_object(self)

	def __init_attributes(self, editor, uri):
		self.__editor = editor
		self.__uri = uri
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __set(self, uri=None):
		uri = uri if uri else None
		self.__editor.set_data("uri", uri)
		from gnomevfs import URI
		uri_object = URI(uri) if uri else None
		self.__editor.set_data("uri_object", uri_object)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __checking_file_cb(self, editor, uri):
		self.__set(uri)
		return False

	def __load_error_cb(self, *args):
		self.__set()
		return False

	def __saved_file_cb(self, editor, uri, encoding):
		self.__set(uri)
		return False
