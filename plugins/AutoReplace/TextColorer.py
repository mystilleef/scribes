from gettext import gettext as _
message = _("Abbreviation highlighted")

class Colorer(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("match-found", self.__found_cb)
		self.__sigid3 = manager.connect("no-match-found", self.__nofound_cb)
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=9999)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__tag = self.__create_tag()
		self.__is_colored = False
		self.__message_flag = False
		return

	def __set_message(self):
		self.__editor.set_message(message)
		self.__message_flag = True
		return False

	def __unset_message(self):
		if self.__message_flag is False: return False
		self.__editor.unset_message(message)
		self.__message_flag = False
		return False

	def __destroy(self):
		self.__uncolor()
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return

	def __precompile_methods(self):
		methods = (self.__found_cb, self.__nofound_cb, self.__color,
			self.__uncolor)
		self.__editor.optimize(methods)
		return False

	def __create_tag(self):
		tag = self.__editor.textbuffer.create_tag()
		tag.set_property("background", "black")
		tag.set_property("foreground", "green")
		from pango import WEIGHT_HEAVY
		tag.set_property("weight", WEIGHT_HEAVY)
		return tag

	def __color(self, word):
		self.__uncolor()
		start = self.__editor.cursor.copy()
		for value in xrange(len(word)): 
			self.__editor.response()
			start.backward_char()
		self.__editor.textbuffer.apply_tag(self.__tag, start, self.__editor.cursor)
		self.__is_colored = True
		return False

	def __uncolor(self):
		if self.__is_colored is False: return False
		begin, end = self.__editor.textbuffer.get_bounds()
		self.__editor.textbuffer.remove_tag(self.__tag, begin, end)
		self.__is_colored = False
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __found_cb(self, manager, word):
		self.__color(word)
		self.__set_message()
		return False

	def __nofound_cb(self, *args):
		self.__uncolor()
		self.__unset_message()
		return False
