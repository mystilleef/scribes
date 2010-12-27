from gettext import gettext as _
from SCRIBES.SignalConnectionManager import SignalManager

class Switcher(SignalManager):

	def __init__(self, manager, editor):
		SignalManager.__init__(self)
		self.__init_attributes(manager, editor)
		self.connect(manager, "activate", self.__activate_cb)
		self.connect(manager, "destroy", self.__destroy_cb)

	def __init_attributes(self, manager, editor):
		self.__manager = manager
		self.__editor = editor
		return

	def __switch(self):
		try:
			start = self.__editor.cursor.copy()
			if start.starts_line() or start.ends_line(): raise ValueError
			self.__editor.freeze()
			start.backward_char()
			end = self.__editor.cursor.copy()
			textbuffer = self.__editor.textbuffer
			character = textbuffer.get_text(start, end)
			textbuffer.begin_user_action()
			textbuffer.delete(start, end)
			iterator = self.__editor.cursor.copy()
			iterator.forward_char()
			textbuffer.place_cursor(iterator)
			textbuffer.insert_at_cursor(character)
			textbuffer.end_user_action()
			self.__editor.thaw()
			self.__editor.update_message(_("Switched character"), "yes")
		except ValueError:
			self.__editor.update_message(_("Invalid operation"), "no")
		return False

	def __activate_cb(self, *args):
		self.__switch()
		return False

	def __destroy_cb(self, *args):
		self.disconnect()
		del self
		return False
