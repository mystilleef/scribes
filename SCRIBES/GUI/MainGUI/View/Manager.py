class Manager(object):

	def __init__(self, editor, uri):
		editor.response()
		from View import View
		View(editor)
		from Refresher import Refresher
		Refresher(editor)
		from SensitivityManager import Manager
		Manager(editor)
		from ResponsivenessManager import Manager
		Manager(editor)
		from ReadonlyManager import Manager
		Manager(editor)
		from DragAndDrop import DragAndDrop
		DragAndDrop(editor)
		from PopupMenuManager import Manager
		Manager(editor)
		from SpellChecker import Checker
		Checker(editor)
		from FullscreenManager import Manager
		Manager(editor)
		from DatabaseListeners.Manager import Manager
		Manager(editor)
		editor.response()
