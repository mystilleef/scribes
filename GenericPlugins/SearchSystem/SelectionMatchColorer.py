class Colorer(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("current-match", self.__current_match_cb)
		self.__sigid3 = manager.connect("search-string", self.__clear_cb)
		self.__sigid4 = manager.connect("hide-bar", self.__clear_cb)
		self.__sigid5 = manager.connect("reset", self.__clear_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__tag = self.__create_tag()
		self.__colored = False
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		del self
		self = None
		return 

	def __create_tag(self):
		from gtk import TextTag
		tag = TextTag("match_selection_tag")
		self.__editor.textbuffer.get_tag_table().add(tag)
		tag.set_property("background", "blue")
		tag.set_property("foreground", "yellow")
		return tag

	def __clear(self):
		if self.__colored is False: return
		bounds = self.__editor.textbuffer.get_bounds()
		self.__editor.textbuffer.remove_tag(self.__tag, *bounds)
		self.__colored = False
		return 

	def __tag_mark(self, mark):
		self.__clear()
		apply_tag = self.__editor.textbuffer.apply_tag
		giam = self.__editor.textbuffer.get_iter_at_mark
		iter1 = giam(mark[0])
		iter2 = giam(mark[1])
		apply_tag(self.__tag, iter1, iter2)
		self.__editor.move_view_to_cursor(False, iter1)
		self.__colored = True
		self.__manager.emit("selected-mark", mark)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __current_match_cb(self, manager, mark):
		self.__tag_mark(mark)
		return False

	def __clear_cb(self, *args):
		self.__clear()
		return False
