class Trigger(object):

	def __init__(self, editor):
		editor.response()
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("supported-encodings-window", self.__activate_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__manager = None
		return

	def __destroy(self):
		if self.__manager: self.__manager.destroy()
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __activate(self):
		try:
			self.__manager.activate()
		except AttributeError:
			from Manager import Manager
			self.__manager = Manager(self.__editor)
			self.__manager.activate()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __activate_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__activate, priority=9999)
		return False
