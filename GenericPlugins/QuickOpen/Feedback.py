from gettext import gettext as _
STATUS_MESSAGE = _("Open files quickly")

class Feedback(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__sigid1 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid2 = manager.connect("pattern", self.__pattern_cb)
		self.__sigid3 = manager.connect("filtered-files", self.__files_cb)
		self.__sigid4 = manager.connect("entry-changed", self.__changed_cb)
		self.__sigid5 = manager.connect("current-path", self.__path_cb)
		self.__sigid6 = manager.connect("formatted-files", self.__formatted_cb)
		self.__sigid7 = manager.connect("show", self.__show_cb)
		self.__sigid8 = manager.connect("hide", self.__hide_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		self.__path = ""
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__manager)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		self.__editor.disconnect_signal(self.__sigid6, self.__manager)
		self.__editor.disconnect_signal(self.__sigid7, self.__manager)
		self.__editor.disconnect_signal(self.__sigid8, self.__manager)
		del self
		return False

	def __clear(self, pattern):
		if pattern: return False
		self.__manager.emit("clear-message")
		return False

	def __search(self):
		message = _("<span foreground='brown'><i>searching please wait...</i></span>")
		self.__manager.emit("message", message)
		return False

	def __message(self, files):
		try:
			from gobject import timeout_add
			if not files: raise ValueError
			message = _("<span foreground='blue'><b>%s matches found</b></span>") % len(files)
			self.__manager.emit("message", message)
			self.__timer1 = timeout_add(5000, self.__clear, "")
		except ValueError:
			message = _("<span foreground='red'><b>No match found</b></span>")
			self.__manager.emit("message", message)
			self.__timer2 = timeout_add(7000, self.__clear, "")
		return False

	def __current_path(self, uri):
		self.__path = uri
		message = _("<span foreground='brown'><i>updating search path please wait...</i></span>")
		self.__manager.emit("message", message)
		return False

	def __path_message(self):
		from gio import File
		path = File(self.__path).get_path()
		message = _("<span foreground='blue'><b>%s is the current search path</b></span>") % path
		self.__manager.emit("message", message)
		from gobject import timeout_add
		self.__timer3 = timeout_add(5000, self.__clear, "")
		return False

	def __remove_timer(self, _timer=1):
		try:
			timers = {
				1: self.__timer1,
				2: self.__timer2,
				3: self.__timer3,
				4: self.__timer4,
				5: self.__timer5,
				6: self.__timer6,
				7: self.__timer7,
				8: self.__timer8,
			}
			from gobject import source_remove
			source_remove(timers[_timer])
		except AttributeError:
			pass
		return False

	def __remove_all_timers(self):
		[self.__remove_timer(_timer) for _timer in xrange(1, 9)]
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __pattern_cb(self, manager, pattern):
		self.__remove_all_timers()
		from gobject import idle_add
		self.__timer4 = idle_add(self.__clear, pattern, priority=9999)
		return False

	def __files_cb(self, manager, files):
		self.__remove_all_timers()
		from gobject import idle_add
		self.__timer5 = idle_add(self.__message, files, priority=9999)
		return False

	def __changed_cb(self, *args):
		self.__remove_all_timers()
		from gobject import idle_add
		self.__timer6 = idle_add(self.__search, priority=9999)
		return False

	def __path_cb(self, manager, uri):
		self.__remove_all_timers()
		from gobject import idle_add
		self.__timer7 = idle_add(self.__current_path, uri, priority=9999)
		return False

	def __formatted_cb(self, *args):
		self.__remove_all_timers()
		from gobject import idle_add
		self.__timer8 = idle_add(self.__path_message, priority=9999)
		return False

	def __show_cb(self, *args):
		self.__editor.set_message(STATUS_MESSAGE)
		return False

	def __hide_cb(self, *args):
		self.__editor.unset_message(STATUS_MESSAGE)
		return False
