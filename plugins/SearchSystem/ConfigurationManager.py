class Manager(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		from gnomevfs import monitor_add, MONITOR_FILE
		self.__monid1 = monitor_add(self.__match_word_uri, MONITOR_FILE, self.__database_changed_cb)
		self.__monid2 = monitor_add(self.__match_case_uri, MONITOR_FILE, self.__database_changed_cb)
		self.__monid3 = monitor_add(self.__search_mode_uri, MONITOR_FILE, self.__database_changed_cb)
		self.__monid4 = monitor_add(self.__search_type_uri, MONITOR_FILE, self.__database_changed_cb)
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
		from gnomevfs import get_uri_from_local_path as get_uri
		self.__match_word_uri = get_uri(word_path)
		self.__match_case_uri = get_uri(case_path)
		self.__search_mode_uri = get_uri(mode_path)
		self.__search_type_uri = get_uri(type_path)
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
		from gnomevfs import monitor_cancel
		if self.__monid1: monitor_cancel(self.__monid1)
		if self.__monid2: monitor_cancel(self.__monid2)
		if self.__monid3: monitor_cancel(self.__monid3)
		if self.__monid4: monitor_cancel(self.__monid4)
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		del self
		self = None
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return

	def __database_changed_cb(self, *args):
		self.__emit_change_signal()
		return False
