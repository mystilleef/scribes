from SCRIBES.SignalConnectionManager import SignalManager
NEWLINE = "\n"

class Processor(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "extracted-text", self.__extract_cb)
		self.connect(manager, "iprocessed-text", self.__processed_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__text = None
		return

	def __destroy(self):
		self.disconnect()
		del self
		return

	def __send_indent(self, text):
		plines = text.split(NEWLINE)
		olines = self.__text.split(NEWLINE)
		if not plines or not olines: return False
		if len(plines) > 1:
			bindentation = len(plines[0]) - len(olines[0])
			eindentation = len(plines[-1]) - len(olines[-1])
			self.__manager.emit("indentation", (bindentation, eindentation))
		else:
			bindentation = len(plines[0]) - len(olines[0])
			self.__manager.emit("indentation", (bindentation, ))
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __extract_cb(self, manager, text):
		self.__text = text
		return False

	def __processed_cb(self, manager, text):
		self.__send_indent(text)
		return False
