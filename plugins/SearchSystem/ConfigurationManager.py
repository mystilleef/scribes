class Manager(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__word_monitor.connect("changed", self.__changed_cb)
		self.__case_monitor.connect("changed", self.__changed_cb)
		self.__mode_monitor.connect("changed", self.__changed_cb)
		self.__type_monitor.connect("changed", self.__changed_cb)
		self.__emit_change_signal()

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		from os.path import join
		preference_folder = join(editor.metadata_folder, "PluginPreferences")
		word_path = join(preference_folder, "MatchWord.gdb")
		case_path = join(preference_folder, "MatchCase.gdb")
		mode_path = join(preference_folder, "SearchMode.gdb")
		type_path = join(preference_folder, "SearchType.gdb")
		self.__word_monitor = editor.get_file_monitor(word_path)
		self.__case_monitor = editor.get_file_monitor(case_path)
		self.__mode_monitor = editor.get_file_monitor(mode_path)
		self.__type_monitor = editor.get_file_monitor(type_path)
		return

	def __emit_change_signal(self):
		from MatchCaseMetadata import get_value
		self.__manager.emit("match-case-flag", get_value())
		from MatchWordMetadata import get_value
		self.__manager.emit("match-word-flag", get_value())
		from SearchModeMetadata import get_value
		self.__manager.emit("search-mode-flag", get_value())
		from SearchTypeMetadata import get_value
		self.__manager.emit("search-type-flag", get_value())
		return

	def __destroy(self):
		self.__word_monitor.cancel()
		self.__case_monitor.cancel()
		self.__mode_monitor.cancel()
		self.__type_monitor.cancel()
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return

	def __changed_cb(self, *args):
		if not self.__editor.monitor_events(args, (0,2,3)): return False
		self.__emit_change_signal()
		return False
