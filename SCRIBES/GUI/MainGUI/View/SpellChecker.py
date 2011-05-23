class Checker(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("enable-spell-checking", self.__checking_cb)
		self.__sigid3 = editor.connect("load-error", self.__check_cb)
		self.__sigid4 = editor.connect("checking-file", self.__check_cb)
		self.__sigid5 = editor.connect("renamed-file", self.__check_cb)
		self.__set()
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__view = editor.textview
		self.__checker = None
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.disconnect_signal(self.__sigid3, self.__editor)
		self.__editor.disconnect_signal(self.__sigid4, self.__editor)
		self.__editor.disconnect_signal(self.__sigid5, self.__editor)
		self.__editor.unregister_object(self)
		del self
		return False

	def __set(self):
		from SCRIBES.SpellCheckMetadata import get_value
		language = self.__editor.language
		language = language if language else "plain text"
		self.__enable() if get_value(language) else self.__disable()
		return False

	def __enable(self):
		try:
			from gobject import GError
			from gtkspell import Spell
			from locale import getdefaultlocale
			if self.__checker: return False
			self.__checker = Spell(self.__view, getdefaultlocale()[0])
		except GError:
			pass
		except ImportError:
			print "ERROR: I cannot find the Python bindings for GtkSpell"
		return False

	def __disable(self):
		if self.__checker: self.__checker.detach()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __checking_cb(self, editor, enable):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__enable if enable else self.__disable, priority=PRIORITY_LOW)
		return False

	def __check_cb(self, *args):
		from gobject import idle_add, PRIORITY_LOW
		idle_add(self.__set, priority=PRIORITY_LOW)
		return False
