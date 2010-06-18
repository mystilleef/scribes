from Signals import Signal

class Manager(Signal):

	def __init__(self, editor):
		editor.response()
		Signal.__init__(self)
		from FeedbackManager import Manager
		Manager(self, editor)
		from BusyManager import Manager
		Manager(self, editor)
		from CursorPositioner import Positioner
		Positioner(self, editor)
		from SelectionManager import Manager
		Manager(self, editor)
		from TextInserter import Inserter
		Inserter(self, editor)
		from MultiLineCommentProcessor import Processor
		Processor(self, editor)
		from SingleLineCommentProcessor import Processor
		Processor(self, editor)
		from BoundaryMarker import Marker
		Marker(self, editor)
		from MarkProcessor import Processor
		Processor(self, editor)
		editor.response()

	def destroy(self):
		self.emit("destroy")
		del self
		return False

	def activate(self):
		self.emit("activate")
		return False
