class Manager(object):

	def __init__(self, manager, editor):
		from TreeView.Manager import Manager
		Manager(manager, editor)
		from Entry import Entry
		Entry(manager, editor)
		from Window import Window
		Window(manager, editor)
