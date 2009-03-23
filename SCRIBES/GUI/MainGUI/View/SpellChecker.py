class Checker(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("enable-spell-checking", self.__checking_cb)
		self.__set()
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__view = editor.textview
		self.__checker = None
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __set(self):
		from SCRIBES.SpellCheckMetadata import get_value
		if not get_value(): return False
		self.__enable()
		return False

	def __enable(self):
		try:
			self.__editor.response()
			from gobject import GError
			from gtkspell import Spell
			from locale import getdefaultlocale
			self.__checker = Spell(self.__view, getdefaultlocale()[0])
		except GError:
			pass
		finally:
			self.__editor.response()
		return False

	def __disable(self):
		self.__editor.response()
		if self.__checker: self.__checker.detach()
		self.__editor.response()
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __checking_cb(self, editor, enable):
		from gobject import idle_add
		idle_add(self.__enable if enable else self.__disable)
		return False
