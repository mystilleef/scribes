from Signals import Signal

class Manager(Signal):

	def __init__(self, editor):
		Signal.__init__(self)
		from BracketRegionMarker import Marker
		Marker(self, editor)
		from FreezeManager import Manager
		Manager(self, editor)
		from TextInserter import Inserter
		Inserter(self, editor)
		from BracketIndenter import Indenter
		Indenter(self, editor)
		from EmptyBracketMonitor import Monitor
		Monitor(self, editor)

	def destroy(self):
		self.emit("destroy")
		del self
		return False
