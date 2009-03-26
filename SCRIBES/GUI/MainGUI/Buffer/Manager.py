class Manager(object):

	def __init__(self, editor):
		editor.response()
		from Buffer import Buffer
		Buffer(editor)
		from ModificationStateNotifier import Notifier
		Notifier(editor)
		from ModificationStateReseter import Reseter
		Reseter(editor)
		from UndoRedo import UndoRedo
		UndoRedo(editor)
		from StyleSchemeUpdater import Updater
		Updater(editor)
		from LanguageSetter import Setter
		Setter(editor)
		from CursorPositionNotifier import Notifier
		Notifier(editor)
		from CursorPlacer import Placer
		Placer(editor)
		from CursorPositionUpdater import Updater
		Updater(editor)
		from ResponsivenessManager import Manager
		Manager(editor)
		editor.response()
