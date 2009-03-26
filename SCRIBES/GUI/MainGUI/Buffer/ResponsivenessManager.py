class Manager(object):

	def __init__(self, editor):
		editor.response()
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = self.__buffer.connect("changed", self.__response_cb)
		self.__sigid3 = self.__buffer.connect_after("changed", self.__response_cb)
		editor.register_object(self)
		from gobject import idle_add
		idle_add(self.__optimize, priority=99999)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__buffer = editor.textbuffer
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__buffer)
		self.__editor.disconnect_signal(self.__sigid3, self.__buffer)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __response(self):
		self.__remove_timers()
		from gobject import timeout_add
		self.__timer = timeout_add(10, self.__response_timeout_cb, priority=9999)
		return False

	def __optimize(self):
		methods = (self.__response_cb, self.__response, 
			self.__response_idle_cb, self.__response_timeout_cb)
		self.__editor.optimize(methods)
		return False

	def __remove_timers(self):
		try:
			from gobject import source_remove
			source_remove(self.__timer)
			source_remove(self.__timer1)
		except AttributeError:
			pass
		return False

	def __response_timeout_cb(self):
		from gobject import idle_add
		self.__timer1 = idle_add(self.__response_idle_cb, priority=9999)
		return False

	def __response_idle_cb(self):
		self.__editor.response()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __response_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__response, priority=9999)
		return False
