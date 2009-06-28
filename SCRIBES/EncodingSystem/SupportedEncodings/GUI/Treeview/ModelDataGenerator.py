class Generator(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__generate()
		self.__destroy()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.response()
		del self
		self = None
		return False

	def __generate(self):
		data = []
		for encoding, alias, language in self.__editor.supported_encodings:
			self.__editor.response()
			data.append([False, encoding, language])
		self.__manager.emit("model-data", data)
		return False
