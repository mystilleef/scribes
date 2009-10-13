class Detector(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("entry-change-text", self.__changed_cb)
		manager.emit("match-case-flag", False)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__case = False
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __emit(self, text):
		islower = text.islower()
		if self.__case == islower: return False
		self.__case = islower
		self.__manager.emit("match-case-flag", not islower)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __changed_cb(self, manager, text):
		self.__emit(text)
		return False
