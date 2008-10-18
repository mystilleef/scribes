class Mapper(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("found-matches", self.__matches_cb)
		self.__sigid3 = manager.connect("search-boundary", self.__boundary_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__offset = 0
		return 

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return 

	def __map_matches(self, matches):
		if not matches: return False
		factor = self.__offset
		remap = lambda start, end: (factor+start, factor+end)
		matches = [remap(*offset) for offset in matches]
		self.__manager.emit("mapped-matches", matches)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False
	
	def __matches_cb(self, manager, matches):
		self.__map_matches(matches)
		return False

	def __boundary_cb(self, manager, boundary):
		self.__offset = boundary[0].get_offset()
		return False
