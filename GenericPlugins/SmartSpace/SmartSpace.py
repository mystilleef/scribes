class SmartSpace(object):

	def __init__(self, editor, manager):
		self.__init_attributes(editor, manager)
		self.__sigid1 = self.__textview.connect('key-press-event', self.__key_press_event_cb)
		self.__sigid2 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid3 = manager.connect("activate", self.__activate_cb)
		from gobject import idle_add
		idle_add(self.__precompile_method, priority=9999)

	def __init_attributes(self, editor, manager):
		self.__editor = editor
		self.__manager = manager
		self.__textview = editor.textview
		self.__buffer = editor.textbuffer
		self.__activate = False
		self.__blocked = False
		return

	def __block_event_after_signal(self):
		if self.__blocked: return
		self.__textview.handler_block(self.__sigid1)
		self.__blocked = True
		return

	def __unblock_event_after_signal(self):
		if self.__blocked is False: return
		self.__textview.handler_unblock(self.__sigid1)
		self.__blocked = False
		return

	def __check_event_signal(self):
		if self.__activate:
			self.__unblock_event_after_signal()
		else:
			self.__block_event_after_signal()
		return

	def __precompile_method(self):
		methods = (self.__key_press_event_cb,)
		self.__editor.optimize(methods)
		return False

	def __key_press_event_cb(self, textview, event):
		if self.__activate is False: return False
		from gtk.keysyms import BackSpace
		if event.keyval != BackSpace: return False
		if self.__buffer.get_has_selection(): return False
		iterator = self.__editor.cursor
		if iterator.starts_line(): return False
		start = iterator.copy()
		while True:
			start.backward_char()
			if start.get_char() != " ": break
			start.forward_char()
			start = self.__get_start_position(start, iterator.get_line_offset())
			break
		self.__buffer.begin_user_action()
		self.__buffer.delete(start, iterator)
		self.__buffer.end_user_action()
		return True

	def __get_start_position(self, start, cursor_offset):
		indentation = self.__textview.get_tab_width()
		moves = cursor_offset % indentation
		if moves == 0 : moves = indentation
		for value in xrange(moves):
			if start.starts_line(): return start
			start.backward_char()
			if start.get_char() == " ": continue
			start.forward_char()
			break
		return start

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __activate_cb(self, manager, use_spaces):
		self.__activate = use_spaces
		self.__check_event_signal()
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__textview)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return
