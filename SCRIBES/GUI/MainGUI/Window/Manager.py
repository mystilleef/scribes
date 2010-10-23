class Manager(object):

	def __init__(self, editor, uri):
		from Window import Window
		Window(editor)
		from StateTracker import Tracker
		Tracker(editor)
		from Grabber import Grabber
		Grabber(editor)
		from FullscreenManager import Manager
		Manager(editor)
		from Positioner import Positioner
		Positioner(editor, uri)
		from PositionUpdater import Updater
		Updater(editor, uri)
		from TitleUpdater import Updater
		Updater(editor, uri)
