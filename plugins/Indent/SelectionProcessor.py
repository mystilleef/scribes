class Processor(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("extracted-text", self.__extract_cb)
		self.__sigid3= manager.connect("iprocessed-text", self.__processed_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__text = None
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return 

	def __send_indent(self, text):
		plines = text.splitlines()
		olines = self.__text.splitlines()
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
