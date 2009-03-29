class Manager(object):

	def __init__(self, editor, uri):
		editor.response()
		from Window.Manager import Manager
		Manager(editor, uri)
		from View.Manager import Manager
		Manager(editor, uri)
		from Buffer.Manager import Manager
		Manager(editor)
		from Toolbar.Manager import Manager
		Manager(editor)
		from StatusBar.Manager import Manager
		Manager(editor)
		editor.response()
