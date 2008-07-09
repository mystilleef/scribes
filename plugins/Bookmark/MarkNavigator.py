class Navigator(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("scroll-to-line", self.__scroll_to_line_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __scroll_to_line(self, line):
		iterator = self.__editor.textbuffer.get_iter_at_line(line)
		self.__editor.textview.scroll_to_iter(iterator, 0.001, use_align=True, xalign=1.0)
		return False
	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __scroll_to_line_cb(self, manager, line):
		self.__scroll_to_line(line)
		return False
