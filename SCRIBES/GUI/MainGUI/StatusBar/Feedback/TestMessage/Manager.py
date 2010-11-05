from Signals import Signal

class Manager(Signal):

	def __init__(self, editor):
		Signal.__init__(self)
		from MessageBarDisplayer import Displayer
		Displayer(self, editor)
		from MessageBarUpdater import Updater
		Updater(self, editor)
		from MessageFormatter import Formatter
		Formatter(self, editor)
		from FallbackMessageHandler import Handler
		Handler(self, editor)
		from StackMessageHandler import Handler
		Handler(self, editor)
		from TimedMessageHandler import Handler
		Handler(self, editor)

