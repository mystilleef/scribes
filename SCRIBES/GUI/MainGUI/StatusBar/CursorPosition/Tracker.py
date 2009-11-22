class Tracker(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = manager.connect("calculate", self.__calculate_cb)
		self.__calculate()
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__busy = False
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __calculate(self):
		if self.__busy: return False
		self.__busy = True
		cursor = self.__editor.cursor
		start = self.__editor.backward_to_line_begin(cursor.copy())
		text = self.__editor.textbuffer.get_text(start, cursor)
		offset = cursor.get_line_offset()
		width = self.__editor.textview.get_tab_width()
		line = cursor.get_line()
		if "\t" in text:
			for characters in text:
				self.__editor.response()
				if (characters == "\t"): offset += (width - 1)
		self.__busy = False
		self.__manager.emit("update", (line+1, offset+1))
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __calculate_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__calculate, priority=9999)
		return False
