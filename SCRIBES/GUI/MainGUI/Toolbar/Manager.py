class Manager(object):

	def __init__(self, editor):
		from Toolbar import Toolbar
		Toolbar(editor)
		from ToolbarVisibility.Manager import Manager
		Manager(editor)
