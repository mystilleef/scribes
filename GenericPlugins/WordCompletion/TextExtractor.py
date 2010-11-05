from SCRIBES.SignalConnectionManager import SignalManager

class Extractor(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "start-indexing", self.__start_indexing_cb)
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__precompile_methods, priority=PRIORITY_LOW)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __extract_text(self):
		texts = []
		for editor in self.__editor.instances:
			self.__editor.refresh(False)
			texts.append(editor.text)
			self.__editor.refresh(False)
		text = " ".join(texts)
		self.__manager.emit("extracted-text", text)
		return False

	def __precompile_methods(self):
		methods = (self.__extract_text, )
		self.__editor.optimize(methods)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __start_indexing_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__extract_text, priority=9999)
		return False
