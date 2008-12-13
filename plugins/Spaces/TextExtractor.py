class Extractor(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("tabs-to-spaces", self.__process_cb)
		self.__sigid3 = manager.connect("spaces-to-tabs", self.__process_cb)
		self.__sigid4 = manager.connect("remove-trailing-spaces", self.__process_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		del self
		self = None
		return

	def __send_extracted_text(self):
		self.__manager.emit("extracted-text", self.__editor.text)
		return False

	def __process_cb(self, *args):
		self.__send_extracted_text()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
