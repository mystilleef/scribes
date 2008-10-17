class Marker(object):
	
	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("found-matches", self.__found_matches_cb)
		
	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return 
	
	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return 
	
	def __mark_matches(self, matches):
		if not matches: return
		mr = self.__editor.create_right_mark
		ml = self.__editor.create_left_mark
		iao = self.__editor.textbuffer.get_iter_at_offset
		def iaos(start, end): return iao(start), iao(end)
		def mark_from_offsets(start, end): 
			bounds = iaos(start, end)
			return ml(bounds[0]), mr(bounds[1])
		marks = [mark_from_offsets(offset[0], offset[1]) for offset in matches]
		self.__manager.emit("marked-matches", marks)
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __found_matches_cb(self, manager, matches):
		self.__mark_matches(matches)
		return False
