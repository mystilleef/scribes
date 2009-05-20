from gettext import gettext as _
pair_chars = ("(", "[", "{", "<")

class Selector(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("select", self.__select_cb)
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=9999)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__match = editor.find_matching_bracket
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return False

	def __select(self):
		cursor = self.__editor.cursor
		tempiter = cursor.copy()
		while True:
			self.__editor.response()
			if tempiter.is_start(): break
			tempiter.backward_char()
			if not (tempiter.get_char() in pair_chars): continue
			tempiter.forward_char()
			iterator = self.__match(tempiter.copy())
			if not iterator: break
			if iterator.get_offset() < cursor.get_offset(): break
			self.__buffer.select_range(tempiter, iterator)
			self.__editor.update_message(_("Selected characters inside bracket"), "pass")
			return
		self.__editor.update_message(_("No brackets found for selection"), "fail")
		return False

	def __precompile_methods(self):
		methods = (self.__select_cb, self.__select, self.__match,)
		self.__editor.optimize(methods)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __select_cb(self, *args):
		self.__select()
		return False
