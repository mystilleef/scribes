from Signals import Signal

class Manager(Signal):

	def __init__(self, editor):
		Signal.__init__(self)
		self.__init_attributes(editor)
		from Feedback import Feedback
		Feedback(self, editor)
		from GUI.Manager import Manager
		Manager(self, editor)
		from ThemeFileInstaller import Installer
		Installer(self, editor)
		from ThemeFileValidator import Validator
		Validator(self, editor)
		from DatabaseWriter import Writer
		Writer(self, editor)
		from DatabaseReader import Reader
		Reader(self, editor)
		from DatabaseMonitor import Monitor
		Monitor(self, editor)
		from ThemeRemover import Remover
		Remover(self, editor)
		from ThemeUpdater import Updater
		Updater(self, editor)
		from ThemeDispatcher import Dispatcher
		Dispatcher(self, editor)
		from ThemeFolderMonitor import Monitor
		Monitor(self, editor)

	def __init_attributes(self, editor):
		from os.path import join
		self.__main_gui = editor.get_gui_object(globals(), join("GUI", "MainGUI", "GUI.glade"))
		self.__chooser_gui = editor.get_gui_object(globals(), join("GUI", "FileChooserGUI", "GUI.glade"))
		return False

	main_gui = property(lambda self: self.__main_gui)
	chooser_gui = property(lambda self: self.__chooser_gui)

	def destroy(self):
		self.emit("destroy")
		del self
		return False

	def activate(self):
		self.emit("activate")
		return False
