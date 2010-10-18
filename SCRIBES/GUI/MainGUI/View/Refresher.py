from SCRIBES.SignalConnectionManager import SignalManager

class Refresher(SignalManager):

	def __init__(self, editor):
		editor.response()
		SignalManager.__init__(self, editor)
		self.__init_attributes(editor)
		self.connect(editor, "quit", self.__quit_cb)
		self.connect(editor, "refresh", self.__refresh_cb, True)
#		from gobject import idle_add
#		idle_add(self.__optimize, priority=9999)
		editor.register_object(self)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__view = editor.textview
		return

	def __destroy(self):
		self.disconnect()
		self.__editor.unregister_object(self)
		del self
		return

	def __refresh(self, grab_focus=False):
		try:
			self.__editor.response()
			self.__view.window.process_updates(True)
		except:
			self.__editor.response()
		finally:
			if grab_focus: self.__view.grab_focus()
			self.__editor.response()
		return False

	def __optimize(self):
#		self.__editor.optimize((self.__refresh,))
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __refresh_cb(self, editor, grab_focus):
#		try:
#			from gobject import idle_add, source_remove
#			source_remove(self.__timer)
#		except AttributeError:
#			pass
#		finally:
#			self.__timer = idle_add(self.__refresh, grab_focus, priority=99999999)
		self.__refresh(grab_focus)
		return False
