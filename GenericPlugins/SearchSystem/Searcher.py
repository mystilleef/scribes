from gettext import gettext as _
message = _("No matches found")

class Searcher(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("search-boundary", self.__boundary_cb)
		self.__sigid3 = manager.connect("new-regex", self.__regex_cb)
		self.__sigid4 = manager.connect("regex-flags", self.__regex_flags_cb)
		self.__sigid5 = manager.connect("search-mode-flag", self.__search_mode_cb)
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=9999)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__text = None
		self.__regex_flags = None
		self.__regex_mode = False
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		del self
		self = None
		return

	def __find_matches(self, regex_object):
		iterator = regex_object.finditer(self.__text)
		matches = [match.span() for match in iterator]
		match_object = regex_object.search(self.__text) if self.__regex_mode else None
		self.__manager.emit("match-object", match_object)
		self.__manager.emit("found-matches", matches)
		if not matches: self.__manager.emit("search-complete")
		if not matches: self.__editor.update_message(message, "fail", 10)
		return

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __boundary_cb(self, manager, boundary):
		self.__text = self.__editor.textbuffer.get_text(*(boundary)).decode("utf-8")
		return False

	def __regex_cb(self, manager, regex_object):
		self.__find_matches(regex_object)
		return False

	def __regex_flags_cb(self, manager, flags):
		self.__regex_flags = flags
		return False

	def __precompile_methods(self):
		methods = (self.__find_matches,)
		self.__editor.optimize(methods)
		return False

	def __search_mode_cb(self, manager, search_mode):
		self.__regex_mode = True if search_mode == "regex" else False
		return False
