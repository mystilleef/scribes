class Manager(object):

	def __init__(self, manager, editor):
		editor.response()
		from GUI.Manager import Manager
		Manager(manager, editor)
		from XMLTemplateWriter import Writer
		Writer(manager, editor)
		from TemplateDataGenerator import Generator
		Generator(manager, editor)
		from TemplateFileCreator import Creator
		Creator(manager, editor)
		from TemplateFileNameCreator import Creator
		Creator(manager, editor)
		editor.response()
