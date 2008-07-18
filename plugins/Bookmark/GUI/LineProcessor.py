class Processor(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("marked-lines", self.__lines_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
#		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
#		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		del self
		self = None
		return

	def __text_from_line(self, line):
		start = self.__editor.textbuffer.get_iter_at_line(line)
		end = self.__editor.forward_to_line_end(start.copy())
		return self.__editor.textbuffer.get_text(start, end).strip(" \t\r\n")


	def __send_line_and_text(self, lines):
		data = [(line + 1, self.__text_from_line(line)) for line in lines]
		self.__manager.emit("populate-model", data)
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __lines_cb(self, manager, lines):
		self.__send_line_and_text(lines)
		return False
