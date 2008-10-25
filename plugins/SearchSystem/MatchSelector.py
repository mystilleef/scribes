class Selector(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("current-match", self.__current_match_cb)
		self.__sigid3 = manager.connect("search-string", self.__clear_cb)
		self.__sigid4 = manager.connect("hide-bar", self.__clear_cb)
		self.__sigid5 = manager.connect("reset", self.__clear_cb)
		self.__sigid6 = manager.connect("select-match", self.__select_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__match = None
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
		self.__match = None
		return 

	def __select(self):
		if not self.__match: return
		start = self.__editor.textbuffer.get_iter_at_mark(self.__match[0])
		end = self.__editor.textbuffer.get_iter_at_mark(self.__match[1])
		self.__editor.textbuffer.select_range(start, end)
		print "Got here"
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
		self.__match = match
		return False
