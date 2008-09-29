from gobject import SIGNAL_RUN_LAST, TYPE_NONE, GObject

class Manager(GObject):

	__gsignals__ = {
		"select-word": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"select-line": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"select-statement": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"select-paragraph": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		from Selector import Selector
		Selector(self, editor)

	def select_word(self):
		self.emit("select-word")
		return False

	def select_statement(self):
		self.emit("select-statement")
		return False
	
	def select_line(self):
		self.emit("select-line")
		return False
	
	def select_paragraph(self):
		self.emit("select-paragraph")
		return False
	
	def destroy(self):
		self.emit("destroy")
		del self
		self = None
		return
