class Manager(object):

	def __init__(self, editor, uri):
		from StateTracker import Tracker
		Tracker(editor)
		from Grabber import Grabber
		Grabber(editor)
		from Window import Window
		Window(editor)
		from Positioner import Positioner
		Positioner(editor, uri)
		from PositionUpdater import Updater
		Updater(editor, uri)
