class Processor(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("character", self.__character_cb)
		self.__sigid3 = manager.connect("extracted-text", self.__text_cb)
		self.__sigid4 = manager.connect("complete", self.__complete_cb)
	
	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__character = None
		return
	
	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		del self
		self = None
		return 

	def __indent(self, text):
		lines = text.splitlines()
		indented_lines = [(self.__character + line) for line in lines]
		text = "\n".join(indented_lines)
		self.__manager.emit("iprocessed-text", text)
		self.__manager.emit("processed-text", text)
		return False

	def __clear(self):
		self.__character = None
		return 

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __character_cb(self, manager, character):
		self.__character = character
		return False

	def __text_cb(self, manager, text):
		self.__indent(text)
		return False

	def __complete_cb(self, *args):
		self.__clear()
		return False
