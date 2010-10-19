class Colorer(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("replaced-mark", self.__replaced_mark_cb)
		self.__sigid3 = manager.connect("search-string", self.__clear_cb)
		self.__sigid4 = manager.connect("hide-bar", self.__clear_cb)
		self.__sigid5 = manager.connect("reset", self.__clear_cb)
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=9999)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__tag = self.__create_tag()
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
		tag = TextTag("replace_tag")
		self.__editor.textbuffer.get_tag_table().add(tag)
		tag.set_property("background", "green")
		tag.set_property("foreground", "blue")
		return tag

	def __clear(self):
		bounds = self.__editor.textbuffer.get_bounds()
		self.__editor.textbuffer.remove_tag(self.__tag, *bounds)
		return 

	def __tag_mark(self, mark):
		start = self.__editor.textbuffer.get_iter_at_mark(mark[0])
		end = self.__editor.textbuffer.get_iter_at_mark(mark[1])
		self.__editor.textbuffer.apply_tag(self.__tag, start, end)
		self.__editor.move_view_to_cursor(False, start)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __replaced_mark_cb(self, manager, mark):
		self.__tag_mark(mark)
		return False

	def __clear_cb(self, *args):
		self.__clear()
		return False

	def __precompile_methods(self):
		methods = (self.__tag_mark,)
		self.__editor.optimize(methods)
		return False
