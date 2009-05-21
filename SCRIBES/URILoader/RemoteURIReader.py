class Reader(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("read-uri", self.__read_uri_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __read(self, uri):
		if uri.startswith("file:///"): return False
		from gio import File
		File(uri).load_contents_async(self.__ready_cb)
		return False

	def __ready_cb(self, gfile, result):
		from gio import Error
		try:
			data = gfile.load_contents_finish(result)
			self.__manager.emit("process-encoding", gfile.get_uri(), data[0])
		except Error:
			print dir(result)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __read_uri_cb(self, manager, uri):
		from gobject import idle_add
		idle_add(self.__read, uri)
		return False
