class Button(object):

	def __init__(self, manager, editor):
		self.__init_attributes(manager, editor)
		self.__set_properties()
		self.__sigid1 = self.__button.connect("value-changed", self.__changed_cb)
		self.__sigid2 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid3 = manager.connect("database-update", self.__update_cb)
		self.__sigid4 = manager.connect("selected-language", self.__language_cb)
		self.__sigid5 = manager.connect("sensitive", self.__sensitive_cb)
		self.__sigid6 = manager.connect("reset", self.__reset_cb)

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		self.__button = manager.gui.get_object("TabSpinButton")
		self.__language = "plain text"
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__button)
		self.__editor.disconnect_signal(self.__sigid2, self.__manager)
		self.__editor.disconnect_signal(self.__sigid3, self.__manager)
		self.__editor.disconnect_signal(self.__sigid4, self.__manager)
		self.__editor.disconnect_signal(self.__sigid5, self.__manager)
		self.__editor.disconnect_signal(self.__sigid6, self.__manager)
		del self
		self = None
		return False

	def __delayed_set(self):
		try:
			from gobject import timeout_add, source_remove
			source_remove(self.__timer1)
		except AttributeError:
			pass
		finally:
			self.__timer1 = timeout_add(250, self.__set, priority=9999)
		return False

	def __reset(self):
		from SCRIBES.TabWidthMetadata import reset
		reset(self.__language)
		return False

	def __set(self):
		tab_size = int(self.__button.get_value())
		from SCRIBES.TabWidthMetadata import set_value
		set_value((self.__language, tab_size))
		return False

	def __update(self, language=""):
		if language: self.__language = language
		from SCRIBES.TabWidthMetadata import get_value
		tab_size = get_value(self.__language)
		self.__button.handler_block(self.__sigid1)
		self.__button.set_value(tab_size)
		self.__button.handler_unblock(self.__sigid1)
		self.__button.set_property("sensitive", True)
		return False

	def __set_properties(self):
		self.__button.set_max_length(3)
		self.__button.set_width_chars(3)
		self.__button.set_digits(0)
		self.__button.set_increments(1, 5)
		self.__button.set_range(1, 24)
		from gtk import UPDATE_ALWAYS
		self.__button.set_update_policy(UPDATE_ALWAYS)
		self.__button.set_numeric(True)
		self.__button.set_snap_to_ticks(True)
		return

	def __changed_cb(self, *args):
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__timer2)
		except AttributeError:
			pass
		finally:
			self.__timer2 = idle_add(self.__delayed_set, priority=9999)
		return True

	def __update_cb(self, *args):
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__timer3)
		except AttributeError:
			pass
		finally:
			self.__timer3 = idle_add(self.__update)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __language_cb(self, manager, language):
		try:
			from gobject import idle_add, source_remove
			source_remove(self.__timer4)
		except AttributeError:
			pass
		finally:
			self.__timer4 = idle_add(self.__update, language)
		return

	def __sensitive_cb(self, manager, sensitive):
		if not sensitive: self.__button.set_property("sensitive", False)
		return False

	def __reset_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__reset)
		return False
