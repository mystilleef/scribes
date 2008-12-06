class Selector(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect_after("inserted-text", self.__insert_cb)
		self.__sigid3 = manager.connect("offsets", self.__offsets_cb)
		self.__sigid4 = manager.connect("indentation", self.__indentation_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__offsets = None
		self.__indentation = None
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		del self
		self = None
		return 

	def __select(self):
		get_iter = self.__editor.textbuffer.get_iter_at_line_offset
		if len(self.__offsets) == 1:
			indentation = self.__indentation[0]
			offset = self.__offsets[0][1]
			line = self.__offsets[0][0]
			noffset = offset + (indentation)
			iterator = get_iter(line, noffset)
			self.__editor.textbuffer.place_cursor(iterator)
		else:
			bindent, eindent = self.__indentation if len(self.__indentation) > 1 else (self.__indentation[0], self.__indentation[0])
			boffset = self.__offsets[0][1] + (bindent)
			eoffset = self.__offsets[1][1] + (eindent)
			start = get_iter(self.__offsets[0][0], boffset)
			end = get_iter(self.__offsets[1][0], eoffset)
			self.__buffer.select_range(start, end)
		self.__indentation = None
		self.__offsets = None
		self.__manager.emit("complete")
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __insert_cb(self, *args):
		from gobject import timeout_add, idle_add
		timeout_add(200, self.__select, priority=9999)
		return False

	def __offsets_cb(self, manager, offsets):
		self.__offsets = offsets
		return False

	def __indentation_cb(self, manager, indentation):
		self.__indentation = indentation
		return False
