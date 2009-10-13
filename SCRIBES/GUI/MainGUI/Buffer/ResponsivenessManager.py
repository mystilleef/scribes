class Manager(object):

	def __init__(self, editor):
		editor.response()
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = self.__buffer.connect("changed", self.__response_cb)
		self.__sigid3 = self.__buffer.connect_after("changed", self.__response_cb)
		self.__sigid4 = self.__buffer.connect("highlight-updated", self.__response_cb)
		self.__sigid5 = self.__buffer.connect_after("highlight-updated", self.__response_cb)
		self.__sigid6 = self.__buffer.connect("source-mark-updated", self.__response_cb)
		self.__sigid7 = self.__buffer.connect_after("source-mark-updated", self.__response_cb)
		from gobject import idle_add
		idle_add(self.__optimize, priority=9999)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__buffer = editor.textbuffer
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__buffer)
		self.__editor.disconnect_signal(self.__sigid3, self.__buffer)
		self.__editor.disconnect_signal(self.__sigid4, self.__buffer)
		self.__editor.disconnect_signal(self.__sigid5, self.__buffer)
		self.__editor.disconnect_signal(self.__sigid6, self.__buffer)
		self.__editor.disconnect_signal(self.__sigid7, self.__buffer)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __refresh(self):
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = idle_add(self.__editor.refresh, False)
		return False

	def __optimize(self):
		self.__editor.optimize((self.__response_cb,))
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __response_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__refresh)
		return False
