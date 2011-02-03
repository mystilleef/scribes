from SCRIBES.SignalConnectionManager import SignalManager

class Searcher(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "boundary-marks", self.__boundary_cb)
		self.connect(manager, "inserted-template", self.__template_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__boundary = ()
		self.__template = ""
		return

	def __search(self, template):
		offset = self.__buffer.get_iter_at_mark(self.__boundary[0]).get_offset()
		placeholder_pattern = "\$+\d"
		from re import finditer, M, U
		flags =  M|U
		matches = finditer(placeholder_pattern, template, flags)
		offsets = [(offset+match.start(), offset+match.end()) for match in matches]
		self.__manager.emit("placeholder-offsets", offsets)
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False

	def __boundary_cb(self, manager, boundary):
		self.__boundary = boundary
		return False

	def __template_cb(self, manager, template):
		self.__search(template)
		return False
