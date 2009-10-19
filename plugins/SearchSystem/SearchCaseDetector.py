class Detector(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("entry-change-text", self.__changed_cb)
		manager.emit("match-case-flag", False)
		from gobject import idle_add
		idle_add(self.__optimize, priority=9999)

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
		match_case = text.islower()
		if self.__case == match_case: return False
		self.__case = match_case
		self.__manager.emit("match-case-flag", not match_case)
		return False

	def __optimize(self):
		self.__editor.optimize((self.__emit,))
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __changed_cb(self, manager, text):
		self.__emit(text)
		return False
