class Manager(object):

	def __init__(self, editor):
		editor.response()
		from Feedback.Manager import Manager
		Manager(editor)
		from CursorPosition.Manager import Manager
		Manager(editor)
		from EditingModeDisplayer import Displayer
		Displayer(editor)
		editor.response()
