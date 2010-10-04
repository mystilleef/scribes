from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE

class Manager(GObject):

	__gsignals__ = {
		"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"escape": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
		"unescape": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		editor.response()
		GObject.__init__(self)
		from Escaper import Escaper
		Escaper(self, editor)
		editor.response()

	def escape(self):
		self.emit("escape")
		return

	def unescape(self):
		self.emit("unescape")
		return

	def destroy(self):
		self.emit("destroy")
		del self
		self = None
		return
