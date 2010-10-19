class Manager(object):

	def __init__(self, editor):
		self.__init_attributes(editor)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.connect("fullscreen", self.__fullscreen_cb)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		self.__window = editor.window
		return

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __activate(self, fullscreen):
		self.__window.fullscreen() if fullscreen else self.__window.unfullscreen()
		self.__editor.move_view_to_cursor(True)
		return False

	def __quit_cb(self, *args):
		self.__destroy()
		return False

	def __fullscreen_cb(self, editor, fullscreen):
		from gobject import idle_add
		idle_add(self.__activate, fullscreen)
		return False
