class Generator(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__generate()
		self.__destroy()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		del self
		self = None
		return False

	def __generate(self):
		data = []
		for encoding, alias, language in self.__editor.supported_encodings:
			data.append([False, encoding, language])
		self.__manager.emit("model-data", data)
		return False
