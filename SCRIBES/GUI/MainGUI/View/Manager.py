class Manager(object):

	def __init__(self, editor, uri):
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
		from SpellChecker import Checker
		Checker(editor)
		from DatabaseListeners.Manager import Manager
		Manager(editor)
