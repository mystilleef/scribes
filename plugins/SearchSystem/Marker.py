class Marker(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("mapped-matches", self.__found_matches_cb)
		self.__sigid3 = manager.connect("hide-bar", self.__clear_cb)
		self.__sigid4 = manager.connect("search-string", self.__clear_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__marks = None
		return 

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		del self
		self = None
		return 

	def __clear(self):
		if not self.__marks: return
		del_ = self.__editor.delete_mark
		remove_marks = lambda start, end: (del_(start), del_(end))
		(remove_marks(*mark) for mark in self.__marks)
		self.__marks[:]
		self.__marks = None
		return 

	def __mark_matches(self, matches):
		if not matches: return
		self.__clear()
		mr = self.__editor.create_right_mark
		ml = self.__editor.create_left_mark
		iao = self.__editor.textbuffer.get_iter_at_offset
		iaos = lambda start, end: (iao(start), iao(end))
		mark_ = lambda start, end: (ml(start), mr(end))
		mark_from_offsets = lambda start, end: mark_(*(iaos(start, end)))
		marks = [mark_from_offsets(*offset) for offset in matches]
		self.__marks = marks
		self.__manager.emit("marked-matches", marks)
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __clear_cb(self, *args):
		self.__clear()
		return False

	def __found_matches_cb(self, manager, matches):
		self.__mark_matches(matches)
		return False
