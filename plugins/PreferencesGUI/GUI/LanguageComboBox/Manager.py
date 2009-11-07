class Manager(object):

	def __init__(self, manager, editor):
		from Initializer import Initializer
		Initializer(manager, editor)
		from LanguageEmitter import Emitter
		Emitter(manager, editor)
		from LanguageSelector import Selector
		Selector(manager, editor)
		from ModelUpdater import Updater
		Updater(manager, editor)
		from DataModelGenerator import Generator
		Generator(manager, editor)
