class Manager(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("show-error", self.__busy_cb)
		self.__sigid3 = editor.connect("show-info", self.__busy_cb)
		self.__sigid4 = manager.connect("hide", self.__hide_cb)
		editor.register_object(self)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		self.__busy = False
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __enable_busy_mode(self):
		if self.__busy: return False
		self.__editor.busy()
		self.__busy = True
		return False

	def __disable_busy_mode(self):
		if not self.__busy: return False
		self.__editor.busy(False)
		self.__busy = False
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __busy_cb(self, editor, title, message, window, busy):
		if busy: self.__enable_busy_mode()
		return False

	def __hide_cb(self, *args):
		self.__disable_busy_mode()
		return False
