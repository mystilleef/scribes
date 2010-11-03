class Manager(object):

	def __init__(self, manager):
		from Initializer import Initializer
		Initializer(manager)
		from UpDownKeyHandler import Handler
		Handler(manager)
		from KeyboardHandler import Handler
		Handler(manager)
		from Disabler import Disabler
		Disabler(manager)
		from RowSelector import Selector
		Selector(manager)
		from RowActivator import Activator
		Activator(manager)
		from ModelUpdater import Updater
		Updater(manager)
		from ModelDataGenerator import Generator
		Generator(manager)
