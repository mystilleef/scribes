from gettext import gettext as _

class Position(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__label.set_label("")
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("cursor-moved", self.__moved_cb)
		self.__update()
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__busy = False
		self.__label = editor.gui.get_widget("StatusCursorPosition")
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return

	def __update_label(self, line, column):
		self.__label.set_label(_("<b>Ln</b> %s <b>Col</b> %s") % (str(line), str(column)))
		self.__busy = False
		return False

	def __update(self):
		self.__busy = True
		cursor = self.__editor.cursor
		start = self.__editor.backward_to_line_begin(cursor.copy())
		text = self.__editor.textbuffer.get_text(start, cursor)
		offset = cursor.get_line_offset()
		width = self.__editor.textview.get_tab_width()
		line = cursor.get_line()
		if "\t" in text:
			for characters in text:
				if (characters == "\t"): offset += (width - 1)
		from gobject import idle_add
		idle_add(self.__update_label, line+1, offset+1, priority=9999)
		return False

	def __update_position(self):
		if self.__busy: return False
		from gobject import idle_add
		idle_add(self.__update, priority=9999)
		return False

	def __move(self):
		try:
			from gobject import source_remove, timeout_add
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = timeout_add(500, self.__update_position, priority=9999)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __moved_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__move, priority=9999)
		return False
