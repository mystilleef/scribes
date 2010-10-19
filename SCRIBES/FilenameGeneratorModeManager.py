class Manager(object):

	def __init__(self, editor, uri):
		self.__init_attributes(editor)
		set_data = lambda generate: editor.set_data("generate_filename", generate)
		set_data(False) if uri else set_data(True)
		self.__sigid1 = editor.connect("checking-file", self.__checking_file_cb)
		self.__sigid2 = editor.connect("load-error", self.__load_error_cb)
		self.__sigid3 = editor.connect("renamed-file", self.__checking_file_cb)
		self.__sigid4 = editor.connect("rename-file", self.__checking_file_cb)
		self.__sigid5 = editor.connect("quit", self.__quit_cb)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.disconnect_signal(self.__sigid5, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __checking_file_cb(self, *args):
		self.__editor.set_data("generate_filename", False)
		return False

	def __load_error_cb(self, *args):
		self.__editor.set_data("generate_filename", True)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False
