class Manager(object):

	def __init__(self, manager, editor):
		from Window import Window
		Window(manager, editor)
		from TreeView import TreeView
		TreeView(manager, editor)
		from AddButton import Button
		Button(manager, editor)
