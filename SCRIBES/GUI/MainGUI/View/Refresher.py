from gtk import events_pending, main_iteration
from SCRIBES.SignalConnectionManager import SignalManager

class Refresher(SignalManager):

	def __init__(self, editor):
		SignalManager.__init__(self)
		self.__init_attributes(editor)
		self.connect(editor, "post-quit", self.__quit_cb)
		self.connect(editor, "refresh", self.__refresh_cb, True)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__view = editor.textview
		return

	def __destroy(self):
		self.disconnect()
		del self
		return

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __refresh_cb(self, editor, grab_focus):
		try:
			while events_pending(): main_iteration(False)
			self.__view.window.process_updates(True)
		except AttributeError:
			pass
		finally:
			if grab_focus: self.__view.grab_focus()
			while events_pending(): main_iteration(False)
		return False
