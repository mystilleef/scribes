class Searcher(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("search-boundary", self.__boundary_cb)
		self.__sigid3 = manager.connect("new-regex", self.__regex_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__text = None
		return  

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return 

	def __find_matches(self, regex_object):
		iterator = regex_object.finditer(self.__text)
		matches = [(match.start(), match.end()) for match in iterator]
		self.__manager.emit("found-matches", matches)
		return 

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __boundary_cb(self, manager, boundary):
		self.__text = self.__editor.textbuffer.get_text(*(boundary))
		return False

	def __regex_cb(self, manager, regex_object):
		self.__find_matches(regex_object)
		return False
