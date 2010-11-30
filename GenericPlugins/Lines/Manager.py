from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE
from gobject import SIGNAL_NO_RECURSE, SIGNAL_ACTION
SCRIBES_SIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
	"delete-line": (SCRIBES_SIGNAL, TYPE_NONE, ()),
	"join-line": (SCRIBES_SIGNAL, TYPE_NONE, ()),
	"duplicate-line": (SCRIBES_SIGNAL, TYPE_NONE, ()),
	"delete-cursor-to-end": (SCRIBES_SIGNAL, TYPE_NONE, ()),
	"delete-cursor-to-start": (SCRIBES_SIGNAL, TYPE_NONE, ()),
	"free-line-below": (SCRIBES_SIGNAL, TYPE_NONE, ()),
	"free-line-above": (SCRIBES_SIGNAL, TYPE_NONE, ()),
	"backward-word-deletion": (SCRIBES_SIGNAL, TYPE_NONE, ()),
	"destroy": (SCRIBES_SIGNAL, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		GObject.__init__(self)
		from LineOperator import Operator
		Operator(self, editor)

	def destroy(self):
		self.emit("destroy")
		del self
		return

	def delete_line(self):
		self.emit("delete-line")
		return

	def join_line(self):
		self.emit("join-line")
		return

	def duplicate_line(self):
		self.emit("duplicate-line")
		return

	def delete_cursor_to_end(self):
		self.emit("delete-cursor-to-end")
		return

	def delete_cursor_to_start(self):
		self.emit("delete-cursor-to-start")
		return

	def free_line_above(self):
		self.emit ("free-line-above")
		return

	def free_line_below(self):
		self.emit("free-line-below")
		return

	def backward_word_deletion(self):
		self.emit("backward-word-deletion")
		return False
