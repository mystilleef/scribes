class Selector(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("current-match", self.__current_match_cb)
		self.__sigid3 = manager.connect("search-string", self.__clear_cb)
		self.__sigid4 = manager.connect("found-matches", self.__clear_cb)
		self.__sigid5 = manager.connect("hide-bar", self.__select_cb)
		self.__sigid6 = manager.connect("replaced-mark", self.__current_match_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__offsets = None
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		self.__editor.disconnect_signal(self.__sigid6, self.__manager)
		del self
		self = None
		return 

	def __clear(self):
		self.__offsets = None
		return 

	def __update_offsets(self, match):
		get_iter = self.__editor.textbuffer.get_iter_at_mark
		self.__offsets = get_iter(match[0]).get_offset(), get_iter(match[1]).get_offset()
		return

	def __select(self):
		if not self.__offsets: return
		get_iter = self.__editor.textbuffer.get_iter_at_offset
		get_range = lambda start, end: (get_iter(start), get_iter(end))
		self.__editor.textbuffer.select_range(*(get_range(*(self.__offsets))))
		self.__clear()
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __select_cb(self, *args):
		self.__select()
		return False

	def __clear_cb(self, *args):
		self.__clear()
		return False

	def __current_match_cb(self, manager, match):
		self.__update_offsets(match)
		return False
