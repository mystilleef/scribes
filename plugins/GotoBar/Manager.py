from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE, TYPE_INT

class Manager(GObject):

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"show-bar": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"hide-bar": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"line-number": (SIGNAL_RUN_LAST, TYPE_NONE, (TYPE_INT,)),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		self.__init_attributes(editor)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__manager = None
		return 

	def destroy(self):
		self.emit("destroy")
		del self
		self = None
		return 

	def show(self):
		try:
			self.__manager.show()
		except AttributeError:
			from GUI.Manager import Manager
			self.__manager = Manager(self, self.__editor)
			self.__manager.show()
		return
