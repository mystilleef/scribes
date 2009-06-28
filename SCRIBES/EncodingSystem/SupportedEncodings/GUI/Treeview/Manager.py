class Manager(object):

	def __init__(self, manager, editor):
		editor.response()
		from Initializer import Initializer
		Initializer(manager, editor)
		from SelectedEncodingsExtractor import Extractor
		Extractor(manager, editor)
		from RowSelector import Selector
		Selector(manager, editor)
		from ModelUpdater import Updater
		Updater(manager, editor)
		from ModelDataGenerator import Generator
		Generator(manager, editor)
		editor.response()
