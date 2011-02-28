from Signals import Signal

class Manager(Signal):

	def __init__(self, editor):
		Signal.__init__(self)
		from Feedback import Feedback
		Feedback(self, editor)
		from BufferFreezer import Freezer
		Freezer(self, editor)
		from RegionSelector import Selector
		Selector(self, editor)
		from CursorPlacer import Placer
		Placer(self, editor)
		from TextInserter import Inserter
		Inserter(self, editor)
		from Commenter import Commenter
		Commenter(self, editor)
		from CommentDecider import Decider
		Decider(self, editor)
		from RegionMarker import Marker
		Marker(self, editor)

	def destroy(self):
		self.emit("destroy")
		del self
		return False

	def activate(self):
		from gobject import idle_add
		idle_add(self.emit, "activate")
		return False
