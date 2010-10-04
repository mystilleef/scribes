from gettext import gettext as _
from SCRIBES.SignalConnectionManager import SignalManager

BRACKET_MESSAGE = _("Bracket selection")
UNDO_MESSAGE = _("Removed last selection")
QUOTE_MESSAGE = _("Quote selection")
FAIL_MESSAGE = _("No brackets found")

class Feedback(SignalManager):

	def __init__(self, manager, editor):
		editor.response()
		SignalManager.__init__(self, editor)
		self.__init_attributes(manager, editor)
		self.connect(manager, "destroy", self.__destroy_cb)
		self.connect(manager, "select-offsets", self.__select_cb, True)
		self.connect(manager, "no-pair-character-found", self.__no_cb, True)
		self.connect(manager, "undo-selection", self.__undo_cb, True)
		editor.response()

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __destroy(self):
		self.disconnect()
		del self
		return False

	def __update_message(self, offset):
		try:
			get_iter = self.__editor.textbuffer.get_iter_at_offset
			character = get_iter(offset-1).get_char()
			from Utils import QUOTE_CHARACTERS as QC, OPEN_PAIR_CHARACTERS as OC
			if not (character in QC) and not (character in OC): raise ValueError
			self.__set_message(character)
		except ValueError:
			character = self.__editor.selected_text[0]
			self.__set_message(character)
		return False

	def __set_message(self, character):
		from Utils import QUOTE_CHARACTERS as QC
		message = QUOTE_MESSAGE if character in QC else BRACKET_MESSAGE
		self.__editor.update_message(message, "yes")
		return False

	def __destroy_cb(self, *args):
		self.__destroy()
		return False

	def __select_cb(self, manager, offsets):
		from gobject import idle_add
		idle_add(self.__update_message, offsets[0])
		return False

	def __no_cb(self, *args):
		self.__editor.update_message(FAIL_MESSAGE, "no")
		return False

	def __undo_cb(self, *args):
		self.__editor.update_message(UNDO_MESSAGE, "info")
		return False
