from gobject import GObject, SIGNAL_ACTION, SIGNAL_RUN_LAST
from gobject import SIGNAL_NO_RECURSE, TYPE_NONE, TYPE_PYOBJECT
SSIGNAL = SIGNAL_RUN_LAST|SIGNAL_NO_RECURSE|SIGNAL_ACTION

class Manager(GObject):

	__gsignals__ = {
		"update-python-path": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"validate-path": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"plugin-path-error": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"search-path-updated": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"plugin-path-not-found-error": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"create-plugin-path": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"plugin-folder-creation-error": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"initialized-module": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"validate-language-module": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"valid-module": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"initialize-module": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"load-plugin": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"unload-plugin": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"loaded-plugin": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"unloaded-plugin": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"check-duplicate-plugins": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"active-plugins": (SSIGNAL, TYPE_NONE, (TYPE_PYOBJECT,)),
		"destroyed-plugins": (SSIGNAL, TYPE_NONE, ()),
	}

	def __init__(self, editor):
		editor.response()
		GObject.__init__(self)
		from PluginReloader import Reloader
		Reloader(self, editor)
		from PluginsDestroyer import Destroyer
		Destroyer(self, editor)
		from PluginsUpdater import Updater
		Updater(self, editor)
		from PluginUnloader import Unloader
		Unloader(self, editor)
		from PluginLoader import Loader
		Loader(self, editor)
		from DuplicatePluginDetector import Detector
		Detector(self, editor)
		from PluginValidator import Validator
		Validator(self, editor)
		from LanguageModuleValidator import Validator
		Validator(self, editor)
		from ModuleValidator import Validator
		Validator(self, editor)
		from ModuleInitializer import Initializer
		Initializer(self, editor)
		from ModuleFinder import Finder
		Finder(self, editor)
		from ErrorManager import Manager
		Manager(self, editor)
		from HomePluginPathCreator import Creator
		Creator(self, editor)
		from PythonPathUpdater import Updater
		Updater(self, editor)
		from PluginPathErrorHandler import Handler
		Handler(self, editor)
		from PluginPathValidator import Validator
		Validator(self, editor)
		from Initializer import Initializer
		Initializer(self, editor)
		editor.response()
