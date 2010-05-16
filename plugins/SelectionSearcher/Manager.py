from Signals import Signal

class Manager(Signal):

	def __init__(self, editor):
		Signal.__init__(self)
		from MatchIndexer import Indexer
		Indexer(self, editor)
		from MatchSelector import Selector
		Selector(self, editor)
		from MatchNavigator import Navigator
		Navigator(self, editor)
		from Reseter import Reseter
		Reseter(self, editor)
		from MatchColorer import Colorer
		Colorer(self, editor)
		from Marker import Marker
		Marker(self, editor)
		from Searcher import Searcher
		Searcher(self, editor)
		from RegexCreator import Creator
		Creator(self, editor)
		from PatternCreator import Creator
		Creator(self, editor)
		from SelectionDetector import Detector
		Detector(self, editor)

	def destroy(self):
		self.emit("destroy")
		del self
		return False

	def activate(self, action):
		self.emit(action)
		return False
