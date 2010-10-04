from SCRIBES.SignalConnectionManager import SignalManager

class Selector(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "inserted-text", self.__insert_cb, True)
		self.connect(manager, "offsets", self.__offsets_cb)
		self.connect(manager, "indentation", self.__indentation_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__offsets = None
		self.__indentation = None
		return

	def __destroy(self):
		self.disconnect()
		del self
		return 

	def __select(self):
		if self.__offsets is None or self.__indentation is None: return False
		self.__editor.textview.window.freeze_updates()
		get_iter = self.__editor.textbuffer.get_iter_at_line_offset
		if len(self.__offsets) == 1:
			indentation = self.__indentation[0]
			offset = self.__offsets[0][1]
			line = self.__offsets[0][0]
			noffset = offset + (indentation)
			if noffset < 0: noffset = 0
			iterator = get_iter(line, noffset)
			self.__buffer.place_cursor(iterator)
		else:
			bindent, eindent = self.__indentation if len(self.__indentation) > 1 else (self.__indentation[0], self.__indentation[0])
			boffset = self.__offsets[0][1] + (bindent)
			eoffset = self.__offsets[1][1] + (eindent)
			if boffset < 0: boffset = 0
			if eoffset < 0: eoffset = 0
			start = get_iter(self.__offsets[0][0], boffset)
			end = get_iter(self.__offsets[1][0], eoffset)
			self.__buffer.place_cursor(start)
			self.__buffer.select_range(start, end)
		self.__indentation = None
		self.__offsets = None
		self.__editor.textview.window.thaw_updates()
		self.__manager.emit("complete")
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __insert_cb(self, *args):
		try:
			from gobject import timeout_add, source_remove, idle_add
			source_remove(self.__timer)
		except AttributeError:
			pass
		finally:
			self.__timer = idle_add(self.__select)
		return False

	def __offsets_cb(self, manager, offsets):
		self.__offsets = offsets
		return False

	def __indentation_cb(self, manager, indentation):
		self.__indentation = indentation
		return False
