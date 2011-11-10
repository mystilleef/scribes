class Processor(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("process-encoding", self.__process_cb)
		self.__sigid3 = manager.connect("init-loading", self.__init_loading_cb)
		self.__sigid4 = manager.connect("insertion-error", self.__process_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		from collections import deque
		self.__encodings = deque()
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		del self
		return False

	def __send(self, uri, string):
		try:
			from gobject import idle_add, PRIORITY_LOW
			encoding = self.__encodings.popleft()
			idle_add(self.__manager.emit, "insert-text", uri, string, encoding, priority=PRIORITY_LOW)
		except IndexError:
			idle_add(self.__manager.emit, "encoding-error", uri, priority=PRIORITY_LOW)
		return False

	def __generate_encoding_list(self, encoding):
		from collections import deque
		encodings = deque(self.__editor.encoding_guess_list)
		encodings.appendleft(encoding)
		return encodings

	def __destroy_cb(self, *args):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__destroy, priority=PRIORITY_LOW)
		return False

	def __process_cb(self, manager, uri, string):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__send, uri, string, priority=PRIORITY_LOW)
		return False

	def __init_loading_cb(self, manager, uri, encoding):
		self.__encodings = self.__generate_encoding_list(encoding)
		return False
