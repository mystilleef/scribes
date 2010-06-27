class Manager(object):

	def __init__(self, manager, editor):
		editor.response()
		from GUI.Manager import Manager
		Manager(manager, editor)
		from PostImportSelector import Selector
		Selector(manager, editor)
		from TemplateDataValidator import Validator
		Validator(manager, editor)
		from ImportedTemplateDataProcessor import Processor
		Processor(manager, editor)
		from XMLTemplateImporter import Importer
		Importer(manager, editor)
		from XMLTemplateValidator import Validator
		Validator(manager, editor)
		editor.response()
