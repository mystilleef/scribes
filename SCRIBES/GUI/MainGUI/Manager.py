class Manager(object):

	def __init__(self, editor, uri):
		from Window.Manager import Manager
		Manager(editor, uri)
		from View.Manager import Manager
		Manager(editor, uri)
