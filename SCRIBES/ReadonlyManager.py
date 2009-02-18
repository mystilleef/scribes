class Manager(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__editor.set_data("readonly", False)
		self.__sigid1 = editor.connect("loaded-file", self.__loaded_cb)
		self.__sigid2 = editor.connect("renamed-file", self.__loaded_cb)
		self.__sigid3 = editor.connect("toggle-readonly", self.__toggle_cb)
		self.__sigid4 = editor.connect("quit", self.__quit_cb)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
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

	def __set(self, readonly):
		self.__editor.set_data("readonly", readonly)
		self.__editor.emit("readonly", readonly)
		return False

	def __check(self, uri):
		self.__set(False) if self.__can_write(uri) else self.__set(True)
		return False

	def __toggle(self):
		try:
			if not self.__can_write(self.__editor.uri): raise ValueError
			self.__set(False) if self.__editor.readonly else self.__set(True)
		except ValueError:
			print "Error: You do not have permission to write to the file."
		return False

	def __can_write(self, uri):
		from Utils import check_uri_permission #FIXME: Bad function name
		return check_uri_permission(uri)

	def __loaded_cb(self, editor, uri, encoding):
		self.__check(uri)
		return False

	def __toggle_cb(self, *args):
		self.__toggle()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False
