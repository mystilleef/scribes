class Manager(object):

	def __init__(self, manager, editor):
		from Initializer import Initializer
		Initializer(manager, editor)
		from KeyboardHandler import Handler
		Handler(manager, editor)
		from FocusMonitor import Monitor
		Monitor(manager, editor)
		from ModelUpdater import Updater
		Updater(manager, editor)
		from ModelDataGenerator import Generator
		Generator(manager, editor)
		from RowExpansionHandler import Handler
		Handler(manager, editor)
		from RowActivationHandler import Handler
		Handler(manager, editor)
		from FocusSwitcher import Switcher
		Switcher(manager, editor)
		from FocusGrabber import Grabber
		Grabber(manager, editor)
		from SensitivityManager import Manager
		Manager(manager)
