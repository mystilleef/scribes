from Signals import Signal

class Manager(Signal):

	def __init__(self, editor):
		Signal.__init__(self)
		from FeedbackManager import Manager
		Manager(self, editor)
		from ModeQuiter import Quiter
		Quiter(self, editor)
		from EventHandler import Handler
		Handler(self, editor)
		from EditPointHandler import Handler
		Handler(self, editor)
		from MarkUpdater import Updater
		Updater(self, editor)
		from TextInsertionHandler import Handler
		Handler(self, editor)
		from TextDeletionHandler import Handler
		Handler(self, editor)
		from ColumnEditPointNavigator import Navigator
		Navigator(self, editor)

	def destroy(self):
		self.emit("destroy")
		del self
		return

	def activate(self):
		self.emit("activate")
		return False
