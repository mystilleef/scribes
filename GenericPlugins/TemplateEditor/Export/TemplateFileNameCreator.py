class Creator(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("selected-language-id", self.__language_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __emit_filename_signal(self, language_id):
		filename = language_id + "-templates.xml"
		self.__manager.emit("export-template-filename", filename)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __language_cb(self, manager, language_id):
		self.__emit_filename_signal(language_id)
		return False
