class Manager(object):

	def __init__(self, editor, uri):
		editor.response()
		from MainGUI.Manager import Manager
		Manager(editor, uri)
		from InformationWindow.Manager import Manager
		Manager(editor)
		editor.response()
