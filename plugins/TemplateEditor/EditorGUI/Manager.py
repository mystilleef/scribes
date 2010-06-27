class Manager(object):

	def __init__(self, manager, editor):
		editor.response()
		from Window import Window
		Window(manager, editor)
		from CancelButton import Button
		Button(manager, editor)
		from SaveButton import Button
		Button(manager, editor)
		from SourceView import SourceView
		SourceView(manager, editor)
		from DescriptionEntry import Entry
		Entry(manager, editor)
		from NameEntry import Entry
		Entry(manager, editor)
		from TemplateDataGenerator import Generator
		Generator(manager, editor)
		from GUIDataInitializer import Initializer
		Initializer(manager, editor)
		from GUIDataExtractor import Extractor
		Extractor(manager, editor)
		from TriggerValidator import Validator
		Validator(manager, editor)
		from ValidatorTriggerListGenerator import Generator
		Generator(manager, editor)
		editor.response()