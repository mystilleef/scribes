class Refresher(object):

	def __init__(self, editor):
		editor.response()
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("refresh", self.__refresh_cb)
		editor.register_object(self)
		from gobject import idle_add
		idle_add(self.__optimize, priority=9999)
		editor.response()

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__view = editor.textview
		self.__count = 0
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return

	def __refresh(self, grab_focus=True):
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
		self.__editor.optimize((self.__refresh,))
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __refresh_cb(self, editor, grab_focus):
		self.__refresh(grab_focus)
		return False
