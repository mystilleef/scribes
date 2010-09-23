from Signals import Signal

class Manager(Signal):

	def __init__(self, editor):
		Signal.__init__(self)
		from Feedback import Feedback
		Feedback(self, editor)
		from Selector import Selector
		Selector(self, editor)
		from QuoteCharacterMatcher import Matcher
		Matcher(self, editor)
		from RangeChecker import Checker
		Checker(self, editor)
		from PairCharacterMatcher import Matcher
		Matcher(self, editor)
		from OpenCharacterSearcher import Searcher
		Searcher(self, editor)
		from SelectionChecker import Checker
		Checker(self, editor)

	def destroy(self):
		self.emit("destroy")
		del self
		return False

	def activate(self):
		self.emit("activate")
		return False
