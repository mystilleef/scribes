from gettext import gettext as _
from SCRIBES.SignalConnectionManager import SignalManager
PLUGIN_PATH_ERROR_MESSAGE = _("ERROR: Cannot find plugin folder. Scribes will not function properly without plugins. Please file a bug report to address the issue.")
PATH_CREATION_ERROR_MESSAGE = _("ERROR: Cannot create local plugin folder. Please address the source of the problem for Scribes to function properly.")
PLUGIN_ERROR = _("PLUGIN ERROR!")

class Manager(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(manager, "plugin-path-not-found-error", self.__not_found_cb)
		self.connect(manager, "plugin-folder-creation-error", self.__creation_error_cb)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return False

	def __error(self, title, message):
		self.__editor.show_error(title, message)
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __not_found_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__error, PLUGIN_ERROR, PLUGIN_PATH_ERROR_MESSAGE)
		return False

	def __creation_error_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__error, PLUGIN_ERROR, PATH_CREATION_ERROR_MESSAGE)
		return False
