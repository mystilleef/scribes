from gettext import gettext as _

class Manager(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("selected-mark", self.__selected_mark_cb)
		self.__sigid3 = manager.connect("marked-matches", self.__marked_matches_cb)
		self.__sigid4 = manager.connect("replace", self.__replace_cb)
		self.__sigid5 = manager.connect("replace-all", self.__replace_all_cb)
		self.__sigid6 = manager.connect("reset", self.__reset_cb)
		self.__sigid7 = manager.connect("hide-bar", self.__reset_cb)
		self.__sigid8 = manager.connect("search-string", self.__search_string_cb)
		self.__sigid9 = manager.connect("replace-string", self.__replace_string_cb)
		self.__sigid10 = manager.connect("match-object", self.__match_cb)
		from gobject import idle_add
		idle_add(self.__precompile_methods, priority=9999)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__buffer = editor.textbuffer
		self.__selected_mark = None
		self.__marks = None
		self.__string = ""
		self.__search_string = ""
		self.__match = None
		return

	def __destroy(self, *args):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		self.__editor.disconnect_signal(self.__sigid6, self.__manager)
		self.__editor.disconnect_signal(self.__sigid7, self.__manager)
		self.__editor.disconnect_signal(self.__sigid8, self.__manager)
		self.__editor.disconnect_signal(self.__sigid9, self.__manager)
		self.__editor.disconnect_signal(self.__sigid10, self.__manager)
		del self
		self = None
		return

	def __reset_flags(self):
		self.__selected_mark, self.__marks, self.__string = None, None, ""
		return False

	def __replace(self, marks, feedback=True):
		if not self.__search_string: return
		start = self.__editor.textbuffer.get_iter_at_mark(marks[0])
		end = self.__editor.textbuffer.get_iter_at_mark(marks[1])
		self.__editor.textview.window.freeze_updates()
		self.__editor.textbuffer.begin_user_action()
		self.__editor.textbuffer.delete(start, end)
		start = self.__editor.textbuffer.get_iter_at_mark(marks[0])
		self.__editor.textbuffer.insert(start, self.__string)
		self.__editor.textbuffer.end_user_action()
		self.__editor.textview.window.thaw_updates()
		self.__manager.emit("replaced-mark", marks)
		if feedback: message = _("Replaced '%s' with '%s'") % (self.__search_string, self.__string)
		if feedback: self.__editor.update_message(message, "pass", 10)
		return

	def __replace_all(self):
		if not self.__search_string: return False
		self.__editor.textview.window.freeze_updates()
		self.__editor.textbuffer.begin_user_action()
		[self.__replace(mark, False) for mark in self.__marks]
		self.__editor.textbuffer.end_user_action()
		self.__editor.textview.window.thaw_updates()
		message = _("Replaced all occurrences of '%s' with '%s'") % (self.__search_string, self.__string)
		self.__editor.update_message(message, "pass", 10)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __reset_cb(self, *args):
		self.__reset_flags()
		return False

	def __selected_mark_cb(self, manager, mark):
		self.__selected_mark = mark
		return False

	def __marked_matches_cb(self, manager, marks):
		self.__marks = marks
		return False

	def __replace_cb(self, *args):
		if self.__selected_mark: self.__replace(self.__selected_mark)
		return False

	def __replace_all_cb(self, *args):
		if self.__marks: self.__replace_all()
		return False

	def __replace_string_cb(self, manager, string):
#		self.__string = unicode(string, "utf-8")
		string = string.decode("utf-8")
		self.__string = self.__match.expand(string) if self.__match else string
		return False

	def __search_string_cb(self, manager, string):
		self.__search_string = string
		return False

	def __match_cb(self, manager, match):
		self.__match = match
		return False

	def __precompile_methods(self):
		methods = (self.__replace,)
		self.__editor.optimize(methods)
		return False
