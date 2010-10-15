class Manager(object):

	def __init__(self, manager, editor):
		from MainGUI.Manager import Manager
		Manager(manager, editor)
		from FileChooserGUI.Manager import Manager
		Manager(editor, manager)
