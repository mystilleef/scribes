class Manager(object):

	def __init__(self, manager):
		from TreeView.Manager import Manager
		Manager(manager)
		from Entry import Entry
		Entry(manager)
		from Label import Label
		Label(manager)
		from Window import Window
		Window(manager)
