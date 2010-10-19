class Manager(object):

	def __init__(self, manager, editor):
		from Window import Window
		Window(manager, editor)
		from Treeview.Manager import Manager
		Manager(manager, editor)
