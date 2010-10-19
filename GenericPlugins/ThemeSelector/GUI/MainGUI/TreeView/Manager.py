class Manager(object):

	def __init__(self, manager, editor):
		from Initializer import Initializer
		Initializer(manager, editor)
		from Disabler import Disabler
		Disabler(manager, editor)
		from RowDeleter import Deleter
		Deleter(manager, editor)
		from RowActivator import Activator
		Activator(manager, editor)
		from RowSelectionMonitor import Monitor
		Monitor(manager, editor)
		from RowSelector import Selector
		Selector(manager, editor)
		from ModelUpdater import Updater
		Updater(manager, editor)
		from ModelDataGenerator import Generator
		Generator(manager, editor)
