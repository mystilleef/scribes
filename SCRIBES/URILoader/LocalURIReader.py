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
		if not uri.startswith("file:///"): return False
		# We do asynchronous reads for local files
		from gnomevfs import OPEN_READ, URI
		from gnomevfs.async import open as open_
		try:
			open_(URI(uri), self.__open_cb, OPEN_READ, 10, uri)
		except:
			self.__manager.emit("error", uri, 5)
		return False

	def __open_cb(self, handle, result, uri):
		try:
			from gnomevfs import URI, get_local_path_from_uri
			local_path = get_local_path_from_uri(uri)
			from os.path import getsize
			size = getsize(local_path)
			if not (size): size = 4096
			handle.read(size, self.__read_cb, uri)
		except:
			self.__manager.emit("error", uri, 6)
		return False

	def __read_cb(self, handle, buffer_, result, bytes, uri):
		try:
			handle.close(self.__close_cb)
			self.__manager.emit("process-encoding", uri, buffer_)
		except:
			self.__manager.emit("error", uri, 7)
		return False

	def __close_cb(self, *args):
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __read_uri_cb(self, manager, uri):
		from gobject import idle_add
		idle_add(self.__read, uri)
		return False
