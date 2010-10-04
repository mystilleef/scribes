class Colorer(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("marked-matches", self.__marked_matches_cb)
		self.__sigid3 = manager.connect("search-string", self.__clear_cb)
		self.__sigid4 = manager.connect("hide-bar", self.__clear_cb)
		self.__sigid5 = manager.connect("reset", self.__clear_cb)
		editor.response()

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
		tag = TextTag("find_tag")
		self.__editor.textbuffer.get_tag_table().add(tag)
		tag.set_property("background", "yellow")
		tag.set_property("foreground", "blue")
		return tag

	def __clear(self):
		if self.__colored is False: return
		bounds = self.__editor.textbuffer.get_bounds()
		self.__editor.textbuffer.remove_tag(self.__tag, *bounds)
		self.__colored = False
		return 

	def __tag_marks(self, marks):
		self.__clear()
		apply_tag = self.__editor.textbuffer.apply_tag
		giam = self.__editor.textbuffer.get_iter_at_mark
		iam = lambda start, end: (giam(start), giam(end))
		tag = lambda start, end: apply_tag(self.__tag, *(iam(start, end)))
		[tag(*mark) for mark in marks]
		self.__colored = True
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __marked_matches_cb(self, manager, marks):
		self.__tag_marks(marks)
		self.__manager.emit("search-complete")
		return False

	def __clear_cb(self, *args):
		self.__clear()
		return False
