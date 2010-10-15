class Manager(object):

	def __init__(self, manager, editor):
		editor.refresh()
		from AddButton import Button
		Button(manager, editor)
		from TreeView.Manager import Manager
		Manager(manager, editor)
		from Label import Label
		Label(manager, editor)
		from RemoveButton import Button
		Button(manager, editor)
		from Window import Window
		Window(manager, editor)
		editor.refresh()
