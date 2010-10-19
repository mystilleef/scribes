class BaseBinder(object):

	def __init__(self, editor, shortcut, signal):
		self.__init_attributes(editor)
		self.__bind(shortcut, signal)
		self.__sigid1 = editor.connect("quit", self.__quit_cb)
		self.__sigid2 = editor.window.connect(signal, self.__activate_cb)
		editor.register_object(self)

	def __init_attributes(self, editor):
		self.__editor = editor
		return

	def __bind(self, shortcut, signal):
		from gtk import accelerator_parse
		keyval, modifier = accelerator_parse(shortcut)
		if (keyval, modifier) in self.__editor.get_shortcuts(): return False
		from gtk import binding_entry_add_signal as bind
		bind(self.__editor.window, keyval, modifier, signal, str, shortcut)
		self.__editor.add_shortcut((keyval, modifier))
		return False

	def __destroy(self):
		self.__editor.disconnect_signal(self.__sigid1, self.__editor)
		self.__editor.disconnect_signal(self.__sigid2, self.__editor.window)
		self.__editor.unregister_object(self)
		del self
		self = None
		return False

	def __quit_cb(self, *args):
		from gobject import idle_add
		idle_add(self.__destroy)
		return False

	def __activate_cb(self, *args):
		from gobject import idle_add
		idle_add(self.activate)
		return False
