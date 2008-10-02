from gobject import GObject, SIGNAL_RUN_LAST, TYPE_NONE

class Manager(GObject):

	__gsignals__ = {
	"delete-line": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	"join-line": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	"duplicate-line": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	"delete-cursor-to-end": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	"delete-cursor-to-start": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	"free-line-below": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	"free-line-above": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	"destroy": (SIGNAL_RUN_LAST, TYPE_NONE, ()),
	}
	
	def __init__(self, editor):
		GObject.__init__(self)
		from LineOperator import Operator
		Operator(self, editor)
	
	def destroy(self):
		self.emit("destroy")
		del self
		self = None
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
