class Extractor(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("indent", self.__process_cb)
		self.__sigid3 = manager.connect("unindent", self.__process_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return
	
	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		del self
		self = None
		return

	def __send_offsets(self):
		if self.__editor.selection_range == 0:
			iterator = self.__editor.cursor
			line = iterator.get_line()
			offset = iterator.get_line_offset()
			data = line, offset
			offsets = (data,)
		else:
			start, end = self.__editor.selection_bounds
			line = start.get_line()
			offset = start.get_line_offset()
			data1 = line, offset
			line = end.get_line()
			offset = end.get_line_offset()
			data2 = line, offset
			offsets = (data1, data2)
		self.__manager.emit("offsets", offsets)
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __process_cb(self, *args):
		self.__send_offsets()
		return False
