class Manager(object):

	def __init__(self, manager, editor):
		from Initializer import Initializer
		Initializer(manager, editor)
		from KeyboardHandler import Handler
		Handler(manager, editor)
		from RowActivationHandler import Handler
		Handler(manager, editor)
		from ModelUpdater import Updater
		Updater(manager, editor)
		from ModelDataGenerator import Generator
		Generator(manager, editor)
