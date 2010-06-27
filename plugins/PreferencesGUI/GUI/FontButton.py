class Button(object):

	def __init__(self, manager, editor):
		editor.response()
		self.__init_attributes(manager, editor)
		self.__sigid1 = self.__button.connect("font-set", self.__set_cb)
		self.__sigid2 = manager.connect("destroy", self.__destroy_cb)
		self.__sigid3 = manager.connect("database-update", self.__update_cb)
		self.__sigid4 = manager.connect("selected-language", self.__language_cb)
		self.__sigid5 = manager.connect("sensitive", self.__sensitive_cb)
		self.__sigid6 = manager.connect("reset", self.__reset_cb)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__editor = editor
		self.__manager = manager
		self.__button = manager.gui.get_object("FontButton")
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

	def __set(self):
		font_name = self.__button.get_font_name()
		from SCRIBES.FontMetadata import set_value
		set_value((self.__language, font_name))
		return False

	def __reset(self):
		from SCRIBES.FontMetadata import reset
		reset(self.__language)
		return False

	def __update(self, language=""):
		if language: self.__language = language
		from SCRIBES.FontMetadata import get_value
		font_name = get_value(self.__language)
		self.__button.handler_block(self.__sigid1)
		self.__button.set_font_name(font_name)
		self.__button.handler_unblock(self.__sigid1)
		self.__button.set_property("sensitive", True)
		return False

	def __update_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__update)
		return

	def __language_cb(self, manager, language):
		from gobject import idle_add
		idle_add(self.__update, language)
		return

	def __sensitive_cb(self, manager, sensitive):
		if not sensitive: self.__button.set_property("sensitive", False)
		return False

	def __set_cb(self, *args):
		self.__set()
		return True

	def __reset_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__reset)
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return
